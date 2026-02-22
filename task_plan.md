# red-run — Skill Library Task Plan

Claude Code skills for penetration testing and CTF work. Skills are SKILL.md files that auto-trigger based on conversation context, support guided and autonomous modes, and install globally to `~/.claude/skills/`. Reference material lives in `~/docs/` (PayloadsAllTheThings, InternalAllTheThings, HackTricks).

## Phase 1: Survey & Taxonomy — COMPLETE

- [x] Survey InternalAllTheThings
- [x] Survey PayloadsAllTheThings
- [x] Survey HackTricks
- [x] Build unified topic taxonomy across all three repos
- [x] Categorize topics into skill groups
- [x] Document findings in `findings.md`

## Phase 2: Architecture — COMPLETE

### v1 (replaced)
- [x] Defined static reference doc format (`skill.md`)
- [x] Created template and 5 SQLi reference docs

### v2 (current)
- [x] Create new template at `skills/_template/SKILL.md`
- [x] Create `install.sh` (symlinks to `~/.claude/skills/red-run-*/`)
- [x] Create `uninstall.sh`
- [x] Update CLAUDE.md
- [ ] Create orchestrator at `skills/orchestrator/SKILL.md`
- [x] Convert 5 existing skill.md files to SKILL.md format
- [x] Delete old skill.md files and old template
- [x] Update README.md — v2 architecture, skill inventory, engagement logging, installation

### Engagement logging
- [x] Define engagement directory structure and file conventions (activity log, findings, evidence) — `./engagement/` with `activity.md`, `findings.md`, `scope.md`, `evidence/`
- [x] Build engagement logging into the SKILL.md template — `## Engagement Logging` section after Mode, auto-detect + offer to create
- [ ] Build engagement logging into the orchestrator — initialize engagement dir, maintain activity log, track findings
- [x] Define evidence format: milestone-based activity entries, numbered findings with severity/target/technique/impact/evidence/repro
- [x] Document conventions in CLAUDE.md — `### Engagement Logging` under Architecture
- [x] Batch update all 11 existing skills with Engagement Logging section

## Phase 3: Core Skills — Web Application (CURRENT)

Split strategy: by **technique** (not by DB engine). DB/engine variants as subsections. Discovery skill routes to techniques via decision tree.

### SQL Injection
- [x] `sql-injection-union` — UNION-based, per-DB variants (converted)
- [x] `sql-injection-error` — error-based, per-DB variants (converted)
- [x] `sql-injection-blind` — boolean, time-based, OOB (converted)
- [x] `sql-injection-stacked` — stacked queries, second-order (converted)

### XSS
- [x] `xss-reflected` — reflected + filter/WAF/CSP bypass
- [x] `xss-stored` — stored + blind XSS
- [x] `xss-dom` — DOM-based (sources, sinks, postMessage, DOM clobbering)

### SSTI
- [x] `ssti-jinja2` — Jinja2/Python (+ Mako, Tornado, Django)
- [x] `ssti-twig` — Twig/PHP (+ Smarty, Blade, Latte)
- [x] `ssti-freemarker` — Freemarker/Java (+ Velocity, Pebble, SpEL, Thymeleaf, Groovy, Java EL)

### Other Web
- [x] `ssrf` — basic, blind, cloud metadata, filter bypass, gopher/dict/file protocol exploitation
- [x] `lfi` — LFI (536 lines), PHP wrappers (filter/data/input/zip/phar), 8 LFI-to-RCE methods, filter bypass, platform-specific paths, RFI
- [ ] `file-upload-bypass` — extension/content-type/magic byte bypass
- [ ] `deserialization-java` — Java (ysoserial, gadget chains)
- [ ] `deserialization-php` — PHP (phar, __wakeup)
- [ ] `deserialization-dotnet` — .NET (ysoserial.net)
- [ ] `xxe` — classic, blind, OOB
- [x] `command-injection` — (486 lines) Linux/Windows operators, 5 filter bypass categories, blind (time/DNS/file), argument injection, polyglots
- [ ] `jwt-attacks` — alg:none, key confusion, kid injection
- [ ] `request-smuggling` — CL.TE, TE.CL, H2 downgrade

### Discovery
- [x] `web-vuln-discovery` — entry point: fuzz, test, route to technique skills (converted)
- [ ] Update `web-vuln-discovery` routing table as each new technique skill is created
- [ ] Final review of `web-vuln-discovery` after all web skills are complete

## Phase 4: Core Skills — Active Directory

- [ ] `ad-attack-discovery` — entry point: enumerate domain, identify attack paths, route to techniques
- [ ] AD Enumeration (BloodHound, PowerView, LDAP)
- [ ] Kerberoasting / AS-REP Roasting
- [ ] Kerberos Delegation (unconstrained, constrained, RBCD)
- [ ] ADCS Certificate Abuse (ESC1–ESC15)
- [ ] NTLM Relay & Coercion
- [ ] ACL/ACE Abuse (WriteDACL, GenericAll, GenericWrite)
- [ ] Pass-the-Hash / Over-Pass-the-Hash
- [ ] DCSync / NTDS Dumping
- [ ] Trust Attacks (SID history, inter-realm TGT)
- [ ] Password Spraying & Credential Harvesting

## Phase 5: Core Skills — Privilege Escalation

- [ ] Windows Privesc (token impersonation, service abuse, DLL hijack, UAC bypass)
- [ ] Linux Privesc (SUID, sudo, capabilities, cron, kernel exploits)
- [ ] macOS Privesc (TCC bypass, dylib hijack, SIP bypass)

## Phase 6: Core Skills — Infrastructure & Network

- [ ] Network Recon (nmap, service enumeration, protocol-specific)
- [ ] Pivoting & Tunneling (SSH, chisel, ligolo-ng, proxychains)
- [ ] Cloud — AWS (IAM, IMDS, S3, Lambda)
- [ ] Cloud — Azure (Azure AD, tokens, CAP bypass, service abuse)
- [ ] Containers (Docker escape, K8s RBAC, SA token abuse)
- [ ] CI/CD (GitHub Actions, GitLab CI, secrets extraction)

## Phase 7: Core Skills — Red Team Operations

- [ ] C2 Frameworks (Cobalt Strike, Mythic, Sliver)
- [ ] Initial Access (phishing, office macros, HTML smuggling)
- [ ] Evasion (AMSI bypass, EDR unhooking, ETW patching)
- [ ] Persistence (Windows registry/services, Linux cron/systemd, AD)
- [ ] Credential Dumping (Mimikatz, DPAPI, LSASS)

## Phase 8: Supplemental Skills

- [ ] Hash Cracking (hashcat, john, rules, wordlists)
- [ ] Shell Cheatsheet (reverse shells, bind shells, TTY upgrade)
- [ ] Database Attacks (MSSQL xp_cmdshell, linked servers, MySQL UDF)
- [ ] Binary Exploitation (stack, heap, ROP — CTF-oriented)
- [ ] Mobile (Android Frida, iOS, WebView attacks)
- [ ] AI/LLM Security (prompt injection, MCP attack surface)

## Backlog

- [ ] Wireless attacks (limited source material)
- [ ] Physical/hardware (limited source material)
- [ ] GCP cloud (gap across all three repos)
