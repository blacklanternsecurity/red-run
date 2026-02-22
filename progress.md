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

---

## 2026-02-21 — Web Skills Session 1

### Decisions
- Skills split by **technique**, not by DB engine or technology
- DB/engine variants go as subsections within each technique skill
- Added a **discovery/triage skill** (`web-vuln-discovery`) as the entry point — fuzzes for injection points, analyzes responses, and routes to the correct technique skill via a decision tree
- Phase 3 expanded from 11 high-level items to 21 specific skills

### Done
- Authored `web-vuln-discovery` — content discovery (ffuf), parameter discovery (arjun, paramspider), polyglot injection testing, full decision tree covering SQLi, SSTI, XSS, SSRF, command injection, LFI, XXE, file upload with response pattern → skill routing
- Authored `sql-injection-union` — column counting (ORDER BY, UNION NULL), per-DB extraction (MySQL, MSSQL, PostgreSQL, Oracle, SQLite), DIOS payloads, info_schema alternatives, WAF bypass, sqlmap automation
- Authored `sql-injection-error` — EXTRACTVALUE/UPDATEXML/GTID_SUBSET/EXP/FLOOR (MySQL), CONVERT/CAST + alternative functions (MSSQL), CAST + XML helpers (PostgreSQL), utl_inaddr/CTXSYS/XMLType (Oracle), output pagination for truncated errors
- Authored `sql-injection-blind` — boolean-based (binary search, LIKE/REGEXP alternatives), time-based (SLEEP/WAITFOR/pg_sleep/DBMS_PIPE/RANDOMBLOB), OOB exfil (DNS via LOAD_FILE, xp_dirtree, COPY TO PROGRAM, UTL_HTTP), per-DB for all techniques

### Status
- 4 skills written, pending review
- Next up: `sql-injection-stacked`, then XSS skills (reflected, stored, DOM)

### Source material used
- PayloadsAllTheThings: SQL Injection/ (all 10 files), Hidden Parameters/, Server Side Template Injection/
- HackTricks: web-vulnerabilities-methodology.md, timing-attacks.md, parameter-pollution.md, sql-injection/
- InternalAllTheThings: databases/ (post-exploitation reference)
