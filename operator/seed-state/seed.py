#!/usr/bin/env python3
"""Seed an engagement state database with operator-known information.

Creates engagement/state.db (or opens an existing one) and interactively
collects targets, ports, credentials, access entries, and vulnerabilities
from the operator. Uses the same schema as the state-server MCP — the
orchestrator's resume flow picks up the seeded state automatically.

Usage:
    python3 operator/seed-state/seed.py [--db engagement/state.db] [--name my-engagement]
    python3 operator/seed-state/seed.py --from seed.yaml

Run from the project root (red-run/).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add state-server to path so we can import schema.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools" / "state-server"))

from schema import init_db


def _input(prompt: str, default: str = "") -> str:
    """Prompt with optional default."""
    if default:
        val = input(f"  {prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"  {prompt}: ").strip()


def _yes(prompt: str, default: bool = True) -> bool:
    """Yes/no prompt."""
    suffix = "Y/n" if default else "y/N"
    val = input(f"\n  {prompt} ({suffix}): ").strip().lower()
    if not val:
        return default
    return val in ("y", "yes")


def _pick(prompt: str, options: list[str]) -> str:
    """Single-select from a list."""
    print(f"\n  {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        val = input(f"  Choice [1-{len(options)}]: ").strip()
        if val.isdigit() and 1 <= int(val) <= len(options):
            return options[int(val) - 1]
        print(f"    Invalid — enter 1-{len(options)}")


def _parse_ports(text: str) -> list[int]:
    """Parse comma-separated ports, ignoring invalid entries."""
    ports = []
    for part in text.replace(" ", "").split(","):
        if part.isdigit():
            ports.append(int(part))
    return ports


def _get_target_id(conn, host: str) -> int | None:
    """Look up a target by host, return its id or None."""
    row = conn.execute("SELECT id FROM targets WHERE host = ?", (host,)).fetchone()
    return row[0] if row else None


def add_target(conn) -> int | None:
    """Interactively add a target. Returns the target id."""
    host = _input("Host (IP or hostname)")
    if not host:
        return None

    existing = _get_target_id(conn, host)
    if existing:
        print(f"    Target {host} already exists (id={existing})")
        return existing

    os_type = _input("OS (linux/windows/unknown)", "unknown")
    role = _input("Role (dc, web, db, workstation, etc.)", "")
    notes = _input("Notes", "")

    conn.execute(
        "INSERT INTO targets (host, os, role, notes, discovered_by) VALUES (?, ?, ?, ?, ?)",
        (host, os_type, role, notes, "operator-seed"),
    )
    conn.commit()
    target_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"    Added target {host} (id={target_id})")

    # Ports
    ports_str = _input("Ports (comma-separated, or blank to skip)", "")
    if ports_str:
        ports = _parse_ports(ports_str)
        for port in ports:
            service = _input(f"  Service on port {port}", "")
            try:
                conn.execute(
                    "INSERT INTO ports (target_id, port, service) VALUES (?, ?, ?)",
                    (target_id, port, service),
                )
            except Exception:
                print(f"    Port {port} already exists, skipping")
        conn.commit()
        print(f"    Added {len(ports)} port(s)")

    return target_id


def add_credential(conn):
    """Interactively add a credential."""
    username = _input("Username")
    if not username:
        return

    secret = _input("Secret (password, hash, key path)")
    secret_type = _pick("Secret type", [
        "password", "ntlm_hash", "aes_key", "kerberos_tgt",
        "kerberos_tgs", "ssh_key", "token", "certificate", "other",
    ])
    domain = _input("Domain (blank if none)", "")
    source = _input("Source (where you got it)", "operator-provided")
    notes = _input("Notes", "")

    conn.execute(
        """INSERT INTO credentials (username, secret, secret_type, domain, source, notes, discovered_by)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (username, secret, secret_type, domain, source, notes, "operator-seed"),
    )
    conn.commit()
    cred_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"    Added credential {domain}\\{username} (id={cred_id})")


def add_access(conn):
    """Interactively add an access entry."""
    host = _input("Target IP/hostname (must match a target you already added)")
    if not host:
        return

    target_id = _get_target_id(conn, host)
    if not target_id:
        print(f"    Target {host} not found — add it as a target first")
        return

    access_type = _pick("Access type", [
        "shell", "ssh", "winrm", "rdp", "web_shell", "db", "token", "vpn", "other",
    ])
    username = _input("Username", "")
    privilege = _pick("Privilege level", [
        "user", "admin", "root", "system", "service", "domain_admin", "other",
    ])
    method = _input("Method (how you got access)", "operator-provided")
    notes = _input("Notes", "")

    conn.execute(
        """INSERT INTO access (target_id, access_type, username, privilege, method, notes, discovered_by)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (target_id, access_type, username, privilege, method, notes, "operator-seed"),
    )
    conn.commit()
    access_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"    Added {access_type} access as {username} on {host} (id={access_id})")


def add_vuln(conn):
    """Interactively add a vulnerability."""
    host = _input("Target IP/hostname (must match a target you already added)")
    if not host:
        return

    target_id = _get_target_id(conn, host)
    if not target_id:
        print(f"    Target {host} not found — add it as a target first")
        return

    title = _input("Title (e.g., 'SQL injection in login form')")
    if not title:
        return

    vuln_type = _input("Type (sqli, xss, rce, lfi, etc.)", "")
    severity = _pick("Severity", ["info", "low", "medium", "high", "critical"])
    endpoint = _input("Endpoint (URL, port, parameter)", "")
    details = _input("Details", "")

    conn.execute(
        """INSERT INTO vulns (target_id, title, vuln_type, severity, endpoint, details, discovered_by)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (target_id, title, vuln_type, severity, endpoint, details, "operator-seed"),
    )
    conn.commit()
    vuln_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"    Added vuln '{title}' on {host} (id={vuln_id})")


def load_yaml(conn, path: Path):
    """Load a seed file and populate the database."""
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML required for --from. Install with: pip install pyyaml")
        sys.exit(1)

    data = yaml.safe_load(path.read_text())
    if not data:
        print("Error: empty seed file")
        sys.exit(1)

    # Targets + ports
    for t in data.get("targets", []):
        host = t["host"]
        existing = _get_target_id(conn, host)
        if existing:
            target_id = existing
            print(f"  Target {host} already exists (id={target_id})")
        else:
            conn.execute(
                "INSERT INTO targets (host, os, role, notes, discovered_by) VALUES (?, ?, ?, ?, ?)",
                (host, t.get("os", ""), t.get("role", ""), t.get("notes", ""), "operator-seed"),
            )
            conn.commit()
            target_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            print(f"  Added target {host} (id={target_id})")

        for p in t.get("ports", []):
            port_num = p if isinstance(p, int) else p.get("port")
            service = "" if isinstance(p, int) else p.get("service", "")
            try:
                conn.execute(
                    "INSERT INTO ports (target_id, port, service) VALUES (?, ?, ?)",
                    (target_id, port_num, service),
                )
            except Exception:
                pass
        conn.commit()

    # Credentials
    for c in data.get("credentials", []):
        conn.execute(
            """INSERT INTO credentials (username, secret, secret_type, domain, source, notes, discovered_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (c["username"], c.get("secret", ""), c.get("secret_type", "password"),
             c.get("domain", ""), c.get("source", "operator-provided"),
             c.get("notes", ""), "operator-seed"),
        )
        conn.commit()
        print(f"  Added credential {c.get('domain', '')}\\{c['username']}")

    # Access
    for a in data.get("access", []):
        target_id = _get_target_id(conn, a["host"])
        if not target_id:
            print(f"  Warning: target {a['host']} not found for access entry, skipping")
            continue
        conn.execute(
            """INSERT INTO access (target_id, access_type, username, privilege, method, notes, discovered_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (target_id, a.get("type", "shell"), a.get("username", ""),
             a.get("privilege", "user"), a.get("method", "operator-provided"),
             a.get("notes", ""), "operator-seed"),
        )
        conn.commit()
        print(f"  Added {a.get('type', 'shell')} access on {a['host']}")

    # Vulns
    for v in data.get("vulns", []):
        target_id = _get_target_id(conn, v["host"])
        if not target_id:
            print(f"  Warning: target {v['host']} not found for vuln entry, skipping")
            continue
        conn.execute(
            """INSERT INTO vulns (target_id, title, vuln_type, severity, endpoint, details, discovered_by)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (target_id, v["title"], v.get("vuln_type", ""), v.get("severity", "medium"),
             v.get("endpoint", ""), v.get("details", ""), "operator-seed"),
        )
        conn.commit()
        print(f"  Added vuln '{v['title']}' on {v['host']}")


def print_summary(conn):
    """Print what's in the database."""
    targets = conn.execute("SELECT COUNT(*) FROM targets").fetchone()[0]
    ports = conn.execute("SELECT COUNT(*) FROM ports").fetchone()[0]
    creds = conn.execute("SELECT COUNT(*) FROM credentials").fetchone()[0]
    access = conn.execute("SELECT COUNT(*) FROM access").fetchone()[0]
    vulns = conn.execute("SELECT COUNT(*) FROM vulns").fetchone()[0]

    print(f"\n  State summary:")
    print(f"    Targets:     {targets}")
    print(f"    Ports:       {ports}")
    print(f"    Credentials: {creds}")
    print(f"    Access:      {access}")
    print(f"    Vulns:       {vulns}")


def main():
    parser = argparse.ArgumentParser(description="Seed an engagement state database")
    parser.add_argument("--db", default="engagement/state.db", help="Path to state.db")
    parser.add_argument("--name", default="seeded-engagement", help="Engagement name")
    parser.add_argument("--mode", default="ctf", choices=["ctf", "pentest"], help="Engagement mode")
    parser.add_argument("--from", dest="seed_file", help="Load from a YAML seed file")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    is_new = not db_path.exists()
    conn = init_db(db_path)

    if is_new:
        conn.execute(
            "INSERT INTO engagement (id, name, mode) VALUES (1, ?, ?)",
            (args.name, args.mode),
        )
        conn.commit()
        print(f"\n[seed] Created {db_path} (name={args.name}, mode={args.mode})")
    else:
        print(f"\n[seed] Opened existing {db_path}")

    # YAML mode — load and exit
    if args.seed_file:
        seed_path = Path(args.seed_file)
        if not seed_path.exists():
            print(f"Error: seed file not found: {seed_path}")
            sys.exit(1)
        print(f"[seed] Loading from {seed_path}")
        load_yaml(conn, seed_path)
        print_summary(conn)
        print(f"\n[seed] Done. Run 'claude' and say 'resume engagement' to continue.")
        conn.close()
        return

    # Interactive mode
    print("[seed] Interactive mode — add targets, creds, access, vulns")
    print("[seed] Press Enter with no input to skip any field\n")

    while _yes("Add a target?"):
        add_target(conn)

    while _yes("Add a credential?", default=False):
        add_credential(conn)

    if _yes("Add an access entry? (only if you already have an active shell/session — most users skip this)", default=False):
        print("    Access = you already logged in and have a working session (SSH, WinRM, web shell, etc.)")
        print("    If you only have credentials but haven't connected yet, skip this — the orchestrator will handle login.\n")
        while True:
            add_access(conn)
            if not _yes("Add another access entry?", default=False):
                break

    while _yes("Add a vulnerability?", default=False):
        add_vuln(conn)

    print_summary(conn)
    print(f"\n[seed] Done. Run 'claude' and say 'resume engagement' to continue.")
    conn.close()


if __name__ == "__main__":
    main()
