# red-run — Source Material Findings

Survey of three reference repos to build a unified topic taxonomy for the skill library.

## Source Repos

| Repo | Path | Focus | Files |
|------|------|-------|-------|
| InternalAllTheThings | `~/docs/InternalAllTheThings` | Internal pentesting, AD, red team ops | ~100 |
| PayloadsAllTheThings | `~/docs/PayloadsAllTheThings` | Web vulns, payloads, injection techniques | ~200 |
| HackTricks | `~/docs/hacktricks` | Broadest scope — web, binary, mobile, macOS, network | ~700+ |

## Unified Topic Taxonomy

### 1. Web Application Attacks

**Best source: PayloadsAllTheThings** (deepest payload coverage per vuln class)
**Supplemented by: HackTricks** (172 web pentesting files, LFI-to-RCE chains, smuggling variants)

| Topic | PATT Depth | HT Depth | IATT Depth |
|-------|-----------|----------|-----------|
| SQL Injection | HIGHEST (3096 lines, 10 files, 8 DB engines) | HIGH | — |
| XSS | HIGH (1915 lines, filter/CSP/WAF bypass) | EXCELLENT (DOM, shadow DOM, service workers) | — |
| SSTI | HIGH (1796 lines, 6 engines) | HIGH | — |
| SSRF | HIGH (965 lines, cloud metadata) | HIGH (URL bypass, platform-specific) | — |
| Deserialization | HIGH (1083 lines, 7 language files) | HIGH (Java, .NET, PHP, Python, Ruby, Node) | — |
| File Inclusion | HIGH (723 lines, LFI-to-RCE) | HIGH (PHP filters, nginx, phpinfo, phar) | — |
| File Upload | HIGH (465 lines, per-type bypass) | MEDIUM | — |
| XXE | MEDIUM (688 lines) | HIGH | — |
| Command Injection | MEDIUM (476 lines) | MEDIUM | — |
| Request Smuggling | MEDIUM (181 lines) | HIGH (CL.TE, TE.CL, H2 downgrade, browser) | — |
| JWT | HIGH (541 lines, alg confusion) | HIGH | — |
| CORS | MEDIUM (274 lines) | HIGH | — |
| GraphQL | MEDIUM (401 lines) | MEDIUM | — |
| Prototype Pollution | MEDIUM (191 lines) | MEDIUM (Node.js focused) | — |
| OAuth | LOW (81 lines) | HIGH (to account takeover) | — |
| SAML | MEDIUM (200 lines) | HIGH | — |
| Race Conditions | MEDIUM (165 lines) | HIGH | — |
| Cache Deception | MEDIUM (151 lines) | HIGH (poisoning, URL discrepancy) | — |

### 2. Active Directory

**Best source: InternalAllTheThings** (exceptional — largest single-topic section at 472K, 65+ files)
**Supplemented by: HackTricks** (42 files + 2 subdirs, OPSEC annotations, 2025 threat context)
**PayloadsAllTheThings**: Minimal — all AD content redirects to InternalAllTheThings. Only LDAP injection (Phase 3b) is relevant.

#### Source Material Depth by Topic

| Topic | IATT Depth | HT Depth | IATT Files | Key Tools |
|-------|-----------|----------|------------|-----------|
| ADCS (ESC1–ESC15) | EXCEPTIONAL | VERY HIGH | 17 (15 ESC + enum + golden) | Certipy, Certify, Rubeus |
| Kerberos Delegation | VERY HIGH | DEEP | 3 (unconstrained, constrained, RBCD) | Rubeus, Impacket, bloodyAD |
| ACL/ACE Abuse | VERY HIGH | VERY HIGH (2500+ lines) | 1 (comprehensive) | bloodyAD, PowerView, Invoke-ACLPwn |
| NTLM Relay & Coercion | VERY HIGH | HIGH | 4 (NTLM relay, Kerberos relay, coercion, DCOM) | ntlmrelayx, Responder, krbrelayx, mitm6 |
| Kerberoasting / AS-REP | HIGH | HIGH (500+ lines each) | 3 (kerberoasting, asrep, timeroasting) | Rubeus, Impacket, NetExec, hashcat |
| Credential Extraction | HIGH | MEDIUM | 9 (LAPS, gMSA, dMSA, shadow creds, hash dump, PTH, OPTH, PTK, spray) | secretsdump, mimikatz, NetExec, bloodyAD |
| NTDS/DCSync | HIGH | HIGH (300+ lines) | 1 (comprehensive) | secretsdump, mimikatz, ntdsutil |
| Ticket Forging | MEDIUM | DEEP (golden/silver/diamond 400-900 lines each) | 3 (tickets, S4U, bronze bit) | Rubeus, mimikatz, Impacket ticketer |
| Trust Attacks | MEDIUM | MEDIUM | 4 (relationships, SID history, trust ticket, PAM) | mimikatz, ticketer, bloodyAD |
| GPO Abuse | HIGH | MEDIUM | 1 | SharpGPOAbuse, GPOHound |
| Password Spraying | HIGH | DEEP (1000+ lines) | 1 | NetExec, kerbrute, DomainPasswordSpray |
| BloodHound/Enumeration | HIGH | HIGH (600+ lines) | 2 (enumerate, groups) | SharpHound, BloodHound.py, rusthound-ce |
| SCCM | HIGH | HIGH (400+ lines) | 1 | SharpSCCM, sccmhunter, MalSCCM |
| AD FS | HIGH | — | 1 | ADFSDump, ADFSpoof |
| DNS Poisoning (ADIDNS) | HIGH | DEEP (600+ lines) | 1 | adidnsdump, dnstool, Inveigh |
| Named CVEs | VERY HIGH (5 files) | MEDIUM | 5 (MS14-068, NoPAC, PrintNightmare, PrivExchange, ZeroLogon) | Various |
| Deployment (MDT/WSUS/SCOM) | MEDIUM | — | 3 | PowerPXE, SharpWSUS, SCOMDecrypt |
| Persistence (DCShadow, SSP, Skeleton Key) | — | DEEP | — | mimikatz |
| AD Linux Integration | MEDIUM | — | 1 | tickey, SSSDKCMExtractor |

#### HackTricks Unique Value (vs InternalAllTheThings)

| Feature | HackTricks Adds | InternalAllTheThings Lacks |
|---------|-----------------|---------------------------|
| Diamond/Sapphire tickets | Modern OPSEC variants (/ldap, /opsec, recutting) | Only Golden/Silver |
| OPSEC annotations | Event ID correlation (4768/4769/4624) per technique | Sparse detection info |
| 2025 threat context | RC4 phase-out, PAC validation, certificate mapping enforcement | Legacy RC4-focused |
| DNS abuse depth | Wildcard, WPAD hijack, Certifried, DDSpoof | Surface-level |
| SCCM relay chain | MP → MSSQL → OSD secret extraction | SCCM enumeration only |
| Token privilege mapping | BloodHound with logon rights, not just ACLs | Minimal |

#### ADCS ESC Breakdown (for skill split decision)

| ESC | Attack Primitive | Prerequisite | Source Depth |
|-----|-----------------|--------------|-------------|
| ESC1 | Enrollee supplies SAN + client auth EKU | Low-priv enrollment | Deep |
| ESC2 | Any Purpose / no EKU → request SAN | Low-priv enrollment | Medium |
| ESC3 | Enrollment Agent → request on behalf | Agent enrollment right | Medium |
| ESC4 | Vulnerable ACL on template → modify to ESC1 | Template ACL write | Medium |
| ESC5 | Vulnerable ACL on CA objects | NTAuthCertificates write | Medium |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 CA flag | CA flag misconfigured | Medium |
| ESC7 | ManageCA/ManageCertificates on CA | CA permissions | Deep |
| ESC8 | NTLM relay to HTTP web enrollment | Network position | Deep |
| ESC9 | No security extension + CT_FLAG bypass | Template flag | Medium |
| ESC10 | Weak cert mapping + GenericAll/Write | ACL on target | Medium |
| ESC11 | NTLM relay to ICPR (RPC enrollment) | Network position | Medium |
| ESC12 | Shell access to CA → steal private key | CA server shell | Medium |
| ESC13 | Issuance policy → linked group SID | Policy misconfigured | Medium |
| ESC14 | altSecurityIdentities explicit mapping abuse | ACL on target | Medium |
| ESC15 | Application policies extension override | Template flag | Medium |

#### Key Observations

1. **ADCS is the deepest single topic**: 17 files in IATT + deep HT subdirectory. ESC1-6 are the most commonly exploited (template misconfigs). ESC7-11 require relay or CA access. ESC12-15 are newer/niche.
2. **Delegation coverage is excellent**: 3 distinct attack paths (unconstrained, constrained, RBCD) with 100+ lines each, distinct prerequisites and exploitation chains.
3. **Relay/coercion is foundational**: 4 deep files covering NTLM relay, Kerberos relay, coercion methods, DCOM. Relay is the backbone of many AD attack chains.
4. **HackTricks adds modern OPSEC context**: Diamond tickets, 2025 enforcement changes, event ID correlation. Essential for OPSEC-conscious skills.
5. **Timeroasting is thin**: Only 16 lines in IATT. Include as subsection of roasting, not standalone.
6. **Shadow credentials bridges ACL abuse and credential access**: Requires msDS-KeyCredentialLink write (ACL) but yields credentials.
7. **CVEs are historical but still exploited**: NoPAC, PrintNightmare, ZeroLogon still appear in real environments. Include as extended phase.
8. **Tool ecosystem**: Rubeus (18 files), Impacket (14), mimikatz (15), bloodyAD (4+), Certipy (4+), NetExec (5+) are the workhorses.
9. **Gaps across sources**: No coverage of Credential Guard bypass, detailed RODC exploitation, comprehensive lockout bypass techniques.

### 3. Privilege Escalation

**Best source: InternalAllTheThings** (Windows + Linux combined in redteam/escalation/)
**Supplemented by: HackTricks** (deeper Windows kernel-level primitives, macOS)

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| Windows Token Impersonation | HIGH (Potato family, PrintSpoofer) | HIGH | HIGH |
| Windows Service Abuse | HIGH | HIGH | HIGH |
| Windows DLL/COM Hijack | MEDIUM | HIGH | MEDIUM |
| Windows UAC Bypass | MEDIUM | HIGH | MEDIUM |
| Windows Kernel | MEDIUM | HIGH (race conditions, handle leaks) | MEDIUM |
| Linux SUID/Capabilities | HIGH | HIGH | HIGH |
| Linux Sudo/GTFOBins | HIGH | HIGH | HIGH |
| Linux Cron/Systemd | HIGH | MEDIUM | HIGH |
| Linux Kernel Exploits | HIGH (DirtyPipe, DirtyCow) | MEDIUM | HIGH |
| Linux Container Escape | HIGH | HIGH (Docker + cgroups) | MEDIUM |
| macOS TCC/SIP/Sandbox | — | VERY HIGH (74 files) | — |

### 4. Cloud

**Best source: InternalAllTheThings** (Azure 144K, AWS 80K)
**HackTricks cloud content lives in separate repo (not surveyed)**

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| Azure AD Connect | HIGH | — | stub |
| Azure Token Theft | HIGH | — | stub |
| Azure Services (12+) | HIGH (per-service files) | — | — |
| Azure CAP Bypass | HIGH | — | — |
| AWS IAM | HIGH | — | stub |
| AWS IMDS/Metadata | HIGH | — | SSRF payloads |
| AWS S3 | HIGH | — | stub |
| AWS Lambda/Cognito | MEDIUM | — | stub |
| GCP | NONE | NONE | NONE |

### 5. Red Team Operations

**Best source: InternalAllTheThings** (520K across access, escalation, evasion, persistence, pivoting)

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| EDR Bypass | VERY HIGH (236K evasion section) | LIGHT | — |
| AMSI Bypass | HIGH (15+ techniques) | MEDIUM | HIGH |
| Windows Defenses | HIGH (AppLocker, CLM, ETW, WDAC, ASR) | MEDIUM | HIGH |
| Initial Access / Phishing | HIGH (delivery chains, Evilginx, GoPhish) | MODERATE | HIGH |
| Office Attacks | HIGH | — | HIGH |
| HTML Smuggling | HIGH | — | MEDIUM |
| Windows Persistence | HIGH | MEDIUM | HIGH |
| Linux Persistence | HIGH | MEDIUM | HIGH |
| Pivoting | HIGH (SOCKS, SSH, ligolo-ng, chisel) | MODERATE | HIGH |

### 6. C2 Frameworks

**Best source: InternalAllTheThings** (Cobalt Strike 3 files, Mythic, Metasploit)

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| Cobalt Strike | HIGH (infra, OpSec, malleable, BOFs, kits) | MODERATE | HIGH |
| Mythic | MEDIUM (agents, profiles) | MODERATE | — |
| Metasploit | MEDIUM (cheatsheet) | — | HIGH |
| Sliver / Havoc | NONE | NONE | NONE |

### 7. Containers & DevOps

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| Docker Escape | HIGH (socket, cgroup, runc, device) | HIGH | MEDIUM |
| Kubernetes RBAC | HIGH (BadPods, KubeHound) | LIGHT | LOW |
| GitHub Actions | HIGH | — | HIGH |
| GitLab CI | MEDIUM | — | MEDIUM |
| Secrets Enumeration | HIGH (nord-stream, SCMKit) | MEDIUM | MEDIUM |
| Supply Chain | MEDIUM (dependency confusion) | — | LOW |

### 8. Network & Infrastructure

| Topic | IATT Depth | HT Depth | PATT Depth |
|-------|-----------|----------|-----------|
| Nmap / Discovery | HIGH (cheatsheet) | MEDIUM | MEDIUM |
| Protocol Pentesting | — | EXCELLENT (189 files, 60+ protocols) | — |
| MSSQL Attacks | HIGH (5 files) | HIGH | HIGH |
| Hash Cracking | HIGH (cheatsheet) | MODERATE | MODERATE |
| Reverse Shells | HIGH (cheatsheet) | HIGH | HIGH (25+ methods) |
| Wireless | — | LIGHT (3 files) | — |

### 9. Supplemental Categories (HackTricks unique)

| Topic | HT Depth | Notes |
|-------|----------|-------|
| Binary Exploitation | EXCELLENT (101 files) | Stack, heap, ROP, kernel — CTF-grade |
| macOS Security | VERY HIGH (74 files) | TCC, SIP, IPC, dylib, entitlements |
| Mobile Pentesting | HIGH (62 files) | Android Frida, iOS, WebView, zero-click |
| Forensics | MODERATE (~25 files) | Volatility, Wireshark, file carving |
| AI/LLM Security | GOOD (23 files) | Prompt injection, MCP, AI-augmented phishing |

## Cross-Repo Overlap & Complementarity

- **InternalAllTheThings ↔ PayloadsAllTheThings**: PATT redirects AD/cloud/pivoting/evasion content to IATT. PATT owns web payloads; IATT owns internal/red-team content. Minimal duplication.
- **HackTricks ↔ both**: HackTricks is broadest but thinner per-topic on web payloads (PATT wins) and AD (IATT wins). HackTricks uniquely covers binary exploitation, macOS, mobile, forensics, AI, and 60+ network protocol guides.
- **Conclusion**: All three repos are needed. No single repo covers everything. The skill library should synthesize the best from each.

## Gaps Across All Three Repos

| Topic | Status |
|-------|--------|
| GCP (Google Cloud) | No coverage in any repo |
| Wireless / WiFi | 3 light files in HackTricks only |
| Physical security | Light in HackTricks only |
| Sliver C2 | Not covered |
| Havoc C2 | Not covered |
| Brute Ratel C2 | Not covered |
| Oracle Cloud | Not covered |
