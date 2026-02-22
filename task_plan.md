# red-run — Skill Library Task Plan

Claude Code skills for penetration testing and CTF work, built from reference material in InternalAllTheThings, PayloadsAllTheThings, and HackTricks.

## Phase 1: Survey & Taxonomy — COMPLETE

- [x] Survey InternalAllTheThings
- [x] Survey PayloadsAllTheThings
- [x] Survey HackTricks
- [x] Build unified topic taxonomy across all three repos
- [x] Categorize topics into skill groups
- [x] Document findings in `findings.md`

## Phase 2: Skill Architecture — COMPLETE

- [x] Define directory layout and naming conventions
- [x] Define skill file format (front matter, sections, structure)
- [x] Create template skill as the canonical pattern
- [x] Document conventions in CLAUDE.md (covers layout, format, naming, opsec rating)

## Phase 3: Core Skills — Web Application (CURRENT)

Priority: highest (broadest coverage across all three repos)

Split strategy: by **technique** (not by DB engine). DB/engine variants live as subsections within each skill. A discovery/triage skill acts as the entry point with a decision tree routing to specific technique skills.

- [x] Web Vulnerability Discovery — entry point: content/parameter fuzzing, injection testing, response analysis decision tree (`web-vuln-discovery`)
- [ ] SQL Injection — Union-based, per-DB variants (`sql-injection-union`) — WRITTEN, IN REVIEW
- [ ] SQL Injection — Error-based, per-DB variants (`sql-injection-error`) — WRITTEN, IN REVIEW
- [ ] SQL Injection — Blind: boolean, time-based, OOB (`sql-injection-blind`) — WRITTEN, IN REVIEW
- [ ] SQL Injection — Stacked queries, second-order (`sql-injection-stacked`)
- [ ] XSS — Reflected + filter bypass (`xss-reflected`)
- [ ] XSS — Stored (`xss-stored`)
- [ ] XSS — DOM-based (`xss-dom`)
- [ ] SSTI — Jinja2 (`ssti-jinja2`)
- [ ] SSTI — Twig (`ssti-twig`)
- [ ] SSTI — Freemarker (`ssti-freemarker`)
- [ ] SSRF — basic, blind, cloud metadata (`ssrf`)
- [ ] File Inclusion — LFI, PHP wrappers, LFI-to-RCE, RFI (`lfi`)
- [ ] File Upload — extension/content-type/magic byte bypass (`file-upload-bypass`)
- [ ] Deserialization — Java (`deserialization-java`)
- [ ] Deserialization — PHP (`deserialization-php`)
- [ ] Deserialization — .NET (`deserialization-dotnet`)
- [ ] XXE — classic, blind, OOB (`xxe`)
- [ ] Command Injection — Linux/Windows + filter bypass (`command-injection`)
- [ ] JWT Attacks — alg:none, key confusion, kid injection (`jwt-attacks`)
- [ ] Request Smuggling — CL.TE, TE.CL, H2 downgrade (`request-smuggling`)

## Phase 4: Core Skills — Active Directory

Priority: highest (exceptional depth in InternalAllTheThings)

- [ ] AD Attack Discovery — entry point: enumerate domain, identify attack paths, decision tree routing to technique skills (`ad-attack-discovery`)
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
