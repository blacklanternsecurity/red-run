# red-run — Skill Library Task Plan

Claude Code skills for penetration testing and CTF work, built from reference material in InternalAllTheThings, PayloadsAllTheThings, and HackTricks.

## Phase 1: Survey & Taxonomy (CURRENT)

- [x] Survey InternalAllTheThings
- [x] Survey PayloadsAllTheThings
- [x] Survey HackTricks
- [x] Build unified topic taxonomy across all three repos
- [x] Categorize topics into skill groups
- [x] Document findings in `findings.md`

## Phase 2: Skill Architecture

- [x] Define directory layout and naming conventions
- [x] Define skill file format (front matter, sections, structure)
- [x] Create template skill as the canonical pattern
- [ ] Document conventions in a CONTRIBUTING or CLAUDE.md

## Phase 3: Core Skills — Web Application

Priority: highest (broadest coverage across all three repos)

- [ ] SQL Injection (per-DB variants: MySQL, MSSQL, PostgreSQL, Oracle, SQLite)
- [ ] XSS (DOM, stored, reflected, filter bypass, CSP bypass)
- [ ] SSTI (per-engine: Jinja2, Twig, Freemarker, Pebble, ERB)
- [ ] SSRF (cloud metadata, protocol smuggling, redirect chains)
- [ ] File Inclusion (LFI/RFI, PHP wrappers, LFI-to-RCE)
- [ ] File Upload (bypass by extension, content type, magic bytes)
- [ ] Deserialization (Java, PHP, Python, .NET, Ruby, Node.js)
- [ ] XXE (classic, blind, OOB)
- [ ] Command Injection (Linux, Windows, filter bypass)
- [ ] Authentication Bypass (JWT, OAuth, SAML, 2FA)
- [ ] Request Smuggling (CL.TE, TE.CL, HTTP/2 downgrade)

## Phase 4: Core Skills — Active Directory

Priority: highest (exceptional depth in InternalAllTheThings)

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
