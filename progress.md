# red-run — Session Log

## 2026-02-22 — Request Smuggling + Web Coverage Audit

### Done
- Created `skills/web/request-smuggling/SKILL.md` (570 lines)
  - Step 1: Assess architecture (front-end/back-end identification, HTTP version, connection reuse)
  - Step 2: Detect CL.TE (detection probe + timing-based)
  - Step 3: Detect TE.CL (detection probe + timing-based)
  - Step 4: Detect TE.TE (10 obfuscation variants)
  - Step 5: Exploit — request hijacking (capture victim requests, access control bypass, header injection)
  - Step 6: HTTP/2 downgrade smuggling (H2.CL, H2.TE, CRLF injection, h2c smuggling)
  - Step 7: Advanced — response desync, cache poisoning, WebSocket smuggling, connection state attacks, hop-by-hop abuse
  - Step 8: Escalate/Pivot
- Updated `web-vuln-discovery` with request smuggling detection probes and routing table (4 patterns)
- Ran comprehensive web coverage audit across all three ~/docs/ repos
  - Enumerated every web technique in PayloadsAllTheThings (60+ dirs), hacktricks/pentesting-web (120+ files), InternalAllTheThings
  - Classified each as COVERED, GAP, or OUT OF SCOPE
- Identified 7 Tier 1 (critical) gaps: IDOR, CSRF, CORS, NoSQL injection, OAuth, account takeover, race conditions
- Identified ~19 Tier 2 (important) gaps: LDAP/XPath/XSLT injection, SSI/ESI, CRLF, GraphQL, WebSocket, prototype pollution, CSTI, clickjacking, open redirect, XS-leaks, postMessage, HPP, cache poisoning, rate limit bypass, CSV injection, proxy/WAF bypass
- Expanded Phase 3 with 7 new Tier 1 skills (authorization & authentication subsection)
- Created Phase 3b for 19 Tier 2 skills (extended web skills)
- Added niche/reference-only topics to Backlog
- Added extended/backlog phase convention to CLAUDE.md

### Source Material Used
- PayloadsAllTheThings: Request Smuggling/README.md, CRLF Injection/README.md, HTTP Parameter Pollution/README.md, Web Sockets/README.md, Reverse Proxy Misconfigurations/README.md, Web Cache Deception/README.md
- HackTricks: http-request-smuggling/ (5 files), http-response-smuggling-desync.md, h2c-smuggling.md, http-connection-request-smuggling.md, http-connection-contamination.md, crlf-0d-0a.md, parameter-pollution.md, abusing-hop-by-hop-headers.md

### Decisions
- Request smuggling is a single skill covering HTTP/1.1 and HTTP/2 variants — they share detection methodology and the escalation from detection to exploitation is a single workflow
- TE.TE treated as a detection variant (obfuscation to force CL.TE or TE.CL) rather than a separate exploitation technique
- WebSocket smuggling, connection state attacks, and hop-by-hop abuse included as advanced subsections rather than separate skills — they're smuggling-adjacent and share the same architectural prerequisite
- CRLF injection gets its own Phase 3b skill (standalone header injection without smuggling context) vs. the request-smuggling skill which uses CRLF as one H2 technique
- Phase 3b keeps extended web skills visible in the plan but clearly separated from core priorities
- Backlog convention documented in CLAUDE.md so future phases follow the same pattern

### Next Steps
- Build Phase 3 Tier 1 skills: IDOR, CSRF, CORS, NoSQL injection, OAuth, account takeover, race conditions
- Update web-vuln-discovery routing for each new skill
- Final web-vuln-discovery review after all Phase 3 skills complete

## 2026-02-22 — State Management + Orchestrator

### Done
- Designed `engagement/state.md` format — compact, machine-readable engagement state snapshot
  - Sections: Targets, Credentials, Access, Vulns, Pivot Map, Blocked
  - One-liner per item, ~200 line budget, current state not history
  - Skills read on activation, write on completion
- Created `skills/orchestrator/SKILL.md` (356 lines)
  - Step 1: Scope & engagement setup (initializes scope.md, state.md, activity.md, findings.md)
  - Step 2: Recon (nmap, httpx, netexec)
  - Step 3: Attack surface mapping → routes to discovery skills
  - Step 4: Vulnerability discovery & exploitation → routes to technique skills
  - Step 5: Vulnerability chaining — reads state.md Pivot Map, chains vulns for impact
    - Info→Access, Access→Deeper Access, Lateral Movement, Privilege Escalation chains
    - Decision logic: check unexploited vulns, unchained access, untested creds, blocked items
  - Step 6: Post-exploitation evidence collection
  - Step 7: Reporting — engagement summary, routes to pentest-findings
- Added `## State Management` section to skill template
- Batch-updated all 20 web skills (6 parallel agents):
  - Added State Management section (read state.md before starting, write back on completion)
  - Added state.md update reminder in each skill's Escalate/Pivot step
  - web-vuln-discovery got discovery-specific variant (focus on new targets, record tested endpoints)
- Updated CLAUDE.md:
  - Added state.md to engagement directory structure
  - Added State Management subsection with format, rules, section table
  - Updated body structure list (now 8 items including State Management)
- Updated README.md engagement directory section with state.md
- Updated task_plan.md — checked off orchestrator, engagement logging, added state management items

### Decisions
- State.md is a snapshot, not a log — keeps it compact for re-ingestion
- ~200 line budget keeps it readable without burning context
- Orchestrator owns chaining logic — reads state.md Pivot Map to decide next actions
- Discovery skills get a slightly different State Management section (focus on tested endpoints)
- Every skill reads state.md first, writes last — ensures cross-skill continuity

### Next Steps
- `request-smuggling` — last remaining Phase 3 web skill

## 2026-02-22 — JWT Attacks Skill

### Done
- Created `skills/web/jwt-attacks/SKILL.md` (533 lines)
  - Step 1: Assess — locate JWTs, decode, identify algorithm, find public keys, note claims
  - Step 2: Algorithm None (CVE-2015-9235) — none/None/NONE/nOnE variants
  - Step 3: Null Signature (CVE-2020-28042) — strip signature, keep algorithm
  - Step 4: Brute Force Weak Secret — hashcat mode 16500, jwt_tool dictionary, jwt-secrets wordlist
  - Step 5: Key Confusion RS256→HS256 (CVE-2016-5431) — jwt_tool, manual openssl, Burp JWT Editor workflow, RSA key recovery from two tokens
  - Step 6: Header Injection — kid (path traversal to /dev/null, SQLi to force known key, command injection), jwk embedding (CVE-2018-0114), jku spoofing (attacker JWKS + URL bypass), x5u/x5c certificate injection
  - Step 7: Claim Tampering — role/admin escalation, user impersonation, expiration bypass, cross-service relay
  - Step 8: Escalate/Pivot — routes to ssrf, sql-injection-union/blind, command-injection
- Updated `web-vuln-discovery` routing table (now 363 lines):
  - Added JWT detection payloads to Step 3
  - Added JWT routing table to Step 4 (4 patterns)
  - Added JWT reference doc to Deep Reference
- Updated task_plan.md, README.md

### Source Material Used
- `~/docs/PayloadsAllTheThings/JSON Web Token/README.md`
- `~/docs/hacktricks/src/pentesting-web/hacking-jwt-json-web-tokens.md`

### Decisions
- Single `jwt-attacks` skill covers all JWT attack types since they share the same target (JWT tokens) and tools (jwt_tool, hashcat, Burp JWT Editor)
- 533 lines — slightly over the 500-line budget but JWT has many distinct attack vectors that all need embedded payloads
- OPSEC rated as low — token manipulation is client-side, brute forcing is offline

### Next Steps
- `request-smuggling` — last remaining Phase 3 web skill

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
1. ~~LFI skill~~ — done in session 8
2. Write orchestrator skill — needs special logging: creates engagement dir, initializes scope.md, maintains activity.md across skill transitions, produces summary
3. Update README.md
4. Remaining web skills: file-upload-bypass, deserialization, XXE, command-injection, JWT, request-smuggling

---

## 2026-02-22 — Engagement Logging + LFI Skill

### Done
- Designed and implemented engagement logging convention (see session above)
- Authored `lfi` skill (536 lines) — largest skill in the library, covering:
  - Basic traversal + 8 filter bypass techniques (URL encoding, double encoding, UTF-8 overlong, non-recursive stripping, null byte, path truncation, mixed separators, backslash encoding)
  - PHP wrappers: php://filter (source code extraction + bypass variants), data://, php://input, expect://, zip://, phar://
  - 8 LFI-to-RCE methods: PHP filter chain RCE (most reliable), log poisoning (Apache/Nginx/SSH/FTP/mail), session poisoning, /proc/self/environ, PHP_SESSION_UPLOAD_PROGRESS race condition, PEARCMD.php gadget, temp file race condition, PHAR deserialization
  - Platform-specific sensitive files: Linux (23 paths) + Windows (14 paths)
  - RFI section: basic, SMB-based (bypasses allow_url_include on Windows), data://
  - Engagement logging section included from the start (first skill with it baked in from creation)
- Verified web-vuln-discovery routing table already covers LFI with 3 patterns
- Updated task_plan.md and progress.md

### Source Material Used
- PayloadsAllTheThings: File Inclusion/README.md (traversal basics, filter bypass), Wrappers.md (PHP wrappers comprehensive), LFI-to-RCE.md (10+ escalation methods), Intruders/ (7,984 payload wordlists)
- HackTricks: file-inclusion/README.md (methodology, blind LFI paths, HTML-to-PDF traversal), lfi2rce-via-php-filters.md (filter chain RCE), via-php_session_upload_progress.md (race condition), phar-deserialization.md

### Decisions
- Single skill for LFI + RFI — RFI is a small section since it's disabled by default since PHP 5.2
- 8 LFI-to-RCE methods prioritized by reliability: filter chain RCE first (no file write, no race condition), then log poisoning (most common), then increasingly exotic methods
- PHP filter chain RCE gets prominent placement as the "most reliable modern LFI-to-RCE technique" — it works without allow_url_include and without file writes
- Embedded platform-specific file paths directly (37 paths) rather than referencing wordlists — users need the top targets immediately, not a 4,500-line wordlist
- Included PEARCMD.php gadget since it's common in Docker PHP images and often overlooked
- PHAR deserialization marked as PHP < 8.0 only — PHP 8.0+ removed auto-deserialization

### Next Steps
1. Continue Phase 3 web skills: command-injection or xxe next
2. Write orchestrator skill
3. Update README.md
4. Remaining web skills: file-upload-bypass, deserialization (java/php/dotnet), xxe, JWT, request-smuggling

---

## 2026-02-22 — Command Injection Skill

### Done
- Authored `command-injection` skill (486 lines) covering:
  - Injection operators: 8 Linux operators + 6 Windows operators with behavior descriptions
  - Context-aware injection: breaking out of double quotes, single quotes, backticks
  - Polyglot payloads: cross-context payloads that work regardless of quoting
  - Filter bypass — 5 categories: space bypass (${IFS}, brace expansion, tab, redirection, ANSI-C), command blacklist bypass (quote splitting, backslash, variable expansion, empty substitution), character restrictions (hex, octal, xxd, base64, env variable substrings), wildcard-based bypass (/???/??t), newline/whitespace injection
  - Blind injection: time-based (sleep, ping), DNS exfiltration (host, dig, curl, wget), file-based (write to webroot)
  - Argument injection: curl, wget, ssh, tar, find, rsync, sendmail flag injection + fullwidth Unicode bypass
  - Windows-specific: case insensitivity, variable substring, PowerShell, caret escaping
  - commix automation
- Verified web-vuln-discovery routing table already covers command injection with 3 patterns
- Updated task_plan.md and progress.md

### Source Material Used
- PayloadsAllTheThings: Command Injection/README.md (operators, bypass, polyglots, argument injection, blind), Intruder/ (450+ payload wordlists)
- HackTricks: command-injection.md (PHP/Node.js patterns, real-world examples), bypass-bash-restrictions/README.md (extensive filter bypass)

### Decisions
- Single skill covering both Linux and Windows — operators overlap significantly, filter bypass is platform-specific but fits in subsections
- Argument injection included as Step 5 — often overlooked but critical when shell metacharacters are properly escaped
- Polyglot payloads included because real-world injection context is often unknown
- DNS exfiltration highlighted as faster alternative to time-based for blind injection
- Noted `%0a` (newline) as the "most commonly missed by filters" operator — useful tactical advice

### Next Steps
1. Update README.md (engagement logging + current skill inventory)
2. Continue Phase 3 web skills: xxe or file-upload-bypass next
3. Write orchestrator skill
4. Remaining: file-upload-bypass, deserialization (java/php/dotnet), xxe, JWT, request-smuggling

---

## 2026-02-22 — XXE Skill

### Done
- Authored `xxe` skill (466 lines after trimming from 665) covering:
  - Classic XXE: basic file read (Linux/Windows), PHP wrappers (filter base64, expect RCE), Java directory listing, useful file targets
  - XXE to SSRF: internal resource access, AWS cloud metadata (IMDSv1), NTLM hash capture via UNC path
  - Blind/OOB XXE: detection ping (general + parameter entity), external DTD exfiltration (HTTP), PHP base64 OOB, FTP exfiltration (multi-line files), xxeserv/230-OOB tooling
  - Error-based XXE: remote DTD error technique, local/system DTD (fonts.dtd, docbookx.dtd, cim20.dtd), dtd-finder for injectable DTD discovery
  - XInclude: for when DOCTYPE is not controllable
  - File format XXE: SVG upload (reflected + OOB), DOCX/XLSX/PPTX injection (extract/edit/repackage workflow), SOAP CDATA wrapping, RSS/Atom feeds, oxml_xxe tool
  - WAF/filter bypass: UTF-16/UTF-7 encoding with BOM reference, HTML numeric entities, Content-Type switching (JSON→XML), PUBLIC keyword bypass
  - Parser-specific notes: PHP libxml2 defaults, Java DocumentBuilder (vulnerable by default), Python lxml, .NET XmlReader/XmlDocument version behavior
  - XXEinjector, xxeserv, oxml_xxe tool references
- Verified web-vuln-discovery routing table already covers XXE with 3 patterns (lines 256-262)
- Updated task_plan.md, progress.md, README.md

### Source Material Used
- PayloadsAllTheThings: XXE Injection/README.md (classic, blind, OOB, error-based, local DTD, XInclude, PHP/Java techniques, SVG, XLSX, SOAP), Files/ (example payloads), Intruders/ (XXE_Fuzzing.txt, xml-attacks.txt)
- HackTricks: xxe-xee-xml-external-entity.md (Java XMLDecoder RCE, jar: protocol, lxml bypass, XLIFF, JMF SSRF, SAML surface, Windows local DTD)

### Decisions
- 665 lines — largest skill in the library. XXE has more distinct attack categories than any other technique: classic, blind OOB (HTTP + FTP), error-based (remote + local DTD), XInclude, 5 file formats, 4 encoding bypasses
- Error-based via local DTD gets prominent coverage because it's the only option when egress is blocked — included 3 specific DTDs (fonts.dtd, docbookx.dtd, cim20.dtd) with ready-to-use payloads
- FTP exfiltration highlighted for Java specifically because HTTP-based OOB breaks on newlines in Java
- XInclude separated as its own step because it's conceptually different (no DOCTYPE control)
- Excluded Billion Laughs DoS — destructive, against project principles
- Excluded XSLT exploitation — different enough to warrant its own skill if needed
- Excluded Java XMLDecoder — full deserialization, better suited for deserialization-java skill

### Next Steps
1. Continue Phase 3 web skills: file-upload-bypass or jwt-attacks next
2. Write orchestrator skill
3. Remaining: file-upload-bypass, deserialization (java/php/dotnet), JWT, request-smuggling

## 2026-02-22 — File Upload Bypass Skill

### Done
- Created `skills/web/file-upload-bypass/SKILL.md` (506 lines)
- 8 steps: Assess → Extension Bypass → Content-Type & Magic Byte → Server Config Exploitation → Image Polyglots & Metadata → Archive & Indirect → Webshell Payloads → Escalate/Pivot
- Updated `web-vuln-discovery` routing table with config file upload pattern
- Updated task_plan.md, README.md

### Source Material
- PayloadsAllTheThings: Upload Insecure Files (extensions, MIME types, .htaccess, web.config, polyglot generators, ImageMagick CVEs, ZIP traversal)
- HackTricks: file-upload (magic bytes, race conditions, path traversal, filename injection)

### Coverage
- **Extension bypass**: alternative extensions per language (PHP/ASP/JSP/CFM/Perl), double extensions, null byte, case variation, special characters (space/newline/dot/slash), NTFS ADS, filename length overflow, RTLO
- **Content-Type & magic bytes**: MIME manipulation, GIF/JPEG/PNG/PDF signatures, combined bypass technique
- **Server config**: .htaccess (AddType + self-contained shell), web.config (handler registration + embedded ASP), uWSGI .ini (exec/http magic operators)
- **Image polyglots**: EXIF injection via exiftool, simple append, PLTE chunk and GIF color table encoding (described with ~/docs/ reference to generator scripts)
- **Archive/indirect**: ZIP path traversal (Python script), symlink technique, filename injection (SQLi/XSS/CMDi/path traversal in uploaded names), race conditions, ImageMagick CVE-2022-44268 + CVE-2016-3714
- **Webshell payloads**: PHP (standard/minimal/blocked alternatives), ASP, ASPX, JSP — one-liner format

### Decisions
- Kept as single skill (same rationale as XXE — techniques are tried in a progressive order, not identified at discovery)
- Trimmed polyglot image generator scripts to descriptions + ~/docs/ references for actual code (saves ~15 lines, generators are multi-file)
- web.config condensed to essential handler registration + embedded ASP (full requestFiltering referenced via ~/docs/)
- Race conditions described as technique rather than full Python script — testers use Burp turbo-intruder in practice
- Included ImageMagick CVEs because they're common in upload-heavy apps (file read + RCE)
- Webshell payloads in single fenced block per language to keep compact

### Next Steps
1. Continue Phase 3 web skills: deserialization or JWT attacks next
2. Write orchestrator skill
3. Remaining: deserialization (java/php/dotnet), JWT, request-smuggling

---

## 2026-02-22 — Deserialization Skills (Java/PHP/.NET)

### Done
- Authored 3 deserialization skills:
  - `deserialization-java` (404 lines) — ysoserial gadget chains (CommonsCollections 1-7, CommonsBeanutils1, URLDNS for blind, ROME, Groovy1), Runtime.exec() workarounds (bash brace encoding, ysoserial-modified, download-and-execute), JNDI injection via marshalsec, Log4Shell CVE-2021-44228 (detection payloads, 4 WAF bypass variants, data exfiltration, RCE via LDAP referral + deserialization gadgets for modern JDK), JSF ViewState (MyFaces default keys), framework-specific (WebLogic T3, JBoss invoker servlets, Jenkins CLI)
  - `deserialization-php` (365 lines) — magic methods table (__wakeup through __debugInfo), basic object injection with property modification, type juggling via deserialization (boolean true bypass, magic hash collisions), private/protected property encoding with null bytes, PHPGGC framework chains (Monolog/Laravel/Symfony/Guzzle/SwiftMailer/Doctrine/WordPress/CakePHP/Yii), Laravel APP_KEY exploitation (crypto-killer), phar:// deserialization (metadata auto-unserialize, JPEG/GIF/PNG polyglots, PHPGGC phar output), autoload exploitation (class name to file path mapping, cross-webapp gadget loading)
  - `deserialization-dotnet` (408 lines) — dangerous formatters table (BinaryFormatter/LosFormatter/ObjectStateFormatter/SoapFormatter/NetDataContractSerializer/JSON.NET/JavaScriptSerializer/XmlSerializer/DataContractSerializer), ViewState attacks (Blacklist3r/BadSecrets for known machine keys, ysoserial.exe ViewState plugin with signing/encryption, machine key format), JSON.NET TypeNameHandling exploitation (ObjectDataProvider RCE payload, WindowsIdentity bridge gadget), BinaryFormatter/SoapFormatter/NetDataContractSerializer ysoserial.net commands, .NET Remoting exploitation, framework-specific (SharePoint CVE-2025-53770, Sitecore CVE-2025-53690, Telerik CVE-2019-18935), blind detection (time-based, DNS, file write)
- Updated `web-vuln-discovery`:
  - Added deserialization test payloads to Step 3 (Java rO0AB, PHP O: prefix, .NET AAEAAAD)
  - Added deserialization routing table to Step 4 (4 patterns routing to 3 skills)
  - Added deserialization reference docs to Deep Reference section
- Updated task_plan.md, README.md
- Added global tool prerequisites list to backlog (per user request — do last after all skills written)

### Source Material Used
- PayloadsAllTheThings: Insecure Deserialization/Java.md (ysoserial chains, JNDI, JSF ViewState), PHP.md (magic methods, POP chains, PHPGGC, type juggling, Laravel), DotNET.md (formatters, ysoserial.net, ViewState)
- HackTricks: deserialization/ directory (Java transformers, JNDI/Log4Shell, SignedObject, JSF ViewState, PHP autoload classes, phar deserialization, .NET ObjectDataProvider/JSON.NET)
- Web research for .NET: ysoserial.net gadget matrix, ViewState exploitation, JSON.NET TypeNameHandling, .NET Remoting, SharePoint/Sitecore/Telerik CVEs

### Decisions
- Three separate skills (Java/PHP/.NET) rather than one monolithic deserialization skill — the tools, payloads, and exploitation chains are completely distinct per language
- Java skill includes Log4Shell as a subsection of JNDI injection — it's the most common JNDI deserialization vector and testers encounter it constantly
- PHP skill includes type juggling — it's a natural companion to deserialization since both exploit unserialize() entry points
- .NET skill leads with ViewState — it's the most common .NET deserialization attack surface in practice
- All three skills ~400 lines (well under 500 budget) — deserialization skills don't need as many embedded payloads since the tools (ysoserial, PHPGGC, ysoserial.net) generate them
- Discovery routing includes error message detection as a 4th pattern — deserialization errors often reveal the formatter/language

### Next Steps
1. Continue Phase 3 web skills: JWT attacks next, then request smuggling
2. Write orchestrator skill
3. Global tool prerequisites list (backlog — after all skills complete)
