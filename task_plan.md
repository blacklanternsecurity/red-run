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
- [x] Create orchestrator at `skills/orchestrator/SKILL.md`
- [x] Convert 5 existing skill.md files to SKILL.md format
- [x] Delete old skill.md files and old template
- [x] Update README.md — v2 architecture, skill inventory, engagement logging, installation

### Engagement logging
- [x] Define engagement directory structure and file conventions (activity log, findings, evidence) — `./engagement/` with `activity.md`, `findings.md`, `scope.md`, `evidence/`
- [x] Build engagement logging into the SKILL.md template — `## Engagement Logging` section after Mode, auto-detect + offer to create
- [x] Build engagement logging into the orchestrator — initialize engagement dir, maintain activity log, track findings
- [x] Define evidence format: milestone-based activity entries, numbered findings with severity/target/technique/impact/evidence/repro
- [x] Document conventions in CLAUDE.md — `### Engagement Logging` under Architecture
- [x] Batch update all 11 existing skills with Engagement Logging section

### State management
- [x] Define `engagement/state.md` format — Targets, Credentials, Access, Vulns, Pivot Map, Blocked
- [x] Add `## State Management` section to SKILL.md template
- [x] Build state.md initialization into orchestrator
- [x] Add vulnerability chaining logic to orchestrator (Step 5)
- [x] Batch update all 20 web skills with State Management section
- [x] Update web-vuln-discovery with discovery-specific state management
- [x] Document state management conventions in CLAUDE.md
- [x] Update README.md engagement directory structure

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
- [x] `file-upload-bypass` — (506 lines) extension bypass (alternative/double/null byte/case/special chars/NTFS ADS), content-type & magic byte bypass, server config exploitation (.htaccess/web.config/uWSGI), image polyglots & EXIF injection, ZIP traversal, race conditions, ImageMagick CVEs, webshell payloads (PHP/ASP/JSP)
- [x] `deserialization-java` — (404 lines) ysoserial gadget chains (CommonsCollections/CommonsBeanutils/URLDNS), JNDI injection + Log4Shell (CVE-2021-44228 with WAF bypass), JSF ViewState, framework-specific (WebLogic T3/JBoss/Jenkins), Runtime.exec() workarounds
- [x] `deserialization-php` — (365 lines) magic methods (__wakeup/__destruct/__toString), POP chains, PHPGGC (Monolog/Laravel/Symfony/Guzzle), phar:// deserialization + polyglots (JPEG/GIF/PNG), autoload exploitation, type juggling auth bypass, Laravel APP_KEY forgery
- [x] `deserialization-dotnet` — (408 lines) ysoserial.net (TypeConfuseDelegate/ObjectDataProvider/WindowsIdentity), dangerous formatters (BinaryFormatter/LosFormatter/SoapFormatter), ViewState attacks (machine keys + Blacklist3r/BadSecrets), JSON.NET TypeNameHandling, .NET Remoting, framework-specific (SharePoint/Sitecore/Telerik)
- [x] `xxe` — (466 lines) classic file read, blind/OOB (HTTP/FTP), error-based (remote + local DTD), XInclude, file format injection (SVG/DOCX/XLSX/SOAP/RSS), WAF bypass, XXE-to-SSRF
- [x] `command-injection` — (486 lines) Linux/Windows operators, 5 filter bypass categories, blind (time/DNS/file), argument injection, polyglots
- [x] `jwt-attacks` — (533 lines) alg:none, null signature, HS256 brute force (hashcat/jwt_tool), RS256→HS256 key confusion, header injection (kid path traversal/SQLi/command injection, jwk embedding, jku spoofing, x5u/x5c), claim tampering, cross-service relay, RSA key recovery
- [x] `request-smuggling` — (570 lines) CL.TE, TE.CL, TE.TE obfuscation, H2.CL/H2.TE/h2c smuggling, response desync, cache poisoning, WebSocket smuggling, connection state attacks, hop-by-hop abuse

### Authorization & Authentication
- [x] `idor` — (569 lines) horizontal/vertical access control bypass, UUID/ObjectId prediction, parameter tampering, API IDOR (REST/GraphQL/batch), encoding bypass, method override, automated enumeration
- [x] `csrf` — (609 lines) token bypass (remove/empty/untied/static), SameSite bypass (Lax GET/method override, None, 2-min window), Referer suppression, JSON CSRF (text/plain, sendBeacon), file upload CSRF, login CSRF, WebSocket CSRF, clickjacking chain
- [x] `cors-misconfiguration` — (565 lines) origin reflection, null origin (sandboxed iframe), regex bypass (unescaped dot/missing anchor/special chars), subdomain trust, wildcard abuse, cache poisoning, CORS+IDOR chain, XSSI/JSONP
- [x] `oauth-attacks` — (610 lines) redirect URI manipulation (path traversal/open redirect chain/parameter pollution/special chars), state bypass (CSRF account linking), code theft (reuse/race condition/client binding), token leakage (Referer/postMessage/implicit flow), OIDC (email claim abuse/nonce bypass/discovery SSRF), PKCE bypass, scope escalation, ROPC 2FA bypass, ATO chains
- [x] `password-reset-poisoning` — (533 lines) host header poisoning (Host/X-Forwarded-Host/double host/absolute URL), token leakage via Referer, email parameter injection (duplication/CRLF Cc/Bcc/separator/JSON array), token weakness analysis (sequential/timestamp/hash/UUID v1), brute-force with rate limit bypass, response manipulation, username enumeration, dangling markup
- [x] `2fa-bypass` — (585 lines) response manipulation (status code/body/redirect), direct navigation bypass, null/empty/array code submission, OTP brute-force with rate limit bypass (IP rotation/session rotation/code resend/HTTP/2 single-packet), backup code attacks, session fixation, remember-me token abuse, OAuth/SSO/ROPC bypass, CSRF on 2FA disable, race conditions
- [x] `nosql-injection` — (519 lines) MongoDB operator injection ($ne/$gt/$regex/$where), auth bypass, blind character extraction with automation scripts, $where JS execution, $lookup cross-collection, Mongoose RCE (CVE-2024-53900), GraphQL filter injection, MongoLite $func
- [x] `race-condition` — (719 lines) limit-overrun (coupon/balance/vote/invite), HTTP/2 single-packet attack, HTTP/1.1 last-byte sync, Turbo Intruder templates (single-gate/multi-endpoint/connection warming), asyncio+httpx PoCs, authentication races (password reset token reuse/2FA code reuse/registration confirmation/email change verification), rate limit bypass (HTTP/2 multiplexing/GraphQL alias batching/session rotation), partial construction races, race window expansion, session locking workaround, WebSocket races, TOCTOU (database-level)

### Discovery
- [x] `web-vuln-discovery` — entry point: fuzz, test, route to technique skills (converted)
- [x] Update `web-vuln-discovery` routing table as each new technique skill is created
- [x] Final review of `web-vuln-discovery` after all web skills are complete

## Phase 3b: Extended Web Skills

Identified during the Phase 3 coverage audit. Important techniques with good source material
in ~/docs/ but lower priority than core Phase 3. Build as capacity allows; may be interleaved
with later phases.

### Injection & Protocol
- [ ] `ldap-injection` — filter injection, wildcard auth bypass, blind extraction
- [ ] `xpath-injection` — filter termination, blind exploitation, OOB extraction
- [ ] `xslt-injection` — EXSLT RCE (PHP/Java/.NET), file read via document()
- [ ] `ssi-esi-injection` — SSI directives (echo/exec/include), ESI abuse on CDNs
- [ ] `crlf-injection` — header injection, response splitting, session fixation, cache poisoning
- [ ] `graphql-attacks` — introspection abuse, batching for rate-limit bypass, mutation exploitation
- [ ] `websocket-attacks` — handshake bypass, message manipulation, cross-site WebSocket hijacking

### Client-Side & Browser
- [ ] `prototype-pollution` — client-side gadget chains, server-side RCE via gadgets, property traversal
- [ ] `client-side-template-injection` — AngularJS sandbox escape, Vue.js gadgets, React context leaks
- [ ] `clickjacking` — frame overlay, invisible buttons, X-Frame-Options bypass, form hijacking
- [ ] `open-redirect` — path-based, parameter-based, domain validation bypass, javascript:/data: protocols
- [ ] `xs-leak` — XS-search, timing attacks, frame counting, cache probing, CSS injection
- [ ] `postmessage-exploitation` — cross-origin messaging abuse, SOP bypass, sensitive data leakage

### Logic & Bypass
- [ ] `http-parameter-pollution` — WAF bypass via duplicate params, backend parsing inconsistencies
- [ ] `web-cache-poisoning` — header manipulation, path discrepancy, URL normalization, cache deception
- [ ] `rate-limit-bypass` — header manipulation, IP rotation, HTTP/2 multiplexing, distributed requests
- [ ] `csv-formula-injection` — DDE payload, formula prefix detection, MS Office formula execution
- [ ] `proxy-waf-bypass` — path normalization, hop-by-hop abuse, HTTP method override, verb tampering

## Phase 4: Core Skills — Active Directory

### Source Material Survey — COMPLETE
- [x] Survey `~/docs/InternalAllTheThings` AD content — 65+ files, exceptional depth across ADCS, delegation, relay, ACL
- [x] Survey `~/docs/hacktricks/src/windows-hardening/active-directory-methodology/` — 42 files + 2 subdirs, adds OPSEC/detection context, modern ticket variants, 2025 enforcement changes
- [x] Survey `~/docs/PayloadsAllTheThings` — minimal AD content, all redirects to InternalAllTheThings. Only LDAP injection (Phase 3b) relevant.
- [x] Define concrete skill splits — 16 skills (1 discovery + 15 technique), see below
- [x] Define batching — 5 batches of 3-4 skills each, see below

### Skill List (16 skills: 1 discovery + 15 technique)

**Batch 1: Foundation** — used on every AD engagement
- [x] `ad-attack-discovery` — (511 lines) domain enum (BloodHound, PowerView, LDAP, netexec), 3 access levels (unauth/username/creds), attack surface mapping, routing table to all 15 technique skills
- [x] `kerberos-roasting` — (436 lines) Kerberoasting (SPN-based TGS extraction) + AS-REP Roasting (pre-auth disabled) + Timeroasting (subsection) + targeted kerberoasting (ACL abuse) + kerberoasting without domain account (Charlie Clark technique)
- [x] `password-spraying` — (508 lines) lockout policy enum, smart password generation, Kerberos pre-auth spray (kerbrute/SpearSpray), NTLM spray (NetExec multi-protocol), OWA spray, empty password/STATUS_PASSWORD_MUST_CHANGE technique. OPSEC exception documented.
- [x] `pass-the-hash` — (473 lines) Pass-the-Key (AES256, lowest OPSEC), Over-Pass-the-Hash (NTLM→TGT), Pass-the-Ticket (ccache/kirbi), Direct PTH (last resort), lateral movement tools, OPSEC comparison table

**Batch 2: Kerberos & ACL** — advanced Kerberos + privilege escalation
- [x] `kerberos-delegation` — (508 lines) Unconstrained (TGT harvesting + SpoolService/PetitPotam/DFSCoerce coercion + krbrelayx), Constrained (S4U2Self + S4U2Proxy + SPN swapping + altservice), RBCD (msDS-AllowedToActOnBehalfOfOtherIdentity + machine account creation + cleanup). 3 attack paths with enumeration, exploitation, and cleanup for each.
- [x] `kerberos-ticket-forging` — (463 lines) Golden Ticket (krbtgt hash/AES → forged TGT, cross-forest via extra-sid), Silver Ticket (service hash/AES → forged TGS, common SPN targets table, KB5021131 AES enforcement), Diamond Ticket (decrypt/modify/re-encrypt legitimate TGT, /ldap /opsec flags), Sapphire Ticket (U2U PAC swap via S4U2Self), Pass-the-Ticket (ccache/kirbi conversion + injection). OPSEC comparison table.
- [x] `acl-abuse` — (554 lines) GenericAll/GenericWrite on users (4 options: shadow credentials, targeted Kerberoasting, ASREPRoast UAC, logon script), GenericAll on groups, WriteDACL (DCSync, GenericAll grant, OU inheritance), WriteOwner (ownership + DACL chain), ForceChangePassword, RBCD via computer write access, AdminSDHolder persistence (SDProp backdoor). Decision tree by ACL right + target type.

**Batch 3: ADCS** — certificate services attack surface
- [x] `adcs-template-abuse` — (457 lines) ESC1 (enrollee-supplies-subject + SAN manipulation + SID pinning for KB5014754), ESC2 (Any Purpose EKU + No EKU subordinate CA), ESC3 (enrollment agent two-step: agent cert + on-behalf-of), ESC6 (EDITF_ATTRIBUTESUBJECTALTNAME2 CA flag + certreq.exe native). Full enumeration (Certipy/Certify/NetExec), PKINIT/Schannel/LDAPS auth chains, UnPAC the Hash, certificate format conversion. Decision tree by ESC variant.
- [x] `adcs-access-and-relay` — (475 lines) ESC4 (template ACL → modify to ESC1 + restore via -save-old), ESC5 (PKI container write → malicious template + golden cert path), ESC7 (ManageCA → officer + SubCA abuse + ESC6 flag enable + RCE via CRL write, ManageCertificates → extension injection), ESC8 (NTLM relay to HTTP enrollment via ntlmrelayx/certipy + PetitPotam/SpoolSample/DFSCoerce coercion + Kerberos relay variant via krbrelayx), ESC11 (NTLM relay to ICPR RPC). OPSEC exception documented for relay attacks (inherently NTLM). Cleanup commands for ESC4/ESC7.
- [x] `adcs-persistence` — (611 lines) Golden Certificate (CA key extraction via certipy/certutil/mimikatz, forge with SID + CRL for KB5014754, ForgeCert), user/machine cert persistence + renewal, ESC9 (no security extension + UPN swap via shadow creds), ESC10 (weak mapping StrongCertificateBindingEnforcement=0, CertificateMappingMethods UPN), ESC12 (YubiHSM key extraction), ESC13 (issuance policy OID group link), ESC14 (altSecIdentities explicit mapping with strong/weak format table), ESC15/CVE-2024-49019 (application policies override on schema v1), certificate theft (THEFT1-5: CAPI/CNG export, DPAPI user/machine, filesystem search, UnPAC), KB5014754 enforcement impact table. OPSEC comparison for all techniques.

**Batch 4: Relay & Credentials** — authentication attacks
- [x] `auth-coercion-relay` — (581 lines) Coercion methods (PetitPotam/PrinterBug/DFSCoerce/ShadowCoerce/CheeseOunce with method reference table, NetExec coerce_plus), NTLM relay (ntlmrelayx to SMB/LDAP/AD CS/MSSQL, SOCKS proxy, machine account creation, RBCD setup), Kerberos relay (krbrelayx + Responder, krbrelayx + mitm6 IPv6 DNS, Kerberos reflection CVE-2025-33073), name resolution poisoning (Responder LLMNR/NBNS/WPAD, mitm6 IPv6, Inveigh), hash capture + NTLMv1 downgrade + cracking, advanced techniques (Drop the MIC CVE-2019-1040, Ghost Potato CVE-2019-1384, NTLM reflection). OPSEC exception documented (inherently NTLM/network-level). Signing requirement assessment workflow.
- [x] `credential-dumping` — (603 lines) DCSync (targeted + full domain via secretsdump/mimikatz/NetExec, replication rights check), NTDS extraction (VSS shadow copy, ntdsutil IFM, vssadmin, offline secretsdump), SAM dump (remote + manual hive extraction, LSA secrets), LAPS (legacy ms-Mcs-AdmPwd + Windows LAPS 2023+ encrypted, NetExec/bloodyAD/PowerView), gMSA (authorized read + GoldenGMSA persistence via KDS root key), dMSA BadSuccessor (CVE-2025-21293, GenericWrite → successor → managed password), DSRM (DsrmAdminLogonBehavior, hash extraction), GPP passwords (MS14-025, cpassword decryption). OPSEC comparison table for all 12 techniques.
- [x] `gpo-abuse` — (532 lines) GPO enumeration (GPOHound dump/analysis, BloodHound edges, PowerView ACL scan, NetExec), exploitation via 7 methods (immediate task, startup/logon scripts, registry Run key, local admin assignment, user rights), 5 tools (SharpGPOAbuse/PowerGPOAbuse/pyGPOAbuse/GroupPolicyBackdoor/StandIn), SYSVOL/NETLOGON logon script poisoning (VBS/BAT/PS1 prepend technique), GPP password extraction (Get-GPPPassword/NetExec/manual openssl decryption), cleanup procedures (GroupPolicyBackdoor state-based + manual). GPO refresh timing documented.

**Batch 5: Trust & Persistence** — domain boundaries + persistence
- [x] `trust-attacks` — (464 lines) Trust enumeration (nltest/PowerView/AD Module/NetExec, trust property assessment: SIDFilteringQuarantined/SelectiveAuthentication/ForestTransitive/TGTDelegation), SID history injection (golden ticket + extra SID child→parent via Mimikatz/Rubeus/ticketer.py, diamond ticket variant for stealth, raiseChild.py automation), inter-realm TGT forging (trust key extraction via lsadump::trust, referral ticket creation, service ticket request in target domain), cross-forest trust abuse (trust account authentication + Kerberoasting, cross-forest RBCD via S4U, SID filtering bypass assessment), PAM trust exploitation (shadow principal enumeration, group membership manipulation via bloodyAD/Set-ADObject). PAC validation considerations for 2025+ enforcement mode. Trust type decision tree.
- [x] `sccm-exploitation` — (510 lines) SCCM enumeration (sccmhunter find/show/http, SharpSCCM, unauthenticated MP HTTP endpoints: MPKEYINFORMATIONMEDIA/MPLIST/SITESIGNCERT), NAA extraction via policy request CRED-2 (machine account creation + sccmwtf + policysecretunobfuscate.py), NAA from WMI/DPAPI CRED-3 (SharpSCCM local secrets, SharpDPAPI blob decryption), WMI repository CRED-4 (SharpDPAPI/SharpSCCM disk search), MP relay to MSSQL TAKEOVER-1 (ntlmrelayx + PetitPotam coercion, SOCKS proxy, RBAC_Admins SQL injection, OSD policy secret extraction + PXEthief decryption), client push relay ELEVATE-2 (SharpSCCM invoke client-push), PXE boot harvesting CRED-1 (pxethiefy/SharpPXE, Hashcat mode 31100), database credential extraction CRED-5 (Mimikatz misc::sccm, SQLRecon), application deployment lateral movement (MalSCCM full chain + SharpSCCM exec), SCCM share looting (CMLoot). Attack path decision tree by access level.
- [x] `ad-persistence` — (600 lines) Golden Certificate (CA key extraction via certipy/certutil/mimikatz, forge with SID embedding for KB5014754, ForgeCert/Certify, certificate renewal + enrollment agent persistence), DCShadow (dual mimikatz instances, SIDHistory/primaryGroupID/ntSecurityDescriptor modification, /stack for batching, delegated DCShadow via Set-DCShadowPermissions), Skeleton Key (misc::skeleton, PPL bypass via !processprotect, /letaes compatibility), Custom SSP (mimilib.dll persistent via registry + memssp in-memory non-persistent, credential logging to kiwissp.log/mimilsa.log), security descriptor backdoors (WMI via Set-RemoteWMI, WinRM via Set-RemotePSRemoting, registry via DAMP Add-RemoteRegBackdoor for remote hash retrieval), ADFS Golden SAML (DKM key extraction from AD contact object, ADFSDump WID extraction, ADFSpoof/Shimit token forging, O365 support), SID history persistence (via DCShadow/golden ticket/direct modification). Persistence decision tree by stealth and reboot survival. OPSEC comparison table.

### Phase 4b: Extended AD Skills

Identified during survey. Important but lower-priority techniques or specialized targets.

- [ ] `adidns-poisoning` — Dynamic DNS record injection, wildcard records, WPAD hijack. Source: IATT ad-integrated-dns.md (81 lines) + HT ad-dns-records.md (600+ lines).
- [ ] `dcom-lateral-movement` — DCOM-based remote execution (MMC20, ShellWindows, ShellBrowserWindow, ExcelDDE). Source: IATT internal-dcom.md (80 lines).
- [ ] `rodc-exploitation` — RODC enumeration, Kerberos Key List Attack. Source: IATT ad-adds-rodc.md (70 lines).
- [ ] `ad-named-cves` — NoPAC (CVE-2021-42278), PrintNightmare (CVE-2021-1675), ZeroLogon (CVE-2020-1472), PrivExchange, MS14-068. Source: IATT CVE/ directory (5 files, 444+ lines) + HT printnightmare.md (600+).
- [ ] `mssql-ad-abuse` — Linked server hopping, xp_cmdshell, impersonation chains, UNC path injection. Source: HT abusing-ad-mssql.md (500+ lines).
- [ ] `deployment-targets` — MDT bootstrap creds, WSUS update poisoning, SCOM RunAs decryption. Source: IATT 3 files (120 lines combined).

## Phase 5: Core Skills — Privilege Escalation

### Source Material Survey — COMPLETE
- [x] Survey `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/` — 26 files + DLL subdir (6,000+ lines). Key: Potato family (5 variants), service misconfig, DLL hijack (536 lines), UAC bypass (275 lines), DPAPI (500 lines), named pipes (297 lines), leaked handles (696 lines), COM hijacking, kernel exploits, autorun (354 lines). Supporting dirs: credentials (424+215+211 lines), UAC (275+319 lines), NTLM (349+185 lines).
- [x] Survey `~/docs/hacktricks/src/linux-hardening/privilege-escalation/` — 46 files + kernel subdir (8,000+ lines). Key: capabilities (1,700 lines), Docker breakout (664+ lines, 14 container files totaling 3,500+), D-Bus (540 lines), groups (288 lines), restricted shell (296 lines), wildcards (255 lines), euid/suid (216 lines), NFS (146 lines), LD_PRELOAD (156 lines). Kernel CVE-2025-38352 (332 lines).
- [x] Survey `~/docs/hacktricks/src/macos-hardening/` — 70+ files, 14,000+ lines. FAR deeper than expected. TCC bypass: 2,275 lines (800 + 932 payloads + 543 bypasses with 20+ techniques). SIP bypass: 284 lines (8+ CVEs). Gatekeeper: 571 lines (11+ CVEs). Dylib hijacking: 169 lines. XPC/Mach IPC: 1,323 lines. Sandbox escape: 507 lines. Process abuse: 2,000+ lines. Persistence: 1,818 lines. Code signing: 413 lines. Electron injection: 511 lines.
- [x] Survey `~/docs/InternalAllTheThings/` — linux-privilege-escalation.md (868 lines, systematic checklist with LinPEAS/pspy/GTFOBins/SUDO_KILLER), windows-privilege-escalation.md (1,565 lines, tool-heavy with PowerUp/Seatbelt/winPEAS/WES-NG, Potato CLSID tables, BYOVD drivers). IATT is complementary — more actionable checklists; HT has deeper technique coverage.
- [x] Survey `~/docs/PayloadsAllTheThings/` — Minimal. Two redirect pages (50+68 lines) pointing to IATT. No standalone privesc content. PAT's value is in the RCE-to-privesc pipeline (command injection, LFI-to-RCE, deserialization) already covered by Phase 3 web skills.
- [x] Define concrete skill splits — Windows 6, Linux 5, macOS 3 (Phase 5b). See below.
- [x] Define batching — 4 core batches by platform, macOS as Phase 5b (1 batch).

### Skill List (14 skills: 2 discovery + 9 technique + 3 macOS technique)

**Batch 1: Windows Foundation** — most common Windows privesc vectors
- [ ] `windows-privesc-discovery` — Enumeration (WinPEAS, PowerUp, Seatbelt, Watson, WES-NG, PrivescCheck, Sherlock, JAWS), system info, user/group enum, installed software, network config, scheduled tasks, routing to 5 technique skills. Source: HT README.md (1,961 lines) + IATT (1,565 lines).
- [ ] `windows-token-impersonation` — Potato family (JuicyPotato/RoguePotato/PrintSpoofer/GodPotato/SweetPotato/EfsPotato/JuicyPotatoNG with CLSID tables), SeImpersonate/SeAssignPrimaryToken, SeDebugPrivilege (token copy + LSASS access), SeBackupPrivilege (SAM/SYSTEM/ntds.dit), SeTakeOwnership, SeManageVolume, SeLoadDriverPrivilege (BYOVD), FullPowers (recover impersonation from services). Source: HT juicypotato.md (162), roguepotato.md (253), token-abuse.md (202), seimpersonate.md (183), sedebug.md (220) + IATT token section.
- [ ] `windows-service-dll-abuse` — Unquoted service paths (enumeration + exploitation), weak service permissions (binpath modification, registry ACL abuse), service binary replacement, DLL hijacking (search order, writable PATH, side-loading, COM DLL), DLL proxying. Source: HT dll-hijacking/ (694 lines), service-triggers.md (148), abusing-auto-updaters.md (234) + IATT service/DLL sections.

**Batch 2: Windows Extended** — secondary vectors + credential access
- [ ] `windows-uac-bypass` — UAC bypass techniques (auto-elevating binaries, fodhelper, eventvwr, sdclt, silentcleanup, cmstp, DiskCleanup), COM hijacking (CLSID registry abuse), AlwaysInstallElevated (MSI payload via WiX/msfvenom), autorun exploitation (startup folders, registry Run/RunOnce). Source: HT uac.md (275), com-hijacking.md (149), create-msi-with-wix.md (72), autorun.md (354).
- [ ] `windows-credential-harvesting` — HiveNightmare/ShadowCopy SAM extraction (CVE-2021-36934), DPAPI decryption (user/machine masterkeys, domain backup key), PowerShell history/transcripts, unattend.xml/sysprep, Sticky Notes DB, Credential Manager/vault, WiFi passwords, browser credentials, registry AutoLogon, Windows Vault. Source: HT dpapi.md (500), registry-hive.md (128), README.md credential sections + IATT password looting sections. Note: Distinct from Phase 4 `credential-dumping` which covers AD-level extraction (DCSync/NTDS/LAPS/gMSA).
- [ ] `windows-kernel-exploits` — Kernel CVEs (MS17-010 EternalBlue, MS16-032, MS15-051, CVE-2019-1388, KiTrap0D), exploit-suggester workflow (Watson/WES-NG/windows-exploit-suggester), BYOVD/LoLDrivers (vulnerable driver loading for kernel R/W), privileged file write (DiagHub, UsoDLLLoader, WerTrigger, WerMgr), privileged file delete (MSI rollback), named pipe impersonation, PrintNightmare local (CVE-2021-1675), leaked handle exploitation. Source: HT kernel-race.md (138), arbitrary-kernel-rw.md (123), leaked-handle.md (696), named-pipe.md (172+125) + IATT kernel/printer sections.

**Batch 3: Linux Foundation** — standard Linux privesc workflow
- [ ] `linux-privesc-discovery` — Enumeration (LinPEAS, LinEnum, linux-smart-enumeration, unix-privesc-check, pspy, SUDO_KILLER, linux-exploit-suggester), system info, kernel version, users/groups, network, running processes, installed software, writable directories, routing to 4 technique skills. Source: HT README.md (2,137 lines) + IATT (868 lines).
- [ ] `linux-sudo-suid-capabilities` — Sudo misconfig (NOPASSWD, LD_PRELOAD/LD_LIBRARY_PATH with sudo, sudo_inject, CVE-2021-3156 Baron Samedit, CVE-2019-14287 -u#-1, doas), SUID/SGID binary exploitation (GTFOBins, custom SUID binaries, shared object injection), Linux capabilities (CAP_SYS_ADMIN, CAP_DAC_READ_SEARCH, CAP_SETUID, CAP_NET_BIND, CAP_SYS_PTRACE, CAP_NET_RAW, 20+ capabilities with exploitation examples). Source: HT linux-capabilities.md (1,700 lines), euid-ruid-suid.md (216) + IATT sudo/SUID/capabilities sections.
- [ ] `linux-cron-service-abuse` — Cron job exploitation (writable scripts, PATH manipulation, wildcard injection in cron, pspy monitoring), systemd timer abuse, D-Bus enumeration and command injection (gdbus, busctl, dbus-send, PolicyKit bypass), Unix socket command injection, writable init scripts/systemd units. Source: HT d-bus.md (540 lines), socket-command-injection.md (89), wildcards.md (255) + IATT cron/systemd sections.

**Batch 4: Linux Extended** — filesystem + kernel vectors
- [ ] `linux-file-path-abuse` — Writable /etc/passwd (add root user), /etc/sudoers, /etc/shadow, NFS no_root_squash (SUID binary injection via mount), shared library hijacking (LD_PRELOAD, ldconfig, RPATH manipulation, ld.so.conf), wildcard injection (tar checkpoint, chown, chmod, rsync, 7z), PATH hijack in scripts/cron, Docker/LXD group escape (mount host filesystem), writable /etc/crontab. Source: HT nfs.md (146), ld.so.conf.md (156), wildcards.md (255), groups.md (288), lxd.md (96), write-to-root.md (98) + IATT NFS/library/group sections.
- [ ] `linux-kernel-exploits` — Kernel CVEs (DirtyPipe CVE-2022-0847, DirtyCow CVE-2016-5195, GameOver(lay) CVE-2023-0386, CVE-2025-38352 POSIX CPU timers, Full Nelson CVE-2010-4258, Mempodipper CVE-2012-0056, RDS CVE-2010-3904), exploit-suggester workflow, restricted shell escape (rbash/rksh breakout via GTFOBins, chroot escape, Python/Perl/PHP shell spawning), jailbreak techniques. Source: HT kernel-exploitation/ subdir, escaping-from-limited-bash.md (296) + IATT kernel CVE references.

### Phase 5b: Extended Privilege Escalation — macOS

macOS has exceptional depth (14,000+ lines in HT). Deferred from core Phase 5 because macOS privesc is less common in standard engagements but fully viable as standalone skills.

- [ ] `macos-tcc-bypass` — TCC database structure (user + system), 20+ bypass techniques: write bypass (TCC doesn't protect writes), ClickJacking, request spoofing (Info.plist), SSH default FDA, CVE-2020-9934 (HOME env variable), CVE-2021-30970 Powerdir (NFSHomeDirectory), plugin loading (Directory Utility CVE-2020-27937, CoreAudiod HAL CVE-2020-29621, DAL camera), Firefox dylib injection, Terminal .terminal scripts, mount_apfs (CVE-2020-9771), mounting over TCC (CVE-2021-1784/30808), SQLITE_AUTO_TRACE, Automation→FDA chain (Finder, System Events + Accessibility). TCC exploitation payloads (camera, keylogger, screen capture). Source: HT macos-tcc/ (800 + 932 + 543 lines).
- [ ] `macos-sip-gatekeeper-bypass` — SIP bypass: Installer packages (CVE-2019-8561, CVE-2020-9854), Shrootless CVE-2021-30892 (/etc/zshenv), systemmigrationd env abuse (Migraine CVE-2023-32369), CVE-2022-22583 (/tmp mount), fsck_cs symlink, sealed system snapshots. Gatekeeper bypass: path length (CVE-2021-1810), zip structure (CVE-2022-22616), ACL+AppleDouble (CVE-2022-42821), Apple Archive (CVE-2022-32910), uchg flag, third-party unarchiver vulns. Quarantine xattr manipulation. Code signing abuse (disable-library-validation entitlement). Source: HT macos-sip.md (284), macos-gatekeeper.md (571), macos-code-signing.md (413).
- [ ] `macos-dylib-injection` — DYLD_INSERT_LIBRARIES injection, @rpath hijacking (LC_RPATH abuse), weak library validation bypass, library reexport, install_name_tool manipulation, function hooking (method swizzling, DYLD hooks, fishhook, Mach-O patching), Electron injection (ELECTRON_RUN_AS_NODE, preload scripts, debug port), Dirty NIB (NIB file abuse for code execution), Chromium --load-extension injection. Source: HT macos-dyld-hijacking.md (169), macos-library-injection.md (344), macos-function-hooking.md (380), macos-electron-applications-injection.md (511), macos-dirty-nib.md (152).

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

- [ ] Global tool prerequisites list — enumerate every tool mentioned across all skills, add to README as install checklist (do last, after all skills written)
- [ ] Learning - how to updating skills, keep them current with the latest methods, update them prior to closing an engagement based on knowledge gained from that engagement, targeted research mode)
- [ ] Wireless attacks (limited source material)
- [ ] Physical/hardware (limited source material)
- [ ] GCP cloud (gap across all three repos)

### Niche / Reference-Only (build if needed during engagements)
- [ ] Captcha bypass
- [ ] Subdomain/domain takeover
- [ ] Email injection
- [ ] Insecure randomness / weak token prediction
- [ ] ORM injection (ORM-specific query manipulation)
- [ ] ZIP slip (archive path traversal — may fold into lfi)
- [ ] SOAP/JAX-WS attacks
- [ ] gRPC-Web testing
- [ ] ReDoS (regex denial of service)
- [ ] Unicode normalization bypass
- [ ] Reverse tab nabbing
