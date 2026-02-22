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

**Best source: InternalAllTheThings** (exceptional — largest single-topic section at 472K)
**Supplemented by: HackTricks** (solid AD methodology section)

| Topic | IATT Depth | HT Depth | Notes |
|-------|-----------|----------|-------|
| ADCS (ESC1–ESC15) | EXCEPTIONAL (15 individual files) | HIGH | Certipy, Golden Certificate |
| Kerberoasting / AS-REP | HIGH | HIGH | Impacket, Rubeus, NetExec, bifrost |
| Kerberos Delegation | HIGH (3 types + S4U + Bronze Bit) | HIGH | Unconstrained, constrained, RBCD |
| NTLM Relay & Coercion | HIGH (signing table by OS) | HIGH | ntlmrelayx, Responder, WebClient |
| ACL/ACE Abuse | HIGH | HIGH | WriteDACL, GenericAll, ForceChangePassword |
| BloodHound Enumeration | HIGH (all collector variants) | HIGH | SharpHound, RustHound, Python, SOAP |
| Pass-the-Hash | HIGH | HIGH | |
| NTDS Dumping | HIGH | HIGH | DCSync, secretsdump |
| Trust Attacks | HIGH (SID history, inter-realm TGT, PAM) | HIGH | |
| Password Spraying | HIGH | HIGH | |
| Shadow Credentials | HIGH | HIGH | msDS-KeyCredentialLink |
| LAPS/gMSA/dMSA | HIGH (3 separate files) | MEDIUM | |
| GPO Abuse | HIGH | MEDIUM | |
| SCCM/WSUS/MDT | HIGH (deployment attacks) | MEDIUM | |
| Named CVEs | HIGH (ZeroLogon, NoPAC, PrintNightmare) | MEDIUM | |

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
