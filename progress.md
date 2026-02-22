# red-run — Session Log

## 2026-02-21 — Bootstrap

### Done
- Initialized repo at `~/claude/red-run`
- Surveyed all three reference repos:
  - `~/docs/InternalAllTheThings` — internal/AD-focused, 9 top-level categories
  - `~/docs/PayloadsAllTheThings` — web-focused, 40+ injection/vuln directories
  - `~/docs/hacktricks` — broadest scope, 700+ files across 20 categories
- Built unified topic taxonomy (see `findings.md`)
- Categorized all topics into 8 skill groups
- Created phased task plan (`task_plan.md`)
- Designed skill directory layout and file format
- Created template skill at `skills/_template/skill.md`

### Observations
- AD coverage in InternalAllTheThings is exceptional — 15 individual ADCS ESC files, full Kerberos delegation chain, modern tooling (Certipy, NetExec, bloodyAD)
- Web coverage in PayloadsAllTheThings is the deepest — SQL injection alone has 10 files across 8 DB engines
- HackTricks has the broadest scope (binary exploitation, macOS, mobile, AI security, forensics) but some sections are thin
- Cloud content is split: InternalAllTheThings has Azure (144K) and AWS (80K); HackTricks main repo has none (lives in HackTricks Cloud, separate repo)
- Notable gaps across all repos: GCP, wireless, physical security
