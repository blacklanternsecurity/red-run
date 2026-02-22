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
- [ ] Restructure to Claude Code native SKILL.md format
- [ ] Create new template at `skills/_template/SKILL.md`
- [ ] Create orchestrator at `skills/orchestrator/SKILL.md`
- [ ] Create `install.sh` (symlinks to `~/.claude/skills/red-run-*/`)
- [ ] Create `uninstall.sh`
- [ ] Convert 5 existing skill.md files to SKILL.md format
- [ ] Delete old skill.md files and old template
- [ ] Update CLAUDE.md, README.md

## Phase 3: Core Skills — Web Application (CURRENT)

Split strategy: by **technique** (not by DB engine). DB/engine variants as subsections. Discovery skill routes to techniques via decision tree.

### SQL Injection
- [ ] `sql-injection-union` — UNION-based, per-DB variants (convert from v1)
- [ ] `sql-injection-error` — error-based, per-DB variants (convert from v1)
- [ ] `sql-injection-blind` — boolean, time-based, OOB (convert from v1)
- [ ] `sql-injection-stacked` — stacked queries, second-order (convert from v1)

### XSS
- [ ] `xss-reflected` — reflected + filter bypass
- [ ] `xss-stored` — stored XSS
- [ ] `xss-dom` — DOM-based

### SSTI
- [ ] `ssti-jinja2` — Jinja2/Python
- [ ] `ssti-twig` — Twig/PHP
- [ ] `ssti-freemarker` — Freemarker/Java

### Other Web
- [ ] `ssrf` — basic, blind, cloud metadata
- [ ] `lfi` — LFI, PHP wrappers, LFI-to-RCE, RFI
- [ ] `file-upload-bypass` — extension/content-type/magic byte bypass
- [ ] `deserialization-java` — Java (ysoserial, gadget chains)
- [ ] `deserialization-php` — PHP (phar, __wakeup)
- [ ] `deserialization-dotnet` — .NET (ysoserial.net)
- [ ] `xxe` — classic, blind, OOB
- [ ] `command-injection` — Linux/Windows + filter bypass
- [ ] `jwt-attacks` — alg:none, key confusion, kid injection
- [ ] `request-smuggling` — CL.TE, TE.CL, H2 downgrade

### Discovery
- [ ] `web-vuln-discovery` — entry point: fuzz, test, route to technique skills (convert from v1)
- [ ] Revisit `web-vuln-discovery` after all web skills are complete

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
