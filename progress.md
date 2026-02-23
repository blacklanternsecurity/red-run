# red-run — Session Log

## 2026-02-23 — Phase 6 Batch 1: Network Foundation (COMPLETE)

### Done

- Completed source material survey for Phase 6 Batch 1 (2 skills)
- Created `skills/network` branch from `skills/privesc`
- Built 2 Network Foundation skills (Batch 1) on `skills/network` branch:
  - `network-recon` (880 lines) — 9-step workflow: passive recon (DNS enum + zone transfer, Shodan, cert transparency), host discovery (ARP/ICMP/TCP/UDP sweeps, masscan for large ranges), port scanning (default `nmap -A -p- -T4 -oA -vvv` plus quick top-ports, stealth/evasion: fragmentation/decoys/source port/idle scan/timing, masscan+nmap combo, Naabu), service enumeration for 20+ protocols each with embedded quick-win checks (FTP anonymous+write/vsftpd backdoor, SSH CVE-2018-15473+regreSSHion, SMTP open relay+NTLM info, DNS zone transfer, HTTP default creds+git exposure, Kerberos AS-REP roast+user enum, RPC null session+NFS, SMB null/guest+EternalBlue+SMBGhost, LDAP anon bind, MSSQL sa empty+xp_cmdshell, Oracle default SIDs+creds, MySQL root empty+UDF, RDP NTLM leak+BlueKeep, PostgreSQL trust auth, WinRM, Redis unauth RCE+SSH key inject, MongoDB unauth, SNMP default community+Net-SNMP Extend, IPMI cipher 0, NFS no_root_squash, TFTP config grab, VNC no-auth), OS fingerprinting (port signatures, TTL heuristics), vuln scanning (NSE vuln scripts, nuclei templates, specific CVE checks), multi-host pipeline (discovery→quick scan→full scan→service enum), output parsing for state.md, routing decision tree to web-discovery/ad-discovery/technique skills, bash fallback scanning for pivots without nmap.
  - `pivoting-tunneling` (1108 lines) — 15-step workflow: tool selection decision tree by scenario (SSH/shell+upload/HTTP-only/DNS-only/ICMP-only/Windows/NTLM proxy), SSH tunneling (local -L single+multi port, dynamic SOCKS -D with proxychains config, remote -R for NAT/firewall bypass, ~C escape sequence for mid-session forwards, ProxyJump -J multi-hop with ssh_config, sshuttle transparent VPN with DNS forwarding and exclusions, SSH VPN TUN device with NAT/routing), Ligolo-ng (TUN setup, agent/proxy workflow, route addition, listener port forwarding, double pivot via listener chaining, transfer methods), Chisel (reverse SOCKS, port forward single+multi, HTTP proxy support, TLS encryption, transfer methods), socat (TCP/UDP relay, SSL encrypted relay, reverse shell relay), Windows pivoting (netsh portproxy with firewall rules, plink SSH-style tunnels, SocksOverRDP+Proxifier, Chisel/Ligolo Windows binaries), DNS tunneling (dnscat2 with port forward+shell, iodine TUN with routing), ICMP tunneling (hans, ptunnel-ng), HTTP tunneling (neo-reGeorg webshell SOCKS, rpivot NTLM proxy bypass), Metasploit pivoting (autoroute, portfwd, SOCKS module, proxychains config), FRP (TOML config with SOCKS+port forward), public tunnels (ngrok/cloudflared — CTF only), multi-hop scenarios (SSH ProxyJump, sshuttle chain, Ligolo double pivot, Chisel chain, proxychains strict_chain), tunnel verification procedures, SOCKS tool compatibility table (14 pentesting tools), persistent tunnels (SSH keep-alive, autossh, Chisel keepalive, tmux session management), Python minimal SOCKS4 proxy fallback.
- Updated task_plan.md, README.md (59 skills, ~31,400 lines), progress.md
- Tool priority per user preference: SSH > Ligolo-ng > Chisel > others (reflected in skill step ordering)

### Batch 2: Containers

- Built `container-escapes` (1021 lines) — Docker escape (socket/privileged/cgroup release_agent/sensitive mounts/capabilities), Kubernetes exploitation (SA tokens, RBAC, kubelet, etcd, malicious pods), container CVEs (runc CVE-2019-5736, Leaky Vessels CVE-2024-21626, CVE-2025-31133), cloud metadata from containers
- Updated orchestrator to route to network-recon, container-escapes, and pivoting-tunneling
- Moved AWS, Azure, CI/CD to backlog (not first release)
- Phase 6 COMPLETE: 60 skills, ~32,400 lines

### Next

- PR `skills/network` branch to main
- Phase 7: Red Team Operations (or test on HTB first)

---

## 2026-02-23 — Phase 5 Batch 4: Linux Extended Skills (Phase 5 COMPLETE)

### Done

- Built 2 Linux Extended privesc skills (Batch 4) on `skills/privesc` branch:
  - `linux-file-path-abuse` (838 lines) — 10-step workflow: writable critical files (/etc/passwd UID 0 backdoor + hash generation, /etc/shadow root hash replacement, /etc/sudoers NOPASSWD injection, SSH authorized_keys to root), NFS no_root_squash (SUID shell C payload via NFS mount, bash -p copy, nosuid/noexec troubleshooting), Docker group escape (host mount -v /, SUID bash creation, /etc/passwd modification, SSH key injection, docker.sock API curl workflow, nsenter --privileged --pid=host), LXD/LXC group escape (privileged container with security.privileged=true and recursive host disk device, init + image import workflow), disk group (debugfs /etc/shadow + SSH key + bash_history extraction, dd full partition dump, hashcat/john crack workflow), shared library hijacking (missing .so via ldd/strace on SUID binaries, constructor C payload, RPATH/RUNPATH writable directory detection with readelf, /etc/ld.so.conf.d/ cache poisoning, Python os.py and Perl strict.pm path hijack), PATH hijacking (writable PATH directory detection, payload binary with passthrough to real command, staff group /usr/local/bin), profile script injection (.bashrc root-conditional SUID creation, /etc/profile.d/ system-wide with zzz- prefix, reverse shell variant), cleanup checklist.
  - `linux-kernel-exploits` (947 lines) — 7-step workflow: kernel/environment identification (version, distro, arch, protections: KASLR/kptr_restrict/ptrace_scope/dmesg_restrict/SELinux/AppArmor), exploit suggesters (linux-exploit-suggester.sh with version override, les2.pl, manual searchsploit, quick CVE version table with 10 major CVEs ranked by reliability), DirtyPipe CVE-2022-0847 (full C exploit source: /etc/passwd overwrite with offset calculation + page boundary check, affected 5.8-5.16.11/5.15.25), DirtyCow CVE-2016-5195 (full C exploit source: race condition madvise/proc-self-mem threads with 30s sleep, stability warning), GameOver(lay) CVE-2023-0386 (overlayfs user namespace, Ubuntu-specific, FUSE mount + trigger workflow), Netfilter CVE-2023-32233, route4 CVE-2022-2588, legacy CVE quick reference table (7 entries with ExploitDB IDs), pre-compiled exploit repos (lucyoa, bwbwbwbw, Kabot), container kernel escapes (CVE-2022-0492 cgroup release_agent full exploit: mount cgroup + notify_on_release + overlayfs perdir discovery, hostPID nsenter), restricted shell escape (GTFOBins: 6 editors, 3 pagers, 6 interpreters, 7 system utilities, 3 file utilities; PATH manipulation; bash BASH_CMDS/declare tricks; SSH force-bash/ShellShock; Python __builtins__/__subclasses__ sandbox escape; Lua encoded bypass + debug.debug()), chroot escape (classic mkdir+chroot+chdir C code, Python variant, FD escape with fchdir, mount-based /proc/1/root, chw00t tool), kernel protection reference (KASLR/SMEP/SMAP/KPTI, grsecurity/PaX detection, SELinux/AppArmor status, ptrace_scope levels).
- Updated README.md: 11 privesc skills (was 9), added new skill rows, status line (57 skills, ~29,400 lines), removed privesc from Planned section.
- Updated task_plan.md: Batch 4 skills marked complete with line counts and technique summaries.
- **Phase 5 (Privilege Escalation) is now COMPLETE**: 11 skills (6 Windows + 5 Linux), 6,712 lines total.

### Inventory

- Total skills: 57 (29 web + 16 AD + 11 privesc + 1 orchestrator)
- Total lines: ~29,400
- Phase 5: COMPLETE (all 4 batches, 11 skills)

### Next: Phase 6 (Infrastructure & Network) or AD Extended (Phase 3b)

**Branch**: `skills/privesc` — ready for PR to main

---

## 2026-02-23 — Phase 5 Batch 3: Linux Foundation Skills

### Done

- Built 3 Linux Foundation privesc skills (Batch 3) on `skills/privesc` branch:
  - `linux-discovery` (599 lines) — 12-step enumeration workflow: system info (kernel, OS, architecture, environment), user context with group-to-vector routing table (docker→file-path-abuse, lxd→file-path-abuse, disk→file-path-abuse, sudo/wheel→sudo-suid-capabilities), sudo configuration assessment (CVE version matching table for Baron Samedit/CVE-2019-14287/CVE-2025-32463, pattern matching for NOPASSWD/env_keep/SETENV/GTFOBins, doas config), SUID/SGID/capabilities enumeration (find commands, GTFOBins quick reference table for 10 common binaries, critical capabilities table), scheduled task enumeration (cron files, systemd timers, pspy process monitoring with manual alternative), file/directory permissions (world-writable files/dirs, critical file checks for passwd/shadow/sudoers/SSH keys/profile scripts/NFS exports, library hijacking paths with RPATH/missing .so detection, Python library paths, writable PATH directories), credential hunting (history files, config files, database strings, backups, git repos, cloud creds, Docker config, SSH agent), network/services (listening services, internal-only, Unix sockets with docker socket check), security controls (SELinux, AppArmor, ASLR, ptrace scope, seccomp, container detection, kernel protections, compiler availability), kernel exploit assessment (DirtyPipe/DirtyCow/GameOver(lay) version checks, exploit-suggester tools), automated tools section (LinPEAS with stealth/all/password modes, LinEnum, lse, unix-privesc-check, SUDO_KILLER, pspy), routing decision tree to 4 technique skills ranked by reliability/OPSEC.
  - `linux-sudo-suid-capabilities` (610 lines) — 7-step workflow: assess sudo config, sudo NOPASSWD exploitation (30+ GTFOBins escapes organized by category: editors, pagers, interpreters, file utilities, archive utilities, network tools, system tools, file read/write), environment variable abuse (LD_PRELOAD with full C payload and compilation, LD_LIBRARY_PATH hijack, PYTHONPATH/PERL5LIB injection, BASH_ENV injection), sudo CVE exploitation (CVE-2021-3156 Baron Samedit with version check and vuln test, CVE-2019-14287 UID -1 bypass, sudo_inject token reuse with ptrace scope check), SUID binary exploitation (GTFOBins SUID patterns with bash -p, custom binary analysis with strings/strace/ltrace, 3 exploitation patterns: PATH hijack for system() calls, shared object injection for missing libraries with constructor C code, file read/write for credential theft, SGID exploitation), Linux capabilities exploitation (15+ capabilities: CAP_SETUID direct root in Python/Perl/Node/Ruby/PHP, CAP_SETGID group escalation, CAP_DAC_OVERRIDE sudoers/passwd write, CAP_DAC_READ_SEARCH shadow/SSH key read + shocker container escape, CAP_SYS_ADMIN mount abuse + bind mount, CAP_SYS_PTRACE GDB injection + Python ptrace shellcode, CAP_SYS_MODULE kernel module with reverse shell Makefile, CAP_CHOWN/FOWNER ownership/permission changes, CAP_SETFCAP capability chaining, CAP_NET_RAW sniffing), escalation routing.
  - `linux-cron-service-abuse` (662 lines) — 8-step workflow: assess cron/service landscape, cron job exploitation (writable script hijack with 3 payload options: SUID bash/reverse shell/stealthy append, PATH manipulation, writable cron directory injection for /etc/cron.d and user crontab), wildcard injection (tar checkpoint with full shell.sh payload, chown/chmod --reference, rsync -e shell, 7z @file exfiltration, zip -T/-TT test injection), systemd exploitation (writable service file ExecStart/ExecStartPre modification, writable timer with OnCalendar, systemd PATH hijack, service binary replacement), D-Bus exploitation (busctl/gdbus/dbus-send enumeration, command injection via string parameters with bash/gdbus/busctl/Python examples, PolicyKit bypass CVE-2021-4034 PwnKit + CVE-2021-3560 timing attack with loop, recent D-Bus CVEs table 2024-2025), Unix socket exploitation (socat/nc/curl injection, Docker socket exploitation), init script/xinetd/at job/anacron exploitation, cleanup reminders and escalation routing.
- Updated README.md: 9 privesc skills (was 6), updated line counts, status line (55 skills, ~27,600 lines), Planned section (2 remaining instead of 5).
- Updated task_plan.md: Batch 3 skills marked complete with line counts and technique summaries.

### Inventory

- Total skills: 55 (29 web + 16 AD + 9 privesc + 1 orchestrator)
- Total lines: ~27,600
- Phase 5 Batch 3: COMPLETE (3/3 skills built, 1,871 lines)
- Remaining: Batch 4 (2 Linux extended)

### Next: Build Batch 4 (Linux Extended — 2 skills)

**Branch**: `skills/privesc`

**Batch 4 skills to build:**
1. `linux-file-path-abuse` — Writable /etc/passwd, NFS no_root_squash, shared library hijacking, wildcard injection, Docker/LXD group escape
2. `linux-kernel-exploits` — DirtyPipe, DirtyCow, GameOver(lay), exploit-suggester, restricted shell escape, BYOVD

---

## 2026-02-23 — Phase 5 Batch 2: Windows Extended Skills

### Done

- Built 3 Windows Extended privesc skills (Batch 2) on `skills/privesc` branch:
  - `windows-uac-bypass` (561 lines) — 6-step workflow: assess UAC config (ConsentPromptBehaviorAdmin levels, EnableLUA, integrity check), auto-elevating binary bypass (fodhelper with ms-settings registry hijack, eventvwr with mscfile hijack, sdclt with Folder hijack, computerdefaults, CMSTP with INF scriptlet, SilentCleanup with windir env var, WSReset, DiskCleanup — each with full cmd/PowerShell write→trigger→cleanup sequences), COM hijacking (Process Monitor CLSID enumeration, scheduled task CLSID hijack, InprocServer32 HKCU override, TypeLib hijacking with scriptlet payloads), AlwaysInstallElevated (dual registry check, msfvenom MSI, custom WiX MSI, MSI repair exploitation), autorun exploitation (startup folders, Run/RunOnce registry keys, writable autorun binaries, Winlogon Userinit/Shell, Active Setup StubPath), escalation routing. Bypass decision table by Windows version/reliability/OPSEC.
  - `windows-credential-harvesting` (540 lines) — 6-step workflow: quick wins (cmdkey/savecred, registry autologon, PS history/transcripts, unattend/sysprep with base64 decode, registry password search, PuTTY/SSH sessions, WiFi passwords, IIS web.config, credential file search, SessionGopher), HiveNightmare/SAM shadow copy (CVE-2021-36934 icacls detection, mimikatz shadow copy extraction, offline secretsdump.py, backup hive paths), DPAPI extraction (5 decryption methods: current session, known password/NTLM, RPC to DC, domain backup key, LSASS memory — SharpDPAPI/mimikatz/dpapi.py for each, machine keys, offline hashcat cracking), browser creds (SharpChrome interactive/offline/remote for Chrome/Edge, Firefox key4.db/logins.json, mimikatz dpapi::chrome), additional sources (vault detailed, Sticky Notes SQLite, VNC, McAfee SiteList.xml, cloud cred files, alternate data streams), escalation routing. Clear scope distinction from AD-level credential-dumping skill.
  - `windows-kernel-exploits` (615 lines) — 8-step workflow: assess OS/patch/drivers, exploit-suggester (WES-NG primary with offline analysis, Watson on-target, legacy windows-exploit-suggester, triage by reliability/impact/crash risk), named kernel CVEs (PrintNightmare local LPE with SharpPrintNightmare/Invoke-Nightmare/mimikatz + remote via Impacket SMB, EternalBlue with nmap/netexec detection + Metasploit/standalone, MS16-032 secondary logon handle, MS15-051 Win32k, KiTrap0D, CVE-2019-1388 cert dialog, SMBGhost — quick reference table), BYOVD (Capcom.sys/RTCore64.sys/DBUtil, loldrivers.io reference, driver enumeration, generic token theft workflow with EPROCESS offset documentation, EDR bypass notes), privileged file write (DiagHub pre-1903, UsoDLLLoader 1903-2004, WerTrigger, WerMgr, MSI rollback file delete to SYSTEM via osk.exe HID.dll), named pipe + leaked handle exploitation (full C API workflow, common triggers, handle enumeration, shellcode injection and parent process spoofing), restricted shell escape (PowerShell CLM bypass, AppLocker LOLBin bypass via MSBuild/InstallUtil/regsvcs), escalation routing.
- Updated windows-discovery with OPSEC guidance for whoami/whoami /priv (CrowdStrike detection). Added .NET-based alternatives for privilege enumeration and context-based privilege inference section.
- Updated README.md: 6 privesc skills (was 3), updated line counts, status line (52 skills, ~25,700 lines), Planned section (5 remaining instead of 8).
- Updated task_plan.md: Batch 2 skills marked complete with line counts and technique summaries.

### Inventory

- Total skills: 52 (29 web + 16 AD + 6 privesc + 1 orchestrator)
- Total lines: ~25,700
- Phase 5 Batch 2: COMPLETE (3/3 skills built, 1,716 lines)
- Remaining: Batch 3 (3 Linux foundation), Batch 4 (2 Linux extended)

### Next: Build Batch 3 (Linux Foundation — 3 skills)

**Branch**: `skills/privesc`

**Batch 3 skills to build:**
1. `linux-discovery` — LinPEAS/LinEnum/pspy enumeration, routing to 4 technique skills
2. `linux-sudo-suid-capabilities` — Sudo misconfig, SUID/SGID exploitation, Linux capabilities
3. `linux-cron-service-abuse` — Cron exploitation, systemd timer abuse, D-Bus, Unix sockets

---

## 2026-02-23 — Phase 5 Batch 1: Windows Foundation Skills

### Done

- Built 3 Windows Foundation privesc skills (Batch 1) on `skills/privesc` branch:
  - `windows-privesc-discovery` (489 lines) — 9-step enumeration workflow: system info (systeminfo/ver), user context (whoami /priv /groups with privilege-to-skill routing table), services (sc query/accesschk/wmic for unquoted paths + weak perms), scheduled tasks (schtasks + autorun + AlwaysInstallElevated), network (netstat/ipconfig + internal-only listeners), credential hunting (cmdkey/registry/unattend/PS history/HiveNightmare check), security controls (AV detection/PPL/Credential Guard/UAC level/AppLocker), automated tools (WinPEAS/PowerUp/Seatbelt/PrivescCheck/JAWS), routing decision tree mapping findings to 5 technique skills
  - `windows-token-impersonation` (440 lines) — Potato family decision tree by OS version: JuicyPotato (pre-1809 with CLSID), PrintSpoofer (simplest, needs Spooler), GodPotato/SigmaPotato (broadest support), RoguePotato (fake OXID resolver), EfsPotato (MS-EFSR pipe fallback chain), JuicyPotatoNG (modern DCOM), PrintNotifyPotato (works with Spooler disabled). FullPowers for stripped service accounts. Dangerous privilege exploitation: SeDebug (token theft from SYSTEM process + LSASS dump), SeBackup (SAM/SYSTEM hive extraction via reg save), SeRestore (arbitrary file write for DLL/binary replace), SeTakeOwnership (ownership → DACL chain), SeLoadDriver (vulnerable kernel driver loading), SeManageVolume (raw volume read bypassing NTFS). Potato variant decision tree diagram.
  - `windows-service-dll-abuse` (532 lines) — Service exploitation: unquoted paths (wmic/PowerUp enumeration + path hijacking), weak permissions (accesschk enumeration + sc config binpath), service registry ACL abuse (ImagePath modification), service binary replacement. Service triggers: named pipe/ETW/RPC/GPO/IP-available trigger types with firing commands. DLL hijacking: search order documentation, Process Monitor filter setup, PowerUp DLL checks, writable PATH enumeration. DLL exploitation: 4 DLL payload templates (basic/user-creation/threaded/msfvenom), DLL proxying (DLLirant/Spartacus), COM DLL hijacking (InprocServer32 HKCU write), writable system PATH injection. Auto-updater/IPC abuse section. 8-step workflow.
- Updated README.md:
  - Added Privilege Escalation skills table (3 skills)
  - Added "Running Claude Code for pentesting" section (Trail of Bits config, VM recommendation)
  - Added baseline skills customization note
  - Updated status line (49 skills, ~24,000 lines)
  - Updated Planned section (8 remaining privesc skills)
- Updated task_plan.md — marked Batch 1 skills complete with line counts

### Inventory

- Total skills: 49 (29 web + 16 AD + 3 privesc + 1 orchestrator)
- Total lines: ~24,000
- Phase 5 Batch 1: COMPLETE (3/3 skills built, 1,461 lines)
- Remaining: Batch 2 (3 Windows extended), Batch 3 (3 Linux foundation), Batch 4 (2 Linux extended)

### Next: Build Batch 2 (Windows Extended — 3 skills)

**Branch**: `skills/privesc`

**Batch 2 skills to build:**
1. `windows-uac-bypass` (~350-400 lines) — UAC bypass techniques, COM hijacking, AlwaysInstallElevated, autorun
2. `windows-credential-harvesting` (~400-450 lines) — HiveNightmare, DPAPI, PS history, unattend, browser creds, vaults
3. `windows-kernel-exploits` (~400-450 lines) — Kernel CVEs, exploit-suggesters, BYOVD, named pipe impersonation, restricted shell

---

## 2026-02-23 — Phase 5 Source Material Survey: Privilege Escalation

### Done

- Surveyed all 5 source material directories for privesc content:
  - **HackTricks Windows**: 26 files + DLL subdir (6,000+ lines). Potato family (5 variants, 598 lines), DLL hijacking (694 lines), DPAPI (500 lines), leaked handles (696 lines), UAC (275 lines), plus credentials/NTLM supporting dirs.
  - **HackTricks Linux**: 46 files + kernel subdir (8,000+ lines). Capabilities (1,700 lines — massive), Docker/container section (14 files, 3,500+ lines), D-Bus (540 lines), groups (288 lines), restricted shell escape (296 lines), wildcards (255 lines).
  - **HackTricks macOS**: 70+ files, 14,000+ lines — far exceeded expectations. TCC bypass (2,275 lines with 20+ techniques), SIP bypass (284 lines, 8+ CVEs), Gatekeeper (571 lines, 11+ CVEs), dylib hijacking (169 lines), XPC/Mach IPC (1,323 lines), sandbox escape (507 lines), Electron injection (511 lines).
  - **InternalAllTheThings**: linux-privilege-escalation.md (868 lines), windows-privilege-escalation.md (1,565 lines). Complementary to HT — more actionable checklists, Potato CLSID tables, BYOVD driver names.
  - **PayloadsAllTheThings**: Minimal — just 2 redirect pages (118 lines total) pointing to IATT. No standalone privesc content.

- Defined concrete skill splits: 11 skills total (macOS removed — never used in engagements)
  - **Windows** (6): 1 discovery + 5 technique (token impersonation, service/DLL, UAC bypass, credential harvesting, kernel exploits)
  - **Linux** (5): 1 discovery + 4 technique (sudo/SUID/capabilities, cron/service/D-Bus, file/path abuse, kernel exploits)

- Defined batching: 4 batches by platform
  - Batch 1: Windows Foundation (3 skills — discovery, token impersonation, service/DLL)
  - Batch 2: Windows Extended (3 skills — UAC, credentials, kernel)
  - Batch 3: Linux Foundation (3 skills — discovery, sudo/SUID/caps, cron/service)
  - Batch 4: Linux Extended (2 skills — file/path abuse, kernel exploits)

### Key Decisions

- **macOS removed**: Never used in engagements. Deep source material exists (14,000+ lines in HT) but not worth building.
- **Docker/container escapes**: Large section in Linux HT survey (3,500+ lines) but belongs in Phase 6 (Containers). Docker/LXD *group escape* included in `linux-file-path-abuse` as a common privesc vector; full container escape coverage deferred.
- **Credential harvesting vs. credential dumping**: Phase 5 `windows-credential-harvesting` focuses on LOCAL credential discovery (DPAPI, history, vaults, HiveNightmare). Phase 4 `credential-dumping` covers AD-level extraction (DCSync, NTDS, LAPS, gMSA). Distinct scopes with minimal overlap.
- **Capabilities standalone vs. combined**: Despite being 1,700 lines in HT, capabilities folded into `linux-sudo-suid-capabilities` — same enumeration workflow (check what binaries have elevated privs → exploit via GTFOBins or technique-specific abuse).
- **Linux restricted shell escape**: Folded into `linux-kernel-exploits` rather than standalone — it's a pre-requisite technique (getting a proper shell before exploiting kernel bugs), and 296 lines alone is thin for a skill.
- **Discovery skills**: Platform-specific (not a single privesc discovery) because the user knows their target OS. Windows and Linux each get a discovery skill.

### Source Material Comparison

| Platform | HackTricks | InternalAllTheThings | PayloadsAllTheThings |
|----------|-----------|---------------------|---------------------|
| Windows | 6,000+ lines (deep technique coverage, PoC code) | 1,565 lines (actionable checklists, CLSID tables) | Redirect only |
| Linux | 8,000+ lines (capabilities alone 1,700, D-Bus 540) | 868 lines (systematic, tool-heavy) | Redirect only |
| macOS | 14,000+ lines (TCC 2,275, XPC 1,323, Gatekeeper 571) | N/A (no macOS content) | N/A |

HT is the primary source for all 3 platforms. IATT is complementary for Windows/Linux. PAT has no useful privesc content.

### Inventory

- Total skills: 46 (29 web + 16 AD + 1 orchestrator)
- Phase 5 planned: 11 skills (6 Windows + 5 Linux)
- Phase 5 will bring total to 57 skills, ~28,000+ estimated lines

### Next: Build Batch 1 (Windows Foundation — 3 skills)

**Branch**: `skills/privesc`

**Batch 1 skills to build** (detailed specs in task_plan.md):
1. `windows-privesc-discovery` (~400-500 lines) — Enumeration hub (WinPEAS/PowerUp/Seatbelt/Watson/WES-NG), 7-step enumeration workflow, routing table to 5 technique skills. Source: HT README.md (1,961 lines) + IATT (1,565 lines).
2. `windows-token-impersonation` (~500-550 lines) — Potato family decision tree by Windows version (7 variants with exact commands), dangerous privileges (SeImpersonate/SeDebug/SeBackup/SeManageVolume/SeLoadDriver/SeRestore each with exploitation), FullPowers. Source: HT juicypotato.md + roguepotato.md + token-abuse.md + seimpersonate.md + sedebug.md + semanagevolume.md + IATT token section.
3. `windows-service-dll-abuse` (~450-500 lines) — Unquoted paths, weak service perms (binpath/registry ACL), DLL hijacking (search order/PATH/side-loading/COM/proxying), auto-updater abuse. Source: HT dll-hijacking/ (694 lines) + service-triggers.md + auto-updaters.md + IATT service/DLL sections.

---

## 2026-02-23 — Phase 4 AD Batch 5: Trust & Persistence Skills (FINAL CORE AD BATCH)

### Done

- Built 3 AD Batch 5 skills (Trust & Persistence) on `skills/ad` branch:
  - `trust-attacks` (464 lines) — Trust enumeration (nltest/PowerView/AD Module/NetExec with 5 critical trust properties: SIDFilteringQuarantined, SelectiveAuthentication, ForestTransitive, TrustDirection, TGTDelegation), cross-domain group membership enumeration. SID history injection child→parent via golden ticket + extra SID (Mimikatz AES256 preferred, Rubeus diamond ticket for OPSEC, Impacket ticketer.py, raiseChild.py automation). Inter-realm TGT forging (trust key extraction via lsadump::trust, referral ticket creation + service ticket request in target domain, trust account authentication for Kerberoasting). Cross-forest abuse (trust account auth + Kerberoasting, cross-forest RBCD via S4U, SID filtering bypass assessment). PAM trust exploitation (shadow principal enumeration + group membership manipulation via bloodyAD/Set-ADObject). PAC validation considerations (CVE-2024-26248/29056 enforcement mode vs compatibility mode). Trust type decision tree routing by trust type and SID filtering status.
  - `sccm-exploitation` (510 lines) — SCCM enumeration (sccmhunter find/show/http, SharpSCCM, 3 unauthenticated MP HTTP endpoints). NAA extraction 3 methods: CRED-2 policy request (addcomputer.py + sccmwtf + policysecretunobfuscate.py), CRED-3 WMI/DPAPI (SharpSCCM local secrets / SharpDPAPI), CRED-4 WMI repository (SharpDPAPI search / SharpSCCM disk). MP relay to MSSQL TAKEOVER-1 (ntlmrelayx SOCKS + PetitPotam coercion, RBAC_Admins SQL insertion for admin, OSD policy secret extraction via stored procs + PXEthief decryption). Client push relay ELEVATE-2 (SharpSCCM invoke client-push + ntlmrelayx). PXE boot harvesting CRED-1 (pxethiefy/SharpPXE + Hashcat 31100). Database extraction CRED-5 (Mimikatz misc::sccm / SQLRecon). Application deployment (MalSCCM full chain: locate→inspect→group→app→deploy→checkin→cleanup, SharpSCCM exec). Share looting (CMLoot SCCMContentLib$). Decision tree by access level. OPSEC comparison table for all 11 techniques.
  - `ad-persistence` (600 lines) — Golden Certificate (CA key extraction 3 methods, forge with certipy/ForgeCert/Certify + SID embedding for KB5014754, certificate renewal + enrollment agent as persistence tokens). DCShadow (dual mimikatz, 4 attribute modification examples: SIDHistory/primaryGroupID/Description/AdminSDHolder ntSecurityDescriptor, /stack batching, delegated DCShadow via Set-DCShadowPermissions). Skeleton Key (misc::skeleton, PPL bypass via !processprotect + mimidrv.sys, /letaes for AES compatibility, must apply to all DCs, lost on reboot). Custom SSP (mimilib.dll persistent via Security Packages registry + memssp in-memory non-persistent). Security descriptor backdoors (WMI via Set-RemoteWMI, WinRM via Set-RemotePSRemoting, registry DAMP for remote hash retrieval). ADFS Golden SAML (DKM key from AD contact object, ADFSDump WID, ADFSpoof/Shimit/WhiskeySAML, O365 forging, 2FA bypass). SID history persistence 3 methods (DCShadow/golden ticket/direct). Persistence decision tree with 9 techniques ranked by stealth and reboot survival. Verification steps for each mechanism.

### Conventions Applied

- `trust-attacks`: Kerberos-first for enumeration and tool execution. Trust ticket attacks use AES256 when available. Diamond ticket recommended over golden for OPSEC. PAC validation enforcement documented for 2025+ environments.
- `sccm-exploitation`: Kerberos-first for enumeration. OPSEC exception documented for relay attacks (TAKEOVER-1, ELEVATE-2) — inherently NTLM. Attack path decision tree routes by access level (domain user → local admin → relay position → SCCM admin → DB access).
- `ad-persistence`: Kerberos-first for remote operations. Skeleton key OPSEC exception (LSASS injection, local to DC). Golden certificate uses PKINIT for authentication. ADFS Golden SAML is federation-layer (not Kerberos). All techniques include cleanup/removal steps.
- All skills include Mode, Engagement Logging, State Management sections per template
- Discovery skill (`ad-attack-discovery`) already routes to all 3 Batch 5 skills (lines 437-439: trusts → trust-attacks, SCCM → sccm-exploitation, post-DA → ad-persistence)
- Updated README name/tagline to reference "redteam runbook" origin

### Inventory

- Total skills: 46 (29 web + 16 AD + 1 orchestrator)
- Total lines: ~22,500
- Phase 4 core: COMPLETE (all 5 batches, 16 AD skills built)
- Phase 4 Batch 5: COMPLETE (3/3 skills built, 1574 lines)
- Remaining: Phase 4b (6 extended AD skills), then Phase 5 (Privilege Escalation)

### Next: Phase 4b Extended AD Skills (6 skills) or Phase 5

**Phase 4b candidates:**
1. `adidns-poisoning` — Dynamic DNS record injection, wildcard records, WPAD hijack
2. `dcom-lateral-movement` — DCOM-based remote execution (MMC20, ShellWindows, ShellBrowserWindow)
3. `rodc-exploitation` — RODC enumeration, Kerberos Key List Attack
4. `ad-named-cves` — NoPAC, PrintNightmare, ZeroLogon, PrivExchange, MS14-068
5. `mssql-ad-abuse` — Linked server hopping, xp_cmdshell, impersonation chains, UNC path injection
6. `deployment-targets` — MDT bootstrap creds, WSUS update poisoning, SCOM RunAs decryption

**Phase 5**: Privilege Escalation (Windows, Linux, macOS)

---

## 2026-02-23 — Phase 4 AD Batch 4: Relay & Credentials Skills

### Done

- Built 3 AD Batch 4 skills (Relay & Credentials) on `skills/ad` branch:
  - `auth-coercion-relay` (581 lines) — 6 coercion methods (PetitPotam MS-EFSR, PrinterBug MS-RPRN, DFSCoerce MS-DFSNM, ShadowCoerce MS-FSRVP, CheeseOunce MS-EVEN, MSSQL xp_dirtree) with reference table and NetExec coerce_plus automation. NTLM relay to 4 targets (SMB code execution, LDAP machine account creation + RBCD, AD CS certificate enrollment, MSSQL command execution) with SOCKS proxy support. Kerberos relay 3 methods (krbrelayx + Responder LLMNR, krbrelayx + mitm6 IPv6 DNS, Kerberos reflection CVE-2025-33073). Name resolution poisoning (Responder LLMNR/NBNS/WPAD, mitm6 IPv6, Inveigh Windows). Hash capture with NTLMv1 downgrade (shuck.sh/crack.sh). Advanced relay techniques (Drop the MIC CVE-2019-1040, Ghost Potato CVE-2019-1384, NTLM reflection CVE-2025-33073). Signing requirement assessment workflow (SMB signing by OS, LDAP signing check, AD CS enrollment check, WebClient status).
  - `credential-dumping` (603 lines) — DCSync (targeted single user + full domain via secretsdump/mimikatz/NetExec, replication rights verification). NTDS extraction 3 methods (VSS via secretsdump -use-vss, ntdsutil IFM, vssadmin manual + offline secretsdump). SAM dump (remote via secretsdump/NetExec, manual hive export, LSA secrets + cached domain creds). LAPS (legacy ms-Mcs-AdmPwd plaintext read via NetExec/bloodyAD/PowerView + Windows LAPS 2023+ encrypted attribute with authorized decryption). gMSA (authorized read via NetExec/bloodyAD/gMSADumper/DSInternals + GoldenGMSA persistence via KDS root key extraction). dMSA BadSuccessor CVE-2025-21293 (GenericWrite on dMSA → set successor → read managed password). DSRM (DsrmAdminLogonBehavior registry + hash extraction via secretsdump/mimikatz). GPP passwords MS14-025 (Get-GPPPassword/NetExec/manual openssl AES decryption with published Microsoft key). OPSEC comparison table for all 12 techniques.
  - `gpo-abuse` (532 lines) — GPO enumeration (GPOHound dump/analysis, BloodHound edge detection, PowerView ACL scan, NetExec gpo_enum). Exploitation via 7 methods: immediate tasks (SharpGPOAbuse/PowerGPOAbuse/pyGPOAbuse/GroupPolicyBackdoor with state-based cleanup), startup/logon scripts, registry Run key via GPP, local admin assignment, user rights assignment (also StandIn tool). SYSVOL/NETLOGON logon script poisoning (VBS/BAT/PS1 prepend techniques preserving original script, write access verification). GPP password extraction (automated via Get-GPPPassword.py/NetExec + manual SYSVOL search and openssl decryption). Cleanup section (GroupPolicyBackdoor state restore + manual procedures). GPO refresh timing (90 min + random offset, DC 5 min).

### Conventions Applied

- `auth-coercion-relay`: Explicit OPSEC exception — relay/coercion is inherently network-level, Kerberos-first does not apply to the attack itself. Enumeration commands still use -k -no-pass.
- `credential-dumping`: Kerberos-first for all remote operations (secretsdump -k -no-pass, bloodyAD -k -no-pass, NetExec --use-kcache). Filesystem operations (SAM/NTDS hive extraction) exempt.
- `gpo-abuse`: pyGPOAbuse uses -hashes, GroupPolicyBackdoor supports -k. Windows tools use domain session. GPP extraction via Get-GPPPassword.py -k -no-pass.
- All skills include Mode, Engagement Logging, State Management sections per template
- Discovery skill (`ad-attack-discovery`) already routes to all 3 Batch 4 skills (SMB signing -> auth-coercion-relay, DCSync rights/LAPS/gMSA -> credential-dumping, GPO write -> gpo-abuse)

### Inventory

- Total skills: 43 (29 web + 13 AD + 1 orchestrator)
- Total lines: ~20,700
- Phase 4 Batch 4: COMPLETE (3/3 skills built, 1716 lines)
- Remaining: Batch 5 (3 skills), Phase 4b (6 extended skills)

### Next Session: Build Batch 5 (Trust & Persistence — 3 skills)

**Branch**: `skills/ad`

**Batch 5 skills to build:**

1. `trust-attacks` — Trust enumeration (nltest, PowerView), SID history injection (child -> forest), inter-realm TGT forging, PAM trust exploitation, cross-forest trust abuse
2. `sccm-exploitation` — SCCM enumeration (SharpSCCM, sccmhunter), management point relay, client push exploitation, credential harvesting
3. `ad-persistence` — DCShadow, skeleton key, custom SSP, ADFS Golden SAML, AdminSDHolder ACL backdoors

**After Batch 5**: Phase 4b (6 extended AD skills), then Phase 5 (Privilege Escalation).

---

## 2026-02-23 — Phase 4 AD Batch 3: ADCS Skills

### Done

- Built 3 AD Batch 3 skills (ADCS) on `skills/ad` branch:
  - `adcs-template-abuse` (457 lines) — ESC1 (enrollee-supplies-subject, SAN manipulation via Certipy `-upn`/Certify `/altname`, SID pinning for KB5014754 patched systems), ESC2 (Any Purpose EKU direct exploitation + No EKU subordinate CA implications), ESC3 (two-step enrollment agent: agent cert request + on-behalf-of enrollment for arbitrary user), ESC6 (EDITF_ATTRIBUTESUBJECTALTNAME2 CA flag enabling SAN via attribute on any template including default User, certreq.exe native exploitation). Shared enumeration (Certipy find -vulnerable, Certify find /enrolleeSuppliesSubject, NetExec LDAP adcs module), PKINIT/Schannel/LDAPS auth chains, UnPAC the Hash for NT hash extraction, certificate format conversion (PEM↔PFX). Decision tree routing by ESC variant, OPSEC comparison table.
  - `adcs-access-and-relay` (475 lines) — ESC4 (template ACL abuse: modify via modifyCertTemplate.py/Certipy template/StandIn.exe + exploit as ESC1 + restore via `-save-old`/`-configuration`), ESC5 (PKI container write: create/publish malicious template or golden cert via CA key), ESC7 (ManageCA: add self as officer → enable SubCA → request/issue/retrieve cycle, enable ESC6 flag, RCE via CRL/file write; ManageCertificates: extension injection on pending requests), ESC8 (NTLM relay to HTTP enrollment: ntlmrelayx `--adcs` + Certipy relay + PetitPotam/SpoolSample/DFSCoerce coercion, Kerberos relay variant via krbrelayx + mitm6), ESC11 (NTLM relay to ICPR RPC: certipy relay `-target rpc://` + ntlmrelayx `-rpc-mode ICPR`). ESC8 vs ESC11 comparison table. Explicit OPSEC exception for relay attacks (inherently NTLM, Kerberos-first N/A). Cleanup commands for ESC4/ESC7.
  - `adcs-persistence` (611 lines) — Golden Certificate (CA key extraction via certipy ca -backup/certutil -backupKey/mimikatz crypto, forge with Certipy/ForgeCert/Certify including -sid + -crl for KB5014754 Full Enforcement), user/machine cert persistence + renewal for extended lifetime, ESC9 (CT_FLAG_NO_SECURITY_EXTENSION + GenericWrite UPN swap via shadow credentials chain), ESC10 (StrongCertificateBindingEnforcement=0 bypass + CertificateMappingMethods UPN variant for computer account mapping), ESC12 (YubiHSM CA key extraction from registry + certutil CSP signing), ESC13 (issuance policy OID group link → automatic group membership in TGT), ESC14 (altSecIdentities explicit mapping with 6 format types: 3 strong + 3 weak, KB5014754 compatibility), ESC15/CVE-2024-49019 (application policies override on schema v1 templates: WebServer → Client Auth injection, Certificate Request Agent OID injection), certificate theft THEFT1-5 (CAPI/CNG patching via mimikatz, DPAPI user masterkey + SharpDPAPI, machine DPAPI_SYSTEM + LSA secret, filesystem PFX search + pfx2john cracking, UnPAC the Hash from PKINIT TGT), KB5014754 enforcement impact table by technique. OPSEC comparison table for all persistence methods.

### Conventions Applied

- All 3 skills follow Kerberos-first auth convention where applicable
- `adcs-template-abuse`: All enumeration and certificate requests use -k -no-pass; PKINIT preferred for authentication
- `adcs-access-and-relay`: Kerberos-first for ACL-based ESCs (4/5/7); explicit OPSEC exception for relay ESCs (8/11) — NTLM detection accepted as necessary cost
- `adcs-persistence`: PKINIT for certificate auth; KB5014754 SID embedding documented for golden cert and mapping techniques
- All skills include Mode, Engagement Logging, State Management sections per template
- Discovery skill (`ad-attack-discovery`) already routes to all 3 ADCS skills (lines 424-427)

### Inventory

- Total skills: 40 (29 web + 10 AD + 1 orchestrator)
- Total lines: ~19,000
- Phase 4 Batch 3: COMPLETE (3/3 skills built, 1543 lines)
- Remaining: Batches 4-5 (6 skills), Phase 4b (6 extended skills)

### Next Session: Build Batch 4 (Relay & Credentials — 3 skills)

**Branch**: `skills/ad`

**Batch 4 skills to build:**

1. `auth-coercion-relay` — PetitPotam, PrinterBug, DFSCoerce, ShadowCoerce, NTLM relay (ntlmrelayx to LDAP/SMB/ADCS/MSSQL), Kerberos relay (krbrelayx, mitm6), LLMNR/NBNS poisoning (Responder)

2. `credential-dumping` — DCSync, NTDS extraction, SAM dump, LAPS, gMSA, dMSA (BadSuccessor), DSRM

3. `gpo-abuse` — GPO enumeration (GPOHound), SharpGPOAbuse, SYSVOL/NETLOGON poisoning

**After Batch 4**: Batch 5 (Trust & Persistence, 2 skills), then Phase 4b (6 extended skills).

---

## 2026-02-23 — Phase 4 AD Batch 2: Kerberos & ACL Skills

### Done

- Built 3 AD Batch 2 skills on `skills/ad` branch:
  - `kerberos-delegation` (508 lines) — Unconstrained Delegation (TGT harvesting via SpoolService/PetitPotam/DFSCoerce coercion, krbrelayx for Linux-based capture, attacker-created computer with unconstrained flag), Constrained Delegation (S4U2Self + S4U2Proxy with Impacket getST.py and Rubeus, SPN swapping via /altservice for LDAP/CIFS/HTTP/HOST/WSMAN, cross-domain S4U), RBCD (machine account creation, msDS-AllowedToActOnBehalfOfOtherIdentity setup via rbcd.py/bloodyAD/PowerView, S4U exploitation, cleanup commands). Decision tree by finding type, enumeration for all 3 types, OPSEC comparison table.
  - `kerberos-ticket-forging` (463 lines) — Golden Ticket (Impacket ticketer.py/Rubeus/mimikatz with AES256 preferred, cross-forest via extra-sid, realistic lifetime tuning), Silver Ticket (service-specific TGS forging, common SPN target table with exploitation examples, KB5021131 AES enforcement note, duration flag), Diamond Ticket (legitimate TGT decrypt/modify PAC/re-encrypt, Rubeus /tgtdeleg /ldap /opsec flags, Impacket -request flag, service ticket re-cutting), Sapphire Ticket (U2U S4U2Self PAC swap technique, Impacket --u2u --s4u2self), Pass-the-Ticket (ccache/kirbi conversion, Linux/Windows injection). Ticket type decision table ranked by OPSEC, comparison table.
  - `acl-abuse` (554 lines) — Enumeration (bloodyAD writable objects, PowerView ACL scanner, BloodHound cypher queries), GenericAll/GenericWrite on User (4 options ranked by OPSEC: shadow credentials via pywhisker/bloodyAD/Certipy + PKINIT + S4U2Self for computer accounts, targeted Kerberoasting via SPN manipulation, ASREPRoast via UAC modification, logon script path), GenericAll on Group (add to privileged group), WriteDACL (DCSync rights grant, GenericAll grant, OU inheritance via dacledit.py), WriteOwner (ownership + DACL chain), ForceChangePassword (destructive last resort), Computer write → RBCD (routes to kerberos-delegation), AdminSDHolder persistence (SDProp propagation backdoor). Decision tree by ACL right + target type, OPSEC comparison table.

### Conventions Applied

- All 3 skills follow Kerberos-first auth convention from CLAUDE.md
- `kerberos-delegation`: All enumeration and exploitation uses -k -no-pass / --use-kcache; RBCD cleanup commands included
- `kerberos-ticket-forging`: Diamond/Sapphire preferred over Golden for OPSEC; AES256 mandatory for modern domains
- `acl-abuse`: Shadow credentials ranked first (lowest OPSEC); password reset marked destructive and ranked last; cleanup commands for every technique
- All skills include Mode, Engagement Logging, State Management sections per template

### Inventory

- Total skills: 37 (29 web + 7 AD + 1 orchestrator)
- Phase 4 Batch 2: COMPLETE (3/3 skills built)
- Remaining: Batches 3-5 (9 skills), Phase 4b (6 extended skills)

### Next Session: Build Batch 3 (ADCS — 3 skills)

**Branch**: `skills/ad`

**Batch 3 skills to build:**

1. `adcs-template-abuse` — ESC1 (enrollee-supplies-subject), ESC2 (any-purpose EKU), ESC3 (enrollment agent), ESC6 (EDITF_ATTRIBUTESUBJECTALTNAME2 flag). Template/CA flag misconfigurations. Sources: IATT 5 files + HT ad-certificates/domain-escalation.md (2000+ lines).

2. `adcs-access-and-relay` — ESC4 (template ACL → modify to ESC1), ESC5 (CA object ACLs), ESC7 (ManageCA/ManageCertificates), ESC8 (NTLM relay to HTTP enrollment), ESC11 (NTLM relay to ICPR). ACL abuse on CA/templates + relay to enrollment endpoints. Sources: IATT 5 files + HT domain-escalation.md.

3. `adcs-persistence` — ESC9-10 (weak cert mapping), ESC12-15, Golden Certificate, certificate theft, account persistence via certificate mapping. Sources: IATT 8 files + HT certificate-theft.md (500+) + domain-persistence.md (400+).

**After Batch 3**: Batch 4 (Relay & Credentials, 3 skills), Batch 5 (Trust & Persistence, 3 skills), then Phase 4b (6 extended skills).

---

## 2026-02-22 — Phase 4 AD Batch 1: Foundation Skills

### Done

- Built 4 AD foundation skills (Batch 1) on `skills/ad` branch:
  - `ad-attack-discovery` (511 lines) — domain enumeration at 3 access levels (unauth/username-only/full creds), BloodHound collection (bloodhound-python, rusthound-ce, SharpHound, SOAPHound), ADCS template enumeration (certipy), targeted enumeration (SPNs, delegation, ACLs, groups, LAPS/gMSA, trusts, shares, sessions, SCCM), full routing table mapping 30+ findings to 15 technique skills with OPSEC-prioritized order
  - `kerberos-roasting` (436 lines) — Kerberoasting (Impacket/Rubeus/NetExec/PowerView with OPSEC flags: /rc4opsec, /delay, /jitter, /pwdsetbefore), AS-REP Roasting (GetNPUsers.py/Rubeus/bloodyAD), kerberoasting without domain account (Charlie Clark technique via altered sname field), targeted kerberoasting (ACL abuse via targetedKerberoast.py), Timeroasting (timeroast.py, unauthenticated), cracking reference table (hashcat modes 13100/18200/19600/19700/31300)
  - `password-spraying` (508 lines) — lockout policy enumeration (NetExec/enum4linux/rpcclient/LDAP, plus Fine-Grained PSOs), smart password generation (season+year, company patterns, SpearSpray per-user templates), pre-spray badPwdCount safety check, Kerberos pre-auth spray (kerbrute/SpearSpray — Event 4771), NTLM spray fallback (NetExec multi-protocol: SMB/LDAP/WinRM/RDP/MSSQL), OWA spray (Ruler/MailSniper/Metasploit), empty password STATUS_PASSWORD_MUST_CHANGE technique, OPSEC exception documented
  - `pass-the-hash` (473 lines) — decision tree by credential material (AES key → PTK, NTLM hash → OPTH, ticket → PTT, last resort → direct PTH), Pass-the-Key with AES256 (/opsec flag, etype 0x12 = normal traffic), Over-Pass-the-Hash (getTGT.py -hashes + Rubeus /rc4:), Pass-the-Ticket (ccache/kirbi conversion, ticket injection), Direct PTH (NetExec -H, Impacket -hashes, mimikatz sekurlsa::pth, RDP Restricted Admin), lateral movement tool comparison (psexec/smbexec/wmiexec/atexec/dcomexec noise levels), OPSEC comparison summary table

### Conventions Applied

- All 4 skills follow Kerberos-first auth convention from CLAUDE.md
- `ad-attack-discovery`: Notes it may start unauthenticated; switches to Kerberos once creds obtained
- `password-spraying`: Documents OPSEC exception (testing credentials = Kerberos-first doesn't apply)
- `kerberos-roasting`: Kerberos-first Prerequisites with getTGT.py workflow
- `pass-the-hash`: Defaults to AES/Kerberos techniques; direct NTLM PTH explicitly marked as last resort
- All skills include Mode, Engagement Logging, State Management sections per template

### Inventory

- Total skills: 34 (29 web + 4 AD + 1 orchestrator)
- Phase 4 Batch 1: COMPLETE (4/4 skills built)
- Remaining: Batches 2-5 (12 skills), Phase 4b (6 extended skills)

### Next Session: Build Batch 2 (Kerberos & ACL — 3 skills)

**Branch**: `skills/ad` (4 commits ahead of main, pushed to origin)

**Batch 2 skills to build:**

1. `kerberos-delegation` — Unconstrained (TGT harvesting + SpoolService coercion), Constrained (S4U2Self + S4U2Proxy), RBCD (msDS-AllowedToActOnBehalfOfOtherIdentity + low-priv path). 3 distinct attack paths with different prerequisites. Sources: IATT 3 files (280+ lines) + HT 3 files (2100+ lines).

2. `kerberos-ticket-forging` — Golden Ticket (krbtgt hash → forged TGT), Silver Ticket (service hash → forged TGS), Diamond Ticket (legitimate TGT decrypt/re-encrypt, OPSEC), Sapphire Ticket (U2U PAC swap), Pass-the-Ticket injection. Sources: IATT kerberos-tickets.md + HT golden-ticket.md (400+) + silver-ticket.md (900+) + diamond-ticket.md (500+).

3. `acl-abuse` — GenericAll, GenericWrite, WriteDACL, WriteOwner, ForceChangePassword, SPN manipulation (→ targeted Kerberoasting), shadow credentials (msDS-KeyCredentialLink → PKINIT), AdminSDHolder persistence. Sources: IATT ad-adds-acl-ace.md (200+ lines) + HT acl-persistence-abuse/README.md (2500+ lines).

**Workflow**: Survey source material for all 3 skills (parallel agents) → write skills → update task_plan.md/progress.md/README.md → commit + push.

**After Batch 2**: Batch 3 (ADCS, 3 skills), Batch 4 (Relay & Credentials, 3 skills), Batch 5 (Trust & Persistence, 3 skills), then Phase 4b (6 extended skills).

---

## 2026-02-22 — IDOR + CORS Misconfiguration Skills

### Done

- Built `idor` skill (569 lines) — horizontal/vertical access control bypass, UUID v1/MongoDB ObjectId prediction, API-specific patterns (REST/GraphQL/batch), encoding bypass, parameter pollution, method override, automated enumeration with ffuf/Python
- Built `cors-misconfiguration` skill (565 lines) — origin reflection, null origin (sandboxed iframe + data URI), regex bypass (unescaped dot, missing anchors, special characters), subdomain trust chain, wildcard abuse, CORS+IDOR chain, XSSI/JSONP bypass, cache poisoning
- Updated `web-vuln-discovery` — added IDOR and CORS detection probes to Step 3, routing tables to Step 4, deep references
- Updated `task_plan.md`, `README.md`, `progress.md`

- Built `csrf` skill (609 lines) — token bypass (remove/empty/untied/static), SameSite bypass (Lax GET, method override, 2-min window), Referer suppression and regex bypass, JSON CSRF (text/plain, sendBeacon), file upload CSRF, login CSRF, WebSocket CSRF (CSWSH), clickjacking chain, multi-action PoC chaining
- Built `oauth-attacks` skill (610 lines) — redirect URI manipulation (path traversal, open redirect chain, parameter pollution, special chars), state bypass (CSRF account linking), code theft (reuse, race condition, client binding), token leakage (Referer, postMessage, implicit flow), OIDC (email claim abuse, nonce bypass, discovery SSRF), PKCE bypass/downgrade, scope escalation, ROPC 2FA bypass, account takeover chains
- Updated `web-vuln-discovery` — added CSRF and OAuth detection probes to Step 3, routing tables to Step 4, deep references

- Built `password-reset-poisoning` skill (533 lines) — host header poisoning (Host/X-Forwarded-Host/double host/absolute URL), token leakage via Referer, email parameter injection (duplication/CRLF/separator/JSON array), token weakness analysis (sequential/timestamp/hash/UUID v1), brute-force with rate limit bypass, response manipulation, username enumeration, dangling markup, unicode normalization
- Built `2fa-bypass` skill (585 lines) — response manipulation (status code/body/redirect), direct navigation bypass, null/empty/array code submission, OTP brute-force with rate limit bypass (IP rotation/session rotation/code resend/HTTP/2 single-packet), backup code attacks, session fixation, remember-me token abuse, OAuth/SSO/ROPC bypass, CSRF on 2FA disable, race conditions

- Built `race-condition` skill (719 lines) — limit-overrun (coupon/balance/vote/invite), HTTP/2 single-packet attack (Burp Repeater + Turbo Intruder), HTTP/1.1 last-byte sync, asyncio+httpx PoCs, connection warming, multi-endpoint races (email change + verification), authentication races (password reset token reuse, 2FA code reuse, registration confirmation, email change verification), rate limit bypass (HTTP/2 multiplexing, GraphQL alias batching, session rotation), advanced (partial construction, race window expansion, session fixation chain, database TOCTOU, WebSocket races), session locking workaround
- Updated `web-vuln-discovery` — added race condition detection probes to Step 3, routing table to Step 4 (4 patterns), deep references

### Inventory

- Total skills: 30 (29 web + 1 orchestrator)
- Phase 3 technique skills: COMPLETE (all 27 web technique skills built)
- Remaining: final `web-vuln-discovery` review

- Final `web-vuln-discovery` review — cross-checked all 27 technique skills against Step 3 (probes), Step 4 (routing), and Deep Reference. Found 3 gaps:
  - Added `file-upload-bypass` detection probes to Step 3 (was the only skill without probes)
  - Added `sql-injection-stacked` routing entries to Step 4 (stacked queries + second-order)
  - Added `file-upload-bypass` deep reference paths (PayloadsAllTheThings + HackTricks)

### Phase 3 Status: COMPLETE

All 27 web technique skills built. Discovery skill reviewed and verified.

### Next Steps

- Phase 4 (AD) — survey complete, ready to build

---

## 2026-02-22 — Phase 4 AD Source Material Survey

### Done

- Surveyed `~/docs/InternalAllTheThings/docs/active-directory/` — 65+ files covering ADCS (17 files with ESC1-15), Kerberos delegation (3 deep), relay/coercion (4 deep), ACL/ACE (200+ lines), credential extraction (9 files), roasting (3 files), trust (4 files), deployment (4 files), CVEs (5 files)
- Surveyed `~/docs/hacktricks/src/windows-hardening/active-directory-methodology/` — 42 files + 2 subdirs (acl-persistence-abuse with 2500+ lines, ad-certificates with ESC1-10 + theft + persistence). HackTricks adds: Diamond/Sapphire tickets, OPSEC annotations (Event IDs), 2025 enforcement context (RC4 phase-out, PAC validation, cert mapping), DNS abuse depth, SCCM relay chain
- Surveyed `~/docs/PayloadsAllTheThings/` — minimal AD content, all redirects to InternalAllTheThings. Only LDAP injection (Phase 3b) relevant
- Defined 16 skill splits (1 discovery + 15 technique) based on source material depth and attack workflow clustering
- Defined 5 batches grouping skills by engagement phase and shared tooling
- Updated findings.md with detailed topic depth table, ADCS ESC breakdown, HackTricks unique value analysis
- Updated task_plan.md with full skill list, batching, source references per skill, and Phase 4b extended list

### Skill Split Decisions

- **Kerberos Roasting**: Kerberoasting + AS-REP combined (same workflow: enumerate → extract → crack). Timeroasting as thin subsection (only 16 lines in IATT).
- **Kerberos Delegation**: All 3 types in one skill (like sql-injection-blind covering boolean/time/OOB). Distinct attack paths but shared context.
- **Ticket Forging**: Golden + Silver + Diamond + Sapphire + PTT in one skill. All about forging/reusing tickets with stolen key material.
- **ADCS split into 3**: Template misconfig (ESC1-3,6), ACL+relay (ESC4-5,7-8,11), mapping+persistence (ESC9-15, golden cert, theft). Grouped by attack primitive, not by ESC number.
- **Auth Coercion + Relay in one skill**: Coercion and relay are a single workflow (coerce → relay → exploit). Includes NTLM relay, Kerberos relay, and LLMNR/NBNS poisoning.
- **Credential Dumping**: Combined DCSync, NTDS, LAPS, gMSA, dMSA into one skill (all about extracting stored credentials). Shadow credentials goes in ACL abuse (requires ACL write access).
- **Pass-the-Hash standalone**: Despite thin source material (136 lines), PTH/Over-PTH/PTK is used on every engagement and deserves visibility.
- **Phase 4b**: 6 extended skills for ADIDNS, DCOM, RODC, named CVEs, MSSQL AD abuse, deployment targets. Important but lower priority than core 16.

### Batch Rationale

1. **Foundation** (4): ad-attack-discovery, kerberos-roasting, password-spraying, pass-the-hash — techniques used on every engagement, builds the routing hub
2. **Kerberos & ACL** (3): delegation, ticket-forging, acl-abuse — advanced Kerberos + the ACL primitives that enable many attack chains
3. **ADCS** (3): template-abuse, access-and-relay, persistence — self-contained attack surface, shared tools (Certipy/Certify)
4. **Relay & Credentials** (3): auth-coercion-relay, credential-dumping, gpo-abuse — authentication chain attacks
5. **Trust & Persistence** (3): trust-attacks, sccm-exploitation, ad-persistence — domain boundaries + long-term access

### Observations

- InternalAllTheThings is the primary source (breadth + modern tooling). HackTricks is essential for OPSEC context and modern ticket variants.
- PayloadsAllTheThings has zero useful AD content — complete redirect to InternalAllTheThings.
- ADCS is the deepest single topic across all sources (17 IATT files + deep HT subdirectory). Could justify 4-5 skills but 3 provides the right granularity.
- HackTricks ACL subdirectory (2500+ lines) is the single most comprehensive file for AD privilege escalation.
- Timeroasting, RODC, and deployment targets (MDT/WSUS) have thin coverage — appropriate for Phase 4b.
- Tool ecosystem dominated by Rubeus, Impacket, mimikatz, bloodyAD, Certipy, NetExec — these will appear across almost every skill.

### OPSEC Convention: Kerberos-First Authentication

- Added convention to CLAUDE.md: all AD skills default to Kerberos auth via ccache to avoid NTLM-specific detections (Event 4776, CrowdStrike Identity Module PTH signatures)
- Each AD skill's Prerequisites section includes: `getTGT.py` → `export KRB5CCNAME` → tool flags (`-k -no-pass` for Impacket, `--use-kcache` for NetExec, `-k` for Certipy/bloodyAD)
- Over-Pass-the-Hash path included for when only an NTLM hash is available
- Exceptions documented: password-spraying (testing creds), auth-coercion-relay (NTLM is the attack), ad-attack-discovery (may start unauthenticated)

### Next Steps

- Build Batch 1: `ad-attack-discovery`, `kerberos-roasting`, `password-spraying`, `pass-the-hash`

---

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
