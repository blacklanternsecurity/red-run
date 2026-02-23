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
- [x] Update web-discovery with discovery-specific state management
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
- [x] `web-discovery` — entry point: fuzz, test, route to technique skills (converted)
- [x] Update `web-discovery` routing table as each new technique skill is created
- [x] Final review of `web-discovery` after all web skills are complete

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
- [x] `ad-discovery` — (511 lines) domain enum (BloodHound, PowerView, LDAP, netexec), 3 access levels (unauth/username/creds), attack surface mapping, routing table to all 15 technique skills
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
- [x] Survey `~/docs/hacktricks/src/macos-hardening/` — 70+ files, 14,000+ lines. Deep content exists but **macOS removed from scope** (never used in engagements).
- [x] Survey `~/docs/InternalAllTheThings/` — linux-privilege-escalation.md (868 lines, systematic checklist with LinPEAS/pspy/GTFOBins/SUDO_KILLER), windows-privilege-escalation.md (1,565 lines, tool-heavy with PowerUp/Seatbelt/winPEAS/WES-NG, Potato CLSID tables, BYOVD drivers). IATT is complementary — more actionable checklists; HT has deeper technique coverage.
- [x] Survey `~/docs/PayloadsAllTheThings/` — Minimal. Two redirect pages (50+68 lines) pointing to IATT. No standalone privesc content. PAT's value is in the RCE-to-privesc pipeline (command injection, LFI-to-RCE, deserialization) already covered by Phase 3 web skills.
- [x] Define concrete skill splits — Windows 6, Linux 5. macOS removed (not in scope).
- [x] Define batching — 4 batches by platform. Docker/container escapes deferred to Phase 6.

### Skill List (11 skills: 2 discovery + 9 technique)

**Batch 1: Windows Foundation** — most common Windows privesc vectors

Build workflow: Survey source material for all 3 skills (parallel agents) → write skills → update task_plan.md/progress.md/README.md → commit + push. Follow existing template at `skills/_template/SKILL.md`. No Kerberos-first convention (that's AD-only). Skills go in `skills/privesc/`.

- [x] `windows-discovery` — (489 lines) Enumeration hub: WinPEAS/PowerUp/Seatbelt/Watson/WES-NG/PrivescCheck, 9-step workflow (system info → user context → services → scheduled tasks → network → credential hunting → security controls → automated tools → routing), privilege-to-skill routing table, security controls detection (AV/AppLocker/PPL/Credential Guard)
- [x] `windows-token-impersonation` — (440 lines) Potato family decision tree by OS version (JuicyPotato/PrintSpoofer/GodPotato/RoguePotato/EfsPotato/SigmaPotato/JuicyPotatoNG/PrintNotifyPotato), dangerous privilege exploitation (SeDebug token theft, SeBackup SAM extraction, SeRestore file write, SeTakeOwnership, SeLoadDriver BYOVD, SeManageVolume raw disk), FullPowers for stripped service accounts, CLSID reference
- [x] `windows-service-dll-abuse` — (532 lines) Unquoted service paths, weak service permissions (accesschk/sc config binpath), service registry ACL abuse, service triggers (named pipe/ETW/RPC), DLL search order hijacking with Process Monitor, DLL proxying (DLLirant/Spartacus), COM DLL hijacking, writable PATH injection, DLL payload templates (C/mingw/msfvenom), auto-updater/IPC abuse

**Batch 2: Windows Extended** — secondary vectors + credential access

Build workflow: Same as Batch 1. Survey source material (parallel agents) → write skills → update tracking → commit + push. Skills go in `skills/privesc/`.

- [x] `windows-uac-bypass` (561 lines) — UAC bypass (fodhelper/eventvwr/sdclt/SilentCleanup/CMSTP/WSReset), COM hijacking (InprocServer32/TypeLib), AlwaysInstallElevated MSI, autorun exploitation (startup folders/Run keys/Active Setup/Winlogon).
  - **UAC bypass techniques**: fodhelper.exe (registry `ms-settings\shell\open\command`), eventvwr.exe (`mscfile\shell\open\command`), sdclt.exe (IsolatedCommand), computerdefaults.exe, cmstp.exe (INF file with ScriptBlock), DiskCleanup (scheduled task environment variable), SilentCleanup (auto-elevating scheduled task), WSReset.exe. Each technique: registry key to write, command to trigger, cleanup.
  - **COM hijacking for persistence/bypass**: InprocServer32 in HKCU overrides HKLM, find hijackable CLSIDs via scheduled tasks/explorer, registry modification (no admin needed for HKCU). Process Monitor enumeration for missing COM DLLs.
  - **AlwaysInstallElevated**: Check both `HKCU\...\Installer\AlwaysInstallElevated` and `HKLM\...\Installer\AlwaysInstallElevated` = 0x1. Exploit: `msfvenom -p windows/x64/shell_reverse_tcp ... -f msi -o evil.msi` → `msiexec /quiet /qn /i evil.msi`. WiX custom MSI for more control.
  - **Autorun exploitation**: Startup folder write (`C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup`), registry Run/RunOnce keys (HKCU writable), writable autorun binaries (icacls check).
  - **Structure**: Step 1 (check UAC level + integrity), Step 2 (auto-elevating binary bypass), Step 3 (COM hijacking), Step 4 (AlwaysInstallElevated), Step 5 (autorun exploitation), Step 6 (escalate/pivot)
  - **Source files**: `~/docs/hacktricks/src/windows-hardening/authentication-credentials-uac-and-efs/uac-user-account-control.md` (275 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/com-hijacking.md` (149 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/create-msi-with-wix.md` (72 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries.md` (354 lines), `~/docs/InternalAllTheThings/docs/redteam/escalation/windows-privilege-escalation.md` (UAC sections)
  - **Target**: ~350-400 lines

- [x] `windows-credential-harvesting` (540 lines) — Local credential discovery: HiveNightmare/SAM shadow copy, DPAPI (SharpDPAPI/mimikatz/dpapi.py with 5 decryption methods), browser creds (SharpChrome/Firefox), PS history/transcripts, unattend/sysprep, credential vault, WiFi, cloud creds, SessionGopher. Distinct from Phase 4 `credential-dumping` which covers AD-level DCSync/NTDS/LAPS/gMSA.
  - **HiveNightmare / ShadowCopy SAM** (CVE-2021-36934): Check `icacls C:\Windows\System32\config\SAM` for `BUILTIN\Users:(I)(RX)`, extract via `mimikatz misc::shadowcopies` + `lsadump::sam`, or `secretsdump.py -sam SAM -system SYSTEM LOCAL`
  - **DPAPI decryption**: User masterkeys (`%APPDATA%\Microsoft\Protect\{SID}`), machine masterkeys, domain backup key. Tools: `mimikatz dpapi::masterkey`, `SharpDPAPI`, `dpapi.py`. Decrypt Chrome/Edge cookies, saved passwords, RDP credential files.
  - **PowerShell history/transcripts**: `ConsoleHost_history.txt` path, transcript logs in `C:\Transcripts`, Module Logging + Script Block Logging in Event Viewer
  - **Unattend/sysprep files**: `C:\unattend.xml`, `C:\Windows\Panther\Unattend.xml`, `C:\Windows\system32\sysprep\sysprep.xml` — base64-encoded admin credentials
  - **Credential Manager/vault**: `cmdkey /list`, `runas /savecred /user:<user> cmd.exe`, `vaultcmd /listcreds:"Web Credentials"`, mimikatz `vault::list`
  - **Browser credentials**: Chrome `Login Data` SQLite + `dpapi::chrome`, Firefox `key3.db`/`key4.db` + `logins.json`, SharpChromium, SharpWeb
  - **Other**: Sticky Notes SQLite DB, WiFi passwords (`netsh wlan show profile key=clear`), registry AutoLogon (`Winlogon` DefaultPassword), PuTTY/WinSCP/RDP saved sessions, IIS web.config, cloud credential files (AWS/Azure/GCP), McAfee SiteList.xml
  - **Structure**: Step 1 (quick wins — cmdkey, registry, history), Step 2 (HiveNightmare check), Step 3 (DPAPI extraction), Step 4 (browser creds), Step 5 (file/config search), Step 6 (escalate/pivot)
  - **Source files**: `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/dpapi-extracting-passwords.md` (500 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries.md` (354 — credential sections), `~/docs/hacktricks/src/windows-hardening/stealing-credentials/credentials-mimikatz.md` (424 lines), `~/docs/InternalAllTheThings/docs/redteam/escalation/windows-privilege-escalation.md` (password looting sections)
  - **Target**: ~400-450 lines

- [x] `windows-kernel-exploits` (615 lines) — Exploit-suggester workflow (WES-NG/Watson), named kernel CVEs (PrintNightmare/EternalBlue/MS16-032/MS15-051/KiTrap0D/CVE-2019-1388), BYOVD (loldrivers.io, token theft), privileged file write (DiagHub/UsoDLLLoader/WerTrigger), MSI rollback file delete, named pipe impersonation, leaked handle exploitation, restricted shell escape (CLM/AppLocker bypass).
  - **Exploit-suggester workflow**: `systeminfo` → WES-NG (`python3 wes.py systeminfo.txt`), Watson (.NET on target), windows-exploit-suggester (legacy). Triage: match KB patches against known CVEs.
  - **Named kernel CVEs with embedded PoC references**: MS17-010 EternalBlue (SMB RCE → SYSTEM), MS16-032 (secondary logon handle), MS15-051 (Win32k), CVE-2019-1388 (certificate dialog UAC bypass), KiTrap0D (MS10-015), PrintNightmare local (CVE-2021-1675 — `SharpPrintNightmare.exe`), CVE-2020-0796 SMBGhost, HiveNightmare (CVE-2021-36934 — already in credential-harvesting but kernel-adjacent)
  - **BYOVD (Bring Your Own Vulnerable Driver)**: Load known-vulnerable signed drivers for kernel R/W. Cross-reference against loldrivers.io. Example: Capcom.sys, RTCore64.sys, DBUtil. SeLoadDriverPrivilege required (or admin). Disable EDR/PPL via kernel access.
  - **Privileged file write**: DiagHub (load DLL as SYSTEM), UsoDLLLoader (abuse Update Session Orchestrator), WerTrigger (Windows Error Reporting), WerMgr (overwrite via WER report). Each: trigger mechanism, target path, exploitation.
  - **Privileged file delete**: MSI rollback (create MSI that deletes target file during rollback), abuse for DACL reset.
  - **Named pipe impersonation**: Create named pipe, wait for privileged client connection, impersonate token. `CreateNamedPipe` + `ConnectNamedPipe` + `ImpersonateNamedPipeClient`. SpoolSample/PrintSpoofer pipe variant.
  - **Leaked handle exploitation**: Enumerate process handles for inherited SYSTEM tokens. `NtQueryInformationProcess`, `DuplicateHandle`. Source material: HT leaked-handle.md (696 lines — extensive).
  - **Restricted shell context**: Brief note on escaping constrained shells (PowerShell Constrained Language Mode bypass, AppLocker bypass via MSBuild/InstallUtil) as prerequisite before kernel exploitation.
  - **Structure**: Step 1 (assess — OS version, patches, drivers), Step 2 (exploit-suggester), Step 3 (kernel CVE exploitation), Step 4 (BYOVD), Step 5 (privileged file operations), Step 6 (named pipe / leaked handle), Step 7 (escalate/pivot)
  - **Source files**: `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/leaked-handle-exploitation.md` (696 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/named-pipe-client-impersonation.md` (172 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/privilege-escalation-abusing-tokens/named-pipes.md` (125 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/kernel-race-condition.md` (138 lines), `~/docs/hacktricks/src/windows-hardening/windows-local-privilege-escalation/arbitrary-write-privilege-escalation.md` (123 lines), `~/docs/InternalAllTheThings/docs/redteam/escalation/windows-privilege-escalation.md` (kernel + BYOVD + printer sections)
  - **Target**: ~450-500 lines

**Batch 3: Linux Foundation** — standard Linux privesc workflow — COMPLETE (1,871 lines)
- [x] `linux-discovery` (599 lines) — LinPEAS/LinEnum/pspy/lse/unix-privesc-check/SUDO_KILLER enumeration, system info (kernel, OS, arch), user context with group-to-vector routing table, sudo config assessment (CVE version matching, NOPASSWD/env_keep pattern table), SUID/SGID/capabilities enumeration with GTFOBins cross-reference and critical capability table, cron/systemd timer assessment with pspy monitoring, file/directory permissions (writable passwd/shadow/sudoers, library hijack paths, writable PATH dirs), credential hunting (history, configs, cloud creds, git repos), network/socket enumeration, security controls detection (SELinux, AppArmor, ASLR, ptrace scope, container detection), kernel exploit assessment, automated tool section (LinPEAS modes, LinEnum, lse, pspy), routing decision tree to 4 technique skills.
- [x] `linux-sudo-suid-capabilities` (610 lines) — Sudo NOPASSWD GTFOBins exploitation (30+ binary escapes), environment variable abuse (LD_PRELOAD with C payload, LD_LIBRARY_PATH, PYTHONPATH/PERL5LIB, BASH_ENV injection), sudo CVEs (CVE-2021-3156 Baron Samedit heap overflow, CVE-2019-14287 UID bypass, sudo_inject token reuse), SUID binary exploitation (GTFOBins patterns, custom binary analysis with strings/strace/ltrace, PATH hijack, shared object injection with constructor), SGID exploitation, 15+ Linux capabilities with full exploitation code (CAP_SETUID/SETGID direct root, CAP_DAC_OVERRIDE file write, CAP_DAC_READ_SEARCH file read + shocker, CAP_SYS_ADMIN mount abuse, CAP_SYS_PTRACE GDB/shellcode injection, CAP_SYS_MODULE kernel module, CAP_CHOWN/FOWNER permission change, CAP_SETFCAP capability chaining, CAP_NET_RAW sniffing).
- [x] `linux-cron-service-abuse` (662 lines) — Cron exploitation (writable script hijack with SUID bash/reverse shell, PATH manipulation, writable cron directory injection), wildcard injection (tar checkpoint with full payload, chown/chmod --reference, rsync -e, 7z @file exfiltration, zip -T/-TT), systemd exploitation (writable service/timer files, ExecStartPre injection, PATH hijack, service binary replacement), D-Bus exploitation (busctl/gdbus/dbus-send enumeration, command injection via string parameters, Python D-Bus exploitation), PolicyKit bypass (CVE-2021-4034 PwnKit, CVE-2021-3560 timing attack with loop), recent D-Bus CVEs (2024-2025), Unix socket command injection (socat/nc/curl), Docker socket exploitation, init script/xinetd/at job/anacron exploitation, cleanup reminders.

**Batch 4: Linux Extended** — filesystem + kernel vectors
- [ ] `linux-file-path-abuse` — Writable /etc/passwd (add root user), /etc/sudoers, /etc/shadow, NFS no_root_squash (SUID binary injection via mount), shared library hijacking (LD_PRELOAD, ldconfig, RPATH manipulation, ld.so.conf), wildcard injection (tar checkpoint, chown, chmod, rsync, 7z), PATH hijack in scripts/cron, Docker/LXD group escape (mount host filesystem), writable /etc/crontab. Source: HT nfs.md (146), ld.so.conf.md (156), wildcards.md (255), groups.md (288), lxd.md (96), write-to-root.md (98) + IATT NFS/library/group sections.
- [ ] `linux-kernel-exploits` — Kernel CVEs (DirtyPipe CVE-2022-0847, DirtyCow CVE-2016-5195, GameOver(lay) CVE-2023-0386, CVE-2025-38352 POSIX CPU timers, Full Nelson CVE-2010-4258, Mempodipper CVE-2012-0056, RDS CVE-2010-3904), exploit-suggester workflow, restricted shell escape (rbash/rksh breakout via GTFOBins, chroot escape, Python/Perl/PHP shell spawning), jailbreak techniques. Source: HT kernel-exploitation/ subdir, escaping-from-limited-bash.md (296) + IATT kernel CVE references.

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
