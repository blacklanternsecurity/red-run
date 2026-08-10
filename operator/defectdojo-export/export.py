#!/usr/bin/env python3
"""Export red-run engagement findings to DefectDojo.

Two modes:

  --out FILE    write DefectDojo "Generic Findings Import" JSON (no network)
  --push        POST straight to /api/v2/import-scan/ (needs URL + token)

The generic-import format is the safer default: it produces a file you can
inspect before anything reaches DefectDojo, and it is the same payload --push
sends.

WHAT THIS EXPORTS, AND WHAT IT CANNOT
-------------------------------------
DefectDojo models vulnerabilities. red-run models an *engagement* — how access
was obtained, which credentials unlocked what, which techniques were tried and
refuted. Only the first has a home in DefectDojo.

Exported:   vulns -> Findings (title, severity, CVSS, CWE, evidence path)
Flattened:  the provenance chain (via_access_id / via_credential_id /
            via_vuln_id) is rendered into each finding's description, because
            DefectDojo has no way to represent it structurally.
NOT sent:   access, credentials, credential_access, pivot_map, tunnels, and
            `blocked`. The last one matters: `blocked` holds every technique
            attempted and refuted, which is a large part of what tells a reader
            "secure" apart from "not looked at". The script prints a count of
            what it left behind so the omission is visible rather than silent.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

SEVERITY = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "info": "Info",
}


def _conn(db: Path) -> sqlite3.Connection:
    if not db.exists():
        sys.exit(f"error: no database at {db}")
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def _chain(conn: sqlite3.Connection, v: sqlite3.Row) -> list[str]:
    """Render provenance as prose. DefectDojo cannot hold the graph itself."""
    out = []
    if v["via_vuln_id"]:
        r = conn.execute(
            "SELECT title FROM vulns WHERE id = ?", (v["via_vuln_id"],)
        ).fetchone()
        if r:
            out.append(f"Chains from finding #{v['via_vuln_id']} — {r['title']}")
    if v["via_access_id"]:
        r = conn.execute(
            "SELECT username, access_type, method FROM access WHERE id = ?",
            (v["via_access_id"],),
        ).fetchone()
        if r:
            out.append(
                f"Discovered from access #{v['via_access_id']} "
                f"({r['username'] or 'unknown user'} via {r['access_type']})"
            )
    if v["via_credential_id"]:
        r = conn.execute(
            "SELECT username, secret_type FROM credentials WHERE id = ?",
            (v["via_credential_id"],),
        ).fetchone()
        if r:
            out.append(
                f"Found using credential #{v['via_credential_id']} "
                f"({r['username'] or 'unnamed'}, {r['secret_type']})"
            )
    return out


def build(db: Path, include_info: bool) -> tuple[dict, dict]:
    conn = _conn(db)
    rows = conn.execute(
        "SELECT v.*, t.ip, t.hostname FROM vulns v "
        "LEFT JOIN targets t ON t.id = v.target_id ORDER BY v.id"
    ).fetchall()

    findings = []
    skipped_info = 0
    for v in rows:
        sev = SEVERITY.get(v["severity"], "Info")
        if sev == "Info" and not include_info:
            skipped_info += 1
            continue

        host = v["hostname"] or v["ip"] or ""
        desc = [v["details"] or "(no detail recorded)"]

        chain = _chain(conn, v)
        if chain:
            desc.append("\n**Provenance**\n" + "\n".join(f"- {c}" for c in chain))
        if v["discovered_by"]:
            desc.append(f"\nFound by: {v['discovered_by']}")
        desc.append(f"\nred-run status: {v['status']}")

        f: dict = {
            # Stable across re-runs: lets DefectDojo reimport instead of
            # duplicating on every export.
            "unique_id_from_tool": f"red-run-vuln-{v['id']}",
            "title": v["title"],
            "description": "\n".join(desc),
            "severity": sev,
            "date": (v["created_at"] or "")[:10],
            # 'actioned' is the only red-run status meaning we demonstrated it.
            "verified": v["status"] == "actioned",
            "active": v["status"] != "blocked",
            "static_finding": False,
            "dynamic_finding": True,
        }
        if host:
            f["endpoints"] = [host]
        if v["cvss_vector"]:
            vec = v["cvss_vector"]
            f["cvssv3"] = vec if vec.startswith("CVSS:") else f"CVSS:3.1/{vec}"
        if v["cwe"]:
            digits = "".join(c for c in v["cwe"] if c.isdigit())
            if digits:
                f["cwe"] = int(digits)
        if v["evidence_path"]:
            f["file_path"] = v["evidence_path"]
        if v["vuln_type"]:
            f["vuln_id_from_tool"] = v["vuln_type"]

        findings.append(f)

    left_behind = {
        "blocked (techniques attempted and refuted)": conn.execute(
            "SELECT COUNT(*) FROM blocked"
        ).fetchone()[0],
        "access records (the chain)": conn.execute(
            "SELECT COUNT(*) FROM access"
        ).fetchone()[0],
        "credentials": conn.execute("SELECT COUNT(*) FROM credentials").fetchone()[0],
        "pivots": conn.execute("SELECT COUNT(*) FROM pivot_map").fetchone()[0],
        "info findings skipped": skipped_info,
    }
    conn.close()
    return {"findings": findings}, left_behind


def push(payload: dict, url: str, token: str, product: str, engagement: str) -> None:
    """POST to /api/v2/import-scan/ as a Generic Findings Import."""
    boundary = "----redrun"
    body = []
    for key, val in (
        ("scan_type", "Generic Findings Import"),
        ("product_name", product),
        ("engagement_name", engagement),
        ("active", "true"),
        ("verified", "false"),
        ("auto_create_context", "true"),
    ):
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{val}\r\n")
    body.append(
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="red-run.json"\r\n'
        "Content-Type: application/json\r\n\r\n"
        + json.dumps(payload)
        + "\r\n"
    )
    body.append(f"--{boundary}--\r\n")
    data = "".join(body).encode()

    req = urllib.request.Request(
        url.rstrip("/") + "/api/v2/import-scan/",
        data=data,
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            print(f"pushed: HTTP {r.status}")
    except urllib.error.HTTPError as e:
        sys.exit(f"push failed: HTTP {e.code} — {e.read().decode()[:400]}")
    except urllib.error.URLError as e:
        sys.exit(f"push failed: {e.reason}")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", type=Path, default=root / "engagement" / "state.db")
    ap.add_argument("--out", type=Path, help="write the import JSON here")
    ap.add_argument("--push", action="store_true", help="POST to DefectDojo")
    ap.add_argument("--url", help="DefectDojo base URL (with --push)")
    ap.add_argument("--token", help="API v2 token (with --push)")
    ap.add_argument("--product", default="red-run", help="DefectDojo product name")
    ap.add_argument("--engagement", default="red-run engagement")
    ap.add_argument(
        "--include-info",
        action="store_true",
        help="also export info-severity findings (refuted candidates, scope "
        "notes). Off by default: they are not vulnerabilities, and importing "
        "them makes controls that held look like open issues.",
    )
    a = ap.parse_args()

    if not a.out and not a.push:
        ap.error("nothing to do — pass --out FILE or --push")
    if a.push and not (a.url and a.token):
        ap.error("--push needs --url and --token")

    payload, left = build(a.db, a.include_info)
    print(f"{len(payload['findings'])} finding(s) prepared from {a.db}")

    print("\nnot exported — DefectDojo has no model for these:")
    for k, n in left.items():
        if n:
            print(f"  {n:>4}  {k}")

    if a.out:
        a.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"\nwrote {a.out}")
    if a.push:
        push(payload, a.url, a.token, a.product, a.engagement)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
