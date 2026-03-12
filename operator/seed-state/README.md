# seed-state

Pre-populate an engagement state database with operator-known information
(targets, ports, credentials, access, vulnerabilities). The orchestrator's
resume flow picks up the seeded state automatically.

## Usage

Run from the project root (`red-run/`):

```bash
# Interactive mode
python3 operator/seed-state/seed.py

# From a YAML seed file
python3 operator/seed-state/seed.py --from path/to/seed.yaml

# Custom database path and engagement name
python3 operator/seed-state/seed.py --db engagement/state.db --name my-engagement --mode pentest
```

Then launch Claude Code and say `resume engagement`.

## Seed File Format

```yaml
targets:
  - host: 10.10.10.5
    os: windows
    role: dc
    ports:
      - 445
      - 5985
      - port: 88
        service: kerberos
      - port: 389
        service: ldap

credentials:
  - username: administrator
    secret: Password123
    secret_type: password
    domain: MEGACORP
    source: client-provided

access:
  - host: 10.10.10.5
    type: winrm
    username: administrator
    privilege: admin
    method: client-provided

vulns:
  - host: 10.10.10.5
    title: Weak admin password
    vuln_type: credential
    severity: high
    details: Default password on administrator account
```

Ports can be integers (just the port number) or objects with `port` and
`service` fields. All fields except `host` (targets), `username`
(credentials), `host`+`title` (vulns), and `host` (access) are optional.

## How It Works

The script imports `schema.py` from `tools/state-server/` and uses the same
`init_db()` function to create and migrate the database. Records are inserted
with `discovered_by: "operator-seed"` so the orchestrator can distinguish
operator-provided data from agent discoveries.

## Prerequisites

- Python 3.10+
- PyYAML (only for `--from` mode): `pip install pyyaml`
- No other dependencies — uses the state-server's schema directly
