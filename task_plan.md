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
- [ ] Final review of `web-vuln-discovery` after all web skills are complete

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
