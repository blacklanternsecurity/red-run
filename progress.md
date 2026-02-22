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

### Done
- Authored 4 v1 reference skills (static `skill.md` format):
  - `web-vuln-discovery` — content discovery, parameter fuzzing, decision tree
  - `sql-injection-union` — UNION-based extraction, 5 DB engines
  - `sql-injection-error` — error-based extraction, 4 DB engines
  - `sql-injection-blind` — boolean, time-based, OOB blind extraction

### Decisions
- Skills split by **technique**, not by DB engine or technology
- DB/engine variants go as subsections within each technique skill
- Discovery/triage skills as entry points with decision trees routing to technique skills

---

## 2026-02-22 — Web Skills Session 2 + Architecture Redesign

### Done
- Authored `sql-injection-stacked` on `skills/web-sqli` branch (stacked queries + second-order injection)
- SQLi v1 skill set complete (4 techniques: union, error, blind, stacked)

### Architecture Redesign (v1 → v2)

Decided to restructure from static reference docs to Claude Code native skills:

**Problem with v1:** Static `skill.md` reference docs required manual invocation (`Read ~/claude/red-run/skills/...`). No auto-triggering, no guided/autonomous modes, no orchestration. A separate reference layer duplicated content from `~/docs/` and would go stale.

**v2 architecture:**
- **SKILL.md** is the only artifact per technique (Claude Code native format)
- Skills **auto-trigger** via pushy `description` field — no slash commands needed
- Two **modes**: guided (interactive, default) and autonomous (end-to-end)
- **Orchestrator** skill: takes a target → recon → route to discovery → route to techniques → report
- **Discovery** skills: identify vulnerabilities, route to technique skills via decision tree
- **Technique** skills: exploit specific vuln classes with embedded critical payloads
- `~/docs/` is a **dependency** (not copied) for deep reference content
- Skills install **globally** to `~/.claude/skills/red-run-*/` via `install.sh` (symlinks)

### Created
- `skills/_template/SKILL.md` — new canonical template with mode handling, routing, deep reference sections
- `install.sh` — symlink-based installer with `red-run-` prefix and `~/docs` dependency check
- `uninstall.sh` — cleanup script
- Updated `CLAUDE.md` with new architecture, format, install workflow
- Updated `task_plan.md` — v2 architecture tasks, conversion checklist

### Status
- Infrastructure ready (template, install scripts)
- 5 existing v1 skills need conversion to SKILL.md format
- All remaining web skills (XSS, SSTI, SSRF, etc.) to be authored in SKILL.md format from scratch
- Orchestrator skill still needs to be written

### Engagement Logging (planned)

Skills need to track what happens during an engagement. Rough design:

- **Engagement directory**: Created by orchestrator (or user) at engagement start. Probably `./engagement/` or user-specified path. Contains:
  - `activity.md` — chronological log of all actions taken (recon scans, injection tests, exploitation attempts). Each entry timestamped. Append-only.
  - `findings.md` — confirmed vulnerabilities. Each finding gets: title, severity, affected host/endpoint, description, reproduction steps, evidence (terminal output, screenshots), impact.
  - `evidence/` — directory for screenshots, saved responses, captured credentials, etc.
  - `scope.md` — target scope, credentials, constraints (written at engagement start)
- **Every skill** logs to activity.md when it runs (what was tried, what worked, what didn't)
- **Successful exploits** get a full finding entry with reproduction steps and evidence
- **Orchestrator** initializes the engagement dir, maintains the activity log, and produces a summary at the end
- This integrates with the existing `pentest-findings` skill for formal finding writeups

### Next Steps
1. ~~Convert 5 existing skills~~ — done in session 3
2. Write orchestrator skill (including engagement dir initialization)
3. Design engagement logging conventions and bake into template
4. Continue Phase 3 web skills in SKILL.md format (XSS next)
5. ~~Note: `sql-injection-stacked` is on `skills/web-sqli` branch~~ — created fresh on `arch/skill-format-v2`

---

## 2026-02-22 — Skill Conversion Session (v1 → v2)

### Done
- Converted all 5 existing v1 skills to SKILL.md format:
  - `sql-injection-error` (240 lines) — rewrote prototype, now self-contained with embedded payloads
  - `sql-injection-union` (287 lines) — full 5-DB coverage, DIOS, WAF bypass
  - `sql-injection-blind` (302 lines) — boolean, time-based, OOB for all DBs
  - `sql-injection-stacked` (306 lines) — created fresh from v1 content on `skills/web-sqli` branch
  - `web-vuln-discovery` (299 lines) — content/param discovery, full routing decision tree
- Deleted all 5 old `skill.md` files and old `skills/_template/skill.md`
- Total: 1,434 lines of SKILL.md content across 5 skills

### Conversion Pattern Applied
Each v1 skill.md was restructured into v2 SKILL.md with:
- **Pushy description**: explicit trigger phrases, OPSEC level, tools, negative conditions
- **Mode section**: guided (default) vs autonomous with specific behavioral guidance
- **Step-based flow**: Assess → Confirm → Exploit → Post-Exploit → Escalate/Pivot
- **Embedded payloads**: top 2-3 functions per DBMS (80% coverage)
- **Deep Reference**: `~/docs/` paths for WAF bypass, edge cases, long tail
- **Inter-skill routing**: bold skill names with context to pass along
- **OPSEC notes**: cleanup, detection signatures, log artifacts
- **Troubleshooting**: preserved from v1 with WAF bypass and sqlmap automation

### Decisions
- Created `sql-injection-stacked` fresh on `arch/skill-format-v2` rather than cherry-picking from `skills/web-sqli` — cleaner than merging branches, and the v2 format is significantly different anyway
- Updated Burp Collaborator domain references from `burpcollaborator.net` to `oastify.com` (current Burp Suite domain)
- Kept OPSEC notes and detection info as brief sections rather than full Detection/Cleanup headings — matches template structure

### Next Steps
1. ~~Start new web skills: XSS~~ — done in this session
2. Write orchestrator skill at `skills/orchestrator/SKILL.md`
3. Design engagement logging conventions and integrate into template
4. Update README.md for v2 architecture
5. Continue Phase 3 web skills: SSTI (jinja2, twig, freemarker) next
6. `skills/web-sqli` branch can be closed/deleted — its content has been superseded

---

## 2026-02-22 — XSS Skills

### Done
- Authored 3 XSS skills fresh in SKILL.md format:
  - `xss-reflected` (343 lines) — reflection context identification, basic → filter bypass → WAF bypass → CSP bypass progression, impact demonstration, AngularJS/SVG/Markdown contexts
  - `xss-stored` (282 lines) — stored + blind XSS, XSS Hunter/callback setup, self-XSS escalation, PDF generation XSS, SVG upload XSS
  - `xss-dom` (355 lines) — comprehensive sources/sinks reference, 6 exploitation examples (hash, param, eval, postMessage, window.name, jQuery), DOM clobbering, DOMPurify bypass, tooling (DOM Invader, domloggerpp)
- Verified web-vuln-discovery routing table already covers all 3 XSS skills
- Total XSS content: 980 lines

### Source Material Used
- PayloadsAllTheThings: README.md, Filter Bypass, Common WAF Bypass, CSP Bypass, Angular XSS
- HackTricks: dom-xss.md (sources/sinks tables, DOM clobbering, window.name abuse, template literal innerHTML gaps)

### Decisions
- Reflected skill covers CSP bypass (JSONP, data: URI, base tag) since CSP is the main obstacle to reflected XSS exploitation
- Stored skill covers blind XSS (separate injection and trigger contexts) since blind is just a variant of stored
- DOM skill is the most detailed (355 lines) because DOM XSS requires understanding JavaScript data flow, not just payload injection
- Used `console.log()` convention for stored XSS testing (avoids alert popup fatigue)

### Next Steps
1. ~~SSTI skills: jinja2, twig, freemarker~~ — done in session 5
2. Orchestrator skill
3. Engagement logging
4. Remaining web skills: SSRF, LFI, file-upload-bypass, deserialization, XXE, command-injection, JWT, request-smuggling

---

## 2026-02-22 — SSTI Skills

### Done
- Authored 3 SSTI skills fresh in SKILL.md format:
  - `ssti-jinja2` (345 lines) — Jinja2 + Mako + Tornado + Django. Covers: lipsum/cycler/joiner/namespace context-free payloads, MRO chain with warning loop, filter bypass (underscore, dot, brackets, quotes, `{{}}`), blind/error/time/OOB variants, Fenjing for automated WAF bypass
  - `ssti-twig` (322 lines) — Twig + Smarty + Blade + Latte. Covers: filter/map/sort/reduce RCE (modern Twig), registerUndefinedFilterCallback (Twig <= 1.19), call_user_func, error-based + boolean-based + CVE-2022-23614 sandbox bypass, obfuscation via block+charset
  - `ssti-freemarker` (382 lines) — Freemarker + Velocity + SpEL + Thymeleaf + Pebble + Groovy + Java EL + Jinjava. Covers: Execute class, sandbox bypass (< 2.3.30), Velocity reflection chains, SpEL T() operator + character-by-character bypass, Thymeleaf expression inlining + preprocessing, Pebble old/new version payloads, XWiki CVE-2025-24893
- Verified web-vuln-discovery routing table already covers all 3 SSTI skills with Jinja2/Twig disambiguation logic
- Total SSTI content: 1,049 lines

### Source Material Used
- PayloadsAllTheThings: Python.md (Jinja2 filter bypass, Mako context-free chains, Tornado), PHP.md (Twig code execution, Smarty, obfuscation), Java.md (Freemarker, Velocity, Pebble, SpEL, Groovy, Jinjava), README.md (universal detection, polyglot, methodology)
- HackTricks: ssti-server-side-template-injection/README.md (all engines overview, XWiki CVE-2025-24893, Thymeleaf, Spring View Manipulation), jinja2-ssti.md (filter bypass, sandbox escape, WAF bypass with Fenjing)

### Decisions
- Jinja2 skill covers all Python engines (Mako, Tornado, Django) since Mako/Tornado are simple (direct code execution, no sandbox) and Django is limited (info disclosure only)
- Twig skill covers all PHP engines (Smarty, Blade, Latte) since Smarty/Latte have simple direct execution and Blade exploitation requires misconfiguration
- Freemarker skill is the largest (382 lines) because Java has the most diverse engine landscape — 8 engines with distinct syntaxes and exploitation chains
- Included blind/error-based/boolean-based SSTI variants for each engine family (per the reference material's 2026 research on "Successful Errors" techniques)
- Included real-world CVE targets (XWiki CVE-2025-24893) to provide actionable context

### Next Steps
1. ~~Continue Phase 3 web skills: SSRF next~~ — done in this session
2. Write orchestrator skill
3. Design engagement logging conventions
4. Remaining web skills: LFI, file-upload-bypass, deserialization, XXE, command-injection, JWT, request-smuggling

---

## 2026-02-22 — SSRF Skill

### Done
- Authored `ssrf` skill (503 lines) covering:
  - Basic SSRF: localhost access, internal network scanning, file:// protocol
  - Filter bypass: IPv6, domain redirects, CIDR, IP encoding (decimal/hex/octal/mixed), URL encoding, URL parsing discrepancy, HTTP redirects, DNS rebinding, PHP filter_var(), JAR scheme, enclosed alphanumeric
  - Cloud metadata: AWS (IMDSv1, IMDSv2, ECS, Lambda, Elastic Beanstalk), GCP (with header bypass via gopher), Azure, Digital Ocean, Oracle, Alibaba, Hetzner, Kubernetes ETCD, Docker, Rancher
  - Protocol exploitation: gopher:// (Redis webshell, FastCGI RCE, MySQL, SMTP relay, Zabbix), dict:// (Redis), file://
  - Blind SSRF: OOB detection, time-based, blind SSRF chains (Elasticsearch, Jenkins, Docker, Redis, Consul, Solr), upgrade to XSS via SVG
  - Escalation paths: AWS credentials → S3/IAM, Redis → webshell, FastCGI → RCE, Docker API → container escape
- Verified web-vuln-discovery routing table already covers SSRF with 3 response patterns (localhost content, blind callback, cloud metadata)

### Source Material Used
- PayloadsAllTheThings: README.md (filter bypass, URL schemes, blind exploitation), SSRF-Cloud-Instances.md (AWS/GCP/Azure/DO/Oracle/Alibaba/Hetzner/k8s/Docker), SSRF-Advanced-Exploitation.md (Redis, FastCGI, MySQL, SMTP, WSGI, Zabbix, DNS AXFR via gopher)
- HackTricks: ssrf-server-side-request-forgery/README.md (methodology overview), cloud-ssrf.md, url-format-bypass.md

### Decisions
- Single skill for all SSRF variants (basic, blind, cloud) since they share the same injection point and bypass techniques — splitting by cloud provider would fragment the workflow
- 503 lines — largest skill so far due to the breadth of bypass techniques and cloud provider coverage
- Included both gopher:// and dict:// exploitation paths for Redis since they have different capabilities (gopher is more flexible, dict is simpler)
- Included r3dir.me as a serverless redirect alternative to hosting your own redirector

### Next Steps
1. ~~Design engagement logging conventions~~ — done in session 7
2. LFI skill next
3. Write orchestrator skill (including engagement dir initialization)
4. Remaining web skills: file-upload-bypass, deserialization, XXE, command-injection, JWT, request-smuggling

---

## 2026-02-22 — Engagement Logging Conventions

### Done
- Designed engagement logging standard and implemented across all skills
- Updated `skills/_template/SKILL.md` — added `## Engagement Logging` section between Mode and Prerequisites
- Updated `CLAUDE.md` — added `### Engagement Logging` under Architecture with full directory structure, behavior rules, and orchestrator responsibilities; updated body structure list (now 7 items)
- Batch-updated all 11 existing SKILL.md files with per-skill Engagement Logging sections:
  - Each section is ~15 lines with skill-specific milestone examples and evidence filename examples
  - Consistent format: auto-detect `./engagement/`, guided asks / autonomous creates, milestone-based activity logging, numbered findings, evidence to `evidence/`
- Updated `task_plan.md` — checked off 5/6 engagement logging tasks (orchestrator integration remains)

### Design Decisions
- **Per-skill section** over CLAUDE.md-only or hybrid — self-contained, explicit, Claude follows it reliably even deep in a skill workflow
- **Auto-detect + offer to create** — skills check for `./engagement/`, guided mode asks, autonomous mode creates. No engagement dir = no logging (graceful degradation)
- **Milestone-based logging** — log at significant events (test confirmed, data extracted, finding discovered, skill pivot), not every command. Keeps activity.md useful without being overwhelming.
- **Light findings format** — numbered entries with severity, target, technique, impact, evidence path, repro command. Formal report-quality writeups come from the `pentest-findings` skill separately.
- **Activity log format**: `### [HH:MM] skill-name → target` with bullet points. Date headers (`## YYYY-MM-DD`) group entries by day.
- **Evidence filenames**: descriptive, skill-prefixed (e.g., `sqli-union-schema-dump.txt`, `ssrf-aws-credentials.json`)
- **Section placement**: after Mode, before Prerequisites — behavioral directive that affects all subsequent steps

### Engagement Directory Structure
```
engagement/
├── scope.md          # Target scope, credentials, rules of engagement
├── activity.md       # Chronological action log (append-only)
├── findings.md       # Confirmed vulnerabilities (working tracker)
└── evidence/         # Saved output, responses, dumps
```

### Next Steps
1. LFI skill next (will include engagement logging from the start)
2. Write orchestrator skill — needs special logging: creates engagement dir, initializes scope.md, maintains activity.md across skill transitions, produces summary
3. Update README.md
4. Remaining web skills: file-upload-bypass, deserialization, XXE, command-injection, JWT, request-smuggling
