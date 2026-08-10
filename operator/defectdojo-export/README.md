# DefectDojo export

Pushes red-run findings into [DefectDojo](https://github.com/DefectDojo/django-DefectDojo)
for remediation tracking.

```bash
# Inspect first — writes the exact payload --push would send, no network
python3 operator/defectdojo-export/export.py --out /tmp/dd.json

# Then push
python3 operator/defectdojo-export/export.py --push \
    --url https://defectdojo.example.org \
    --token "$DD_TOKEN" \
    --product "Acme Corp — staging" \
    --engagement "2026-Q1 external pentest"
```

`--db` defaults to `engagement/state.db`. The push uses
`/api/v2/import-scan/` with `scan_type=Generic Findings Import` and
`auto_create_context=true`, so the product and engagement are created if absent.

## What is exported

`vulns` become Findings. `unique_id_from_tool` is set to `red-run-vuln-<id>`,
which is stable across runs — re-exporting updates existing findings rather than
duplicating them.

| red-run | DefectDojo |
|---|---|
| `title` · `details` | `title` · `description` |
| `severity` | `severity` (the five levels map exactly) |
| `cvss_vector` | `cvssv3`, prefixed `CVSS:3.1/` if not already |
| `cwe` | `cwe` (integer part only) |
| `evidence_path` | `file_path` |
| `vuln_type` | `vuln_id_from_tool` |
| target `hostname`/`ip` | `endpoints` |
| `status == 'actioned'` | `verified: true` |
| `status == 'blocked'` | `active: false` |

`status='actioned'` is the only red-run state that means the finding was
actually demonstrated, so it is the only one mapped to `verified`.

Info-severity findings are **skipped by default**. In red-run they are mostly
refuted candidates and scope notes — importing them makes controls that held
look like open issues. `--include-info` overrides this.

## What is not exported, and why it matters

DefectDojo models vulnerabilities. red-run models an engagement. Five tables
have no counterpart and are dropped:

- **`blocked`** — every technique attempted and refuted, with its reasoning.
  This is the largest loss. It is what lets a reader tell "secure" apart from
  "not looked at", and there is nowhere in DefectDojo to put it.
- **`access`, `credentials`, `credential_access`, `pivot_map`** — the access
  chain: how the tester got in and what each step unlocked.

The provenance links (`via_vuln_id`, `via_access_id`, `via_credential_id`) are
not lost outright — they are flattened into each finding's description under a
**Provenance** heading, since DefectDojo cannot represent the graph itself.

Every run prints a count of what it left behind. The omission is deliberate and
visible rather than silent:

```
not exported — DefectDojo has no model for these:
    24  blocked (techniques attempted and refuted)
     8  credentials
```

**The DefectDojo export is not a substitute for the engagement report.** It
carries the findings, not the narrative. Deliver both.

## Backfilling `cvss_vector` and `cwe`

Both are columns as of schema v23. Engagements started before that recorded
CVSS and CWE as free text inside `details`, and those rows export without the
`cvssv3`/`cwe` fields until the columns are populated — via `update_vuln`, or by
whatever produced the scores in the first place.

## Requirements

Python 3.11+, standard library only. No dependencies, no venv.
