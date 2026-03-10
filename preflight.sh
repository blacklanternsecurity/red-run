#!/usr/bin/env bash
set -euo pipefail

# preflight.sh — Check attackbox dependencies for red-run
#
# Verifies that required tools, wordlists, and target-side binaries are
# available. Does NOT install anything — only reports what's missing with
# install hints.
#
# Usage:
#   bash preflight.sh              # full check
#   bash preflight.sh --category   # check one category
#   bash preflight.sh --list       # list available categories
#   bash preflight.sh --json       # machine-readable output

# ── Colors ──────────────────────────────────────────────────────────────────

if [[ -t 1 ]]; then
    GREEN=$'\033[0;32m'  RED=$'\033[0;31m'  YELLOW=$'\033[0;33m'
    CYAN=$'\033[0;36m'   BOLD=$'\033[1m'    DIM=$'\033[2m'
    RESET=$'\033[0m'
else
    GREEN="" RED="" YELLOW="" CYAN="" BOLD="" DIM="" RESET=""
fi

# ── Counters ────────────────────────────────────────────────────────────────

PASS=0 FAIL=0 WARN=0
JSON_MODE=false
JSON_RESULTS=()

# ── Helpers ─────────────────────────────────────────────────────────────────

pass() {
    PASS=$((PASS + 1))
    if $JSON_MODE; then
        JSON_RESULTS+=("{\"name\":\"$1\",\"status\":\"pass\",\"path\":\"$2\"}")
    else
        printf "  ${GREEN}✓${RESET} %-28s %s\n" "$1" "${DIM}${2}${RESET}"
    fi
}

fail() {
    FAIL=$((FAIL + 1))
    if $JSON_MODE; then
        JSON_RESULTS+=("{\"name\":\"$1\",\"status\":\"fail\",\"hint\":\"$2\"}")
    else
        printf "  ${RED}✗${RESET} %-28s %s\n" "$1" "${DIM}${2}${RESET}"
    fi
}

warn() {
    WARN=$((WARN + 1))
    if $JSON_MODE; then
        JSON_RESULTS+=("{\"name\":\"$1\",\"status\":\"warn\",\"hint\":\"$2\"}")
    else
        printf "  ${YELLOW}○${RESET} %-28s %s\n" "$1" "${DIM}${2}${RESET}"
    fi
}

section() {
    $JSON_MODE && return
    echo ""
    echo "${BOLD}${CYAN}[$1]${RESET}"
}

# Check if a command exists anywhere in PATH
has_cmd() { command -v "$1" &>/dev/null; }

# Find a command and print its path, or return 1
find_cmd() {
    local path
    path="$(command -v "$1" 2>/dev/null)" && echo "$path" && return 0
    return 1
}

# Check common locations for git-cloned repos
find_repo() {
    local name="$1"
    local dirs=(
        "$HOME/tools/$name"
        "$HOME/Tools/$name"
        "/opt/$name"
        "/usr/share/$name"
        "$HOME/$name"
        "$HOME/git/$name"
    )
    for d in "${dirs[@]}"; do
        [[ -d "$d" ]] && echo "$d" && return 0
    done
    return 1
}

# Check for a pipx-installed package
find_pipx() {
    local name="$1"
    local bin="${2:-$1}"
    local path
    # Check if the binary is in PATH (pipx puts them in ~/.local/bin/)
    path="$(find_cmd "$bin")" && echo "$path" && return 0
    # Check pipx list
    if has_cmd pipx && pipx list --short 2>/dev/null | grep -qi "^${name} "; then
        echo "pipx:${name}"
        return 0
    fi
    return 1
}

# Check for a Go binary
find_go() {
    local bin="$1"
    local path
    path="$(find_cmd "$bin")" && echo "$path" && return 0
    # Common Go binary locations
    for d in "$HOME/go/bin" "/usr/local/go/bin" "${GOPATH:-}/bin" "${GOBIN:-}"; do
        [[ -n "${d:-}" && -x "${d}/${bin}" ]] && echo "${d}/${bin}" && return 0
    done
    return 1
}

# ── Check functions ─────────────────────────────────────────────────────────

check_redrun_prereqs() {
    section "red-run prerequisites"

    local p
    # uv (required by install.sh)
    if p=$(find_cmd uv); then pass "uv" "$p"
    else fail "uv" "https://docs.astral.sh/uv/getting-started/installation/"; fi

    # Docker
    if p=$(find_cmd docker); then
        if docker info &>/dev/null 2>&1; then
            pass "docker (daemon running)" "$p"
        else
            warn "docker (daemon not running)" "$p — start with: sudo systemctl start docker"
        fi
    else fail "docker" "https://docs.docker.com/engine/install/"; fi

    # Docker images
    if has_cmd docker && docker info &>/dev/null 2>&1; then
        if docker image inspect red-run-nmap:latest &>/dev/null 2>&1; then
            pass "red-run-nmap image" "docker"
        else warn "red-run-nmap image" "run: ./install.sh"; fi

        if docker image inspect red-run-shell:latest &>/dev/null 2>&1; then
            pass "red-run-shell image" "docker"
        else warn "red-run-shell image" "run: ./install.sh"; fi
    fi

    # Python 3
    if p=$(find_cmd python3); then pass "python3" "$p"
    else fail "python3" "sudo apt install python3"; fi

    # Git
    if p=$(find_cmd git); then pass "git" "$p"
    else fail "git" "sudo apt install git"; fi

    # pipx (needed for many tools)
    if p=$(find_cmd pipx); then pass "pipx" "$p"
    else warn "pipx" "sudo apt install pipx"; fi

    # Go (needed for nuclei, httpx, ffuf, etc.)
    if p=$(find_cmd go); then pass "go" "$p"
    else warn "go" "sudo apt install golang-go"; fi

    # Node/npm (needed for domdig)
    if p=$(find_cmd npm); then pass "npm" "$p"
    else warn "npm" "sudo apt install npm"; fi
}

check_network_scanning() {
    section "Network scanning and enumeration"

    local p
    if p=$(find_cmd nmap); then pass "nmap" "$p"
    else fail "nmap" "sudo apt install nmap"; fi

    if p=$(find_go nuclei); then pass "nuclei" "$p"
    else fail "nuclei" "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"; fi

    if p=$(find_go httpx); then pass "httpx" "$p"
    else fail "httpx" "go install github.com/projectdiscovery/httpx/cmd/httpx@latest"; fi

    if p=$(find_pipx netexec nxc); then pass "netexec (nxc)" "$p"
    else fail "netexec (nxc)" "pipx install netexec"; fi

    if p=$(find_pipx enum4linux-ng); then pass "enum4linux-ng" "$p"
    else warn "enum4linux-ng" "pipx install enum4linux-ng"; fi

    if p=$(find_pipx manspider); then pass "manspider" "$p"
    else warn "manspider" "pipx install manspider"; fi

    if p=$(find_cmd snmpwalk); then pass "snmpwalk" "$p"
    else warn "snmpwalk" "sudo apt install snmp"; fi

    if p=$(find_cmd onesixtyone); then pass "onesixtyone" "$p"
    else warn "onesixtyone" "sudo apt install onesixtyone"; fi
}

check_web_testing() {
    section "Web application testing"

    local p
    if p=$(find_go ffuf); then pass "ffuf" "$p"
    else fail "ffuf" "go install github.com/ffuf/ffuf/v2@latest"; fi

    if p=$(find_cmd sqlmap); then pass "sqlmap" "$p"
    else fail "sqlmap" "sudo apt install sqlmap"; fi

    if p=$(find_cmd wpscan); then pass "wpscan" "$p"
    else warn "wpscan" "sudo gem install wpscan"; fi

    if p=$(find_pipx arjun); then pass "arjun" "$p"
    else warn "arjun" "pipx install arjun"; fi

    if p=$(find_cmd commix); then pass "commix" "$p"
    else warn "commix" "sudo apt install commix"; fi

    if p=$(find_go dalfox); then pass "dalfox" "$p"
    else warn "dalfox" "go install github.com/hahwul/dalfox/v2@latest"; fi

    if p=$(find_repo XSStrike); then pass "XSStrike" "$p"
    else warn "XSStrike" "git clone https://github.com/s0md3v/XSStrike.git"; fi

    if p=$(find_pipx sstimap); then pass "sstimap" "$p"
    else warn "sstimap" "pipx install sstimap"; fi

    if p=$(find_repo tplmap); then pass "tplmap" "$p"
    else warn "tplmap" "git clone https://github.com/epinna/tplmap.git"; fi

    if p=$(find_go TInjA); then pass "TInjA" "$p"
    else warn "TInjA" "go install github.com/Hackmanit/TInjA@latest"; fi

    if p=$(find_pipx fenjing); then pass "fenjing" "$p"
    else warn "fenjing" "pipx install fenjing"; fi

    if p=$(find_repo SSRFmap); then pass "SSRFmap" "$p"
    else warn "SSRFmap" "git clone https://github.com/swisskyrepo/SSRFmap.git"; fi

    if p=$(find_repo Gopherus || find_repo gopherus); then pass "gopherus" "$p"
    else warn "gopherus" "git clone https://github.com/tarunkant/Gopherus.git"; fi

    if p=$(find_go interactsh-client); then pass "interactsh-client" "$p"
    else warn "interactsh-client" "go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"; fi

    if p=$(find_go xxeserv); then pass "xxeserv" "$p"
    else warn "xxeserv" "go install github.com/staaldraad/xxeserv@latest"; fi

    if p=$(find_repo XXEinjector); then pass "XXEinjector" "$p"
    else warn "XXEinjector" "git clone https://github.com/enjoiz/XXEinjector.git"; fi

    if p=$(find_pipx jwt_tool jwt_tool); then pass "jwt-tool" "$p"
    elif p=$(find_cmd jwt_tool); then pass "jwt-tool" "$p"
    else warn "jwt-tool" "pipx install jwt-tool"; fi

    if p=$(find_cmd domdig); then pass "domdig" "$p"
    else warn "domdig" "npm install -g domdig"; fi

    if p=$(find_repo php_filter_chain_generator); then pass "php_filter_chain_gen" "$p"
    else warn "php_filter_chain_gen" "git clone https://github.com/synacktiv/php_filter_chain_generator.git"; fi
}

check_deserialization() {
    section "Deserialization"

    local p
    # ysoserial — check for JAR file
    if compgen -G "$HOME/tools/**/ysoserial*.jar" >/dev/null 2>&1 ||
       compgen -G "/opt/**/ysoserial*.jar" >/dev/null 2>&1 ||
       compgen -G "/usr/share/**/ysoserial*.jar" >/dev/null 2>&1; then
        pass "ysoserial (Java)" "found .jar"
    else warn "ysoserial (Java)" "download JAR from https://github.com/frohoff/ysoserial"; fi

    if p=$(find_repo marshalsec); then pass "marshalsec" "$p"
    else warn "marshalsec" "git clone + mvn package"; fi

    if p=$(find_repo phpggc); then pass "phpggc" "$p"
    elif p=$(find_cmd phpggc); then pass "phpggc" "$p"
    else warn "phpggc" "git clone https://github.com/ambionics/phpggc.git"; fi

    if p=$(find_repo jexboss); then pass "jexboss" "$p"
    else warn "jexboss" "git clone https://github.com/joaomatosf/jexboss.git"; fi

    if p=$(find_pipx badsecrets); then pass "badsecrets" "$p"
    else warn "badsecrets" "pipx install badsecrets"; fi
}

check_active_directory() {
    section "Active Directory"

    local p
    if p=$(find_pipx bloodhound bloodhound-python || find_cmd bloodhound-python); then
        pass "BloodHound CE (collector)" "$p"
    else fail "BloodHound CE" "pipx install bloodhound"; fi

    if p=$(find_cmd rusthound || find_repo RustHound-CE); then pass "rusthound-ce" "$p"
    else warn "rusthound-ce" "download from GitHub releases"; fi

    if p=$(find_pipx certipy-ad certipy); then pass "certipy" "$p"
    elif p=$(find_cmd certipy); then pass "certipy" "$p"
    else fail "certipy" "pipx install certipy-ad"; fi

    if p=$(find_pipx bloodyad bloodyAD || find_cmd bloodyAD); then pass "bloodyAD" "$p"
    else fail "bloodyAD" "pipx install bloodyad"; fi

    if p=$(find_cmd kerbrute || find_go kerbrute); then pass "kerbrute" "$p"
    else fail "kerbrute" "download from https://github.com/ropnop/kerbrute/releases"; fi

    if p=$(find_pipx pywhisker); then pass "pywhisker" "$p"
    else warn "pywhisker" "pipx install pywhisker"; fi

    if p=$(find_repo targetedKerberoast); then pass "targetedKerberoast" "$p"
    else warn "targetedKerberoast" "git clone https://github.com/ShutdownRepo/targetedKerberoast"; fi

    if p=$(find_repo krbrelayx); then pass "krbrelayx" "$p"
    else fail "krbrelayx" "git clone https://github.com/dirkjanm/krbrelayx"; fi

    if p=$(find_repo PetitPotam); then pass "PetitPotam" "$p"
    else warn "PetitPotam" "git clone https://github.com/topotam/PetitPotam"; fi

    if p=$(find_repo DFSCoerce); then pass "DFSCoerce" "$p"
    else warn "DFSCoerce" "git clone https://github.com/Wh04m1001/DFSCoerce"; fi

    if p=$(find_repo ShadowCoerce); then pass "ShadowCoerce" "$p"
    else warn "ShadowCoerce" "git clone https://github.com/ShutdownRepo/ShadowCoerce"; fi

    if p=$(find_repo PKINITtools); then pass "PKINITtools" "$p"
    else fail "PKINITtools" "git clone https://github.com/dirkjanm/PKINITtools"; fi

    if p=$(find_repo modifyCertTemplate); then pass "modifyCertTemplate" "$p"
    else warn "modifyCertTemplate" "git clone https://github.com/fortalice/modifyCertTemplate"; fi

    if p=$(find_repo gMSADumper); then pass "gMSADumper" "$p"
    else warn "gMSADumper" "git clone https://github.com/micahvandeusen/gMSADumper"; fi

    if p=$(find_pipx impacket); then pass "impacket (local)" "$p"
    elif p=$(find_cmd secretsdump.py); then pass "impacket (local)" "$p"
    else fail "impacket (local)" "pipx install impacket"; fi
}

check_sccm_gpo() {
    section "SCCM and GPO"

    local p
    if p=$(find_pipx sccmhunter); then pass "sccmhunter" "$p"
    else warn "sccmhunter" "pipx install sccmhunter"; fi

    if p=$(find_repo PXEThief || find_repo pxethiefy); then pass "pxethiefy" "$p"
    else warn "pxethiefy" "git clone https://github.com/MWR-CyberSec/PXEThief"; fi

    if p=$(find_repo pyGPOAbuse); then pass "pyGPOAbuse" "$p"
    else warn "pyGPOAbuse" "git clone https://github.com/Hackndo/pyGPOAbuse"; fi

    if p=$(find_pipx gpohound || find_cmd gpohound); then pass "GPOHound" "$p"
    else warn "GPOHound" "pipx install gpohound"; fi
}

check_pivoting() {
    section "Pivoting and tunneling"

    local p
    if p=$(find_cmd sshuttle); then pass "sshuttle" "$p"
    else fail "sshuttle" "sudo apt install sshuttle"; fi

    if p=$(find_cmd proxychains4 || find_cmd proxychains); then pass "proxychains" "$p"
    else fail "proxychains" "sudo apt install proxychains4"; fi

    if p=$(find_cmd autossh); then pass "autossh" "$p"
    else warn "autossh" "sudo apt install autossh"; fi

    if p=$(find_cmd msfconsole); then pass "metasploit" "$p"
    else warn "metasploit" "sudo apt install metasploit-framework"; fi
}

check_cracking() {
    section "Credential cracking"

    local p
    if p=$(find_cmd hashcat); then pass "hashcat" "$p"
    else fail "hashcat" "sudo apt install hashcat"; fi

    if p=$(find_cmd john); then pass "john" "$p"
    else fail "john" "sudo apt install john"; fi

    if p=$(find_cmd hydra); then pass "hydra" "$p"
    else fail "hydra" "sudo apt install hydra"; fi
}

check_evasion() {
    section "Evasion and payload building"

    local p
    if p=$(find_cmd x86_64-w64-mingw32-gcc); then pass "mingw-w64" "$p"
    elif p=$(find_cmd i686-w64-mingw32-gcc); then pass "mingw-w64" "$p"
    else warn "mingw-w64" "sudo apt install mingw-w64"; fi

    if p=$(find_cmd msfvenom); then pass "msfvenom" "$p"
    else warn "msfvenom" "sudo apt install metasploit-framework"; fi

    if p=$(find_cmd gcc); then pass "gcc" "$p"
    else warn "gcc" "sudo apt install build-essential"; fi

    if p=$(find_cmd searchsploit); then pass "searchsploit" "$p"
    else warn "searchsploit" "sudo apt install exploitdb"; fi
}

check_general() {
    section "General utilities"

    local p
    if p=$(find_cmd curl); then pass "curl" "$p"
    else fail "curl" "sudo apt install curl"; fi

    if p=$(find_cmd openssl); then pass "openssl" "$p"
    else fail "openssl" "sudo apt install openssl"; fi

    if p=$(find_cmd ldapsearch); then pass "ldapsearch" "$p"
    else fail "ldapsearch" "sudo apt install ldap-utils"; fi

    if p=$(find_cmd rpcclient); then pass "rpcclient" "$p"
    else warn "rpcclient" "sudo apt install smbclient"; fi

    if p=$(find_cmd jq); then pass "jq" "$p"
    else fail "jq" "sudo apt install jq"; fi

    if p=$(find_cmd exiftool); then pass "exiftool" "$p"
    else warn "exiftool" "sudo apt install libimage-exiftool-perl"; fi

    if p=$(find_cmd ruby); then pass "ruby" "$p"
    else warn "ruby" "sudo apt install ruby"; fi

    if p=$(find_cmd java); then pass "java" "$p"
    else warn "java" "sudo apt install default-jdk"; fi

    if p=$(find_cmd tmux); then pass "tmux" "$p"
    else warn "tmux" "sudo apt install tmux"; fi
}

check_wordlists() {
    section "Wordlists"

    if [[ -d /usr/share/seclists ]]; then
        pass "SecLists" "/usr/share/seclists"
    elif [[ -d /usr/share/SecLists ]]; then
        pass "SecLists" "/usr/share/SecLists"
    elif [[ -d "$HOME/SecLists" || -d "$HOME/tools/SecLists" || -d "$HOME/wordlists/SecLists" ]]; then
        local d
        for d in "$HOME/SecLists" "$HOME/tools/SecLists" "$HOME/wordlists/SecLists"; do
            [[ -d "$d" ]] && pass "SecLists" "$d" && break
        done
    else
        fail "SecLists" "sudo apt install seclists  OR  git clone to /usr/share/seclists/"
    fi

    if [[ -f /usr/share/wordlists/rockyou.txt ]]; then
        pass "rockyou.txt" "/usr/share/wordlists/rockyou.txt"
    elif [[ -f /usr/share/wordlists/rockyou.txt.gz ]]; then
        warn "rockyou.txt (compressed)" "gunzip /usr/share/wordlists/rockyou.txt.gz"
    else
        fail "rockyou.txt" "expected at /usr/share/wordlists/rockyou.txt"
    fi

    if p=$(find_repo jwt-secrets); then pass "jwt-secrets" "$p"
    else warn "jwt-secrets" "git clone https://github.com/wallarm/jwt-secrets"; fi
}

check_target_tools() {
    section "Target-side tools (pre-staged on attackbox)"

    local found=false p

    # Linux
    for name in linpeas.sh lse.sh pspy64 pspy32 linux-exploit-suggester.sh deepce.sh; do
        short="${name%%.*}"
        if compgen -G "$HOME/tools/**/$name" >/dev/null 2>&1 ||
           compgen -G "/opt/**/$name" >/dev/null 2>&1 ||
           compgen -G "$HOME/tools/bin/$name" >/dev/null 2>&1; then
            pass "$short" "found"
        else
            warn "$short" "download and stage in ~/tools/"
        fi
    done

    # Windows
    for name in winpeas.exe mimikatz.exe Rubeus.exe; do
        short="${name%%.*}"
        if compgen -G "$HOME/tools/**/$name" >/dev/null 2>&1 ||
           compgen -G "/opt/**/$name" >/dev/null 2>&1 ||
           compgen -G "$HOME/tools/bin/$name" >/dev/null 2>&1; then
            pass "$short" "found"
        else
            warn "$short" "download and stage in ~/tools/"
        fi
    done

    # Tunnel agents (Linux + Windows builds)
    for name in chisel ligolo-agent; do
        if compgen -G "$HOME/tools/**/$name*" >/dev/null 2>&1 ||
           compgen -G "/opt/**/$name*" >/dev/null 2>&1; then
            pass "$name (agent builds)" "found"
        else
            warn "$name (agent builds)" "download from GitHub releases"
        fi
    done

    if p=$(find_pipx wesng wes || find_cmd wes); then pass "WES-NG" "$p"
    else warn "WES-NG" "pipx install wesng"; fi
}

# ── Category map ────────────────────────────────────────────────────────────

declare -A CATEGORIES=(
    [prereqs]=check_redrun_prereqs
    [network]=check_network_scanning
    [web]=check_web_testing
    [deser]=check_deserialization
    [ad]=check_active_directory
    [sccm-gpo]=check_sccm_gpo
    [pivoting]=check_pivoting
    [cracking]=check_cracking
    [evasion]=check_evasion
    [general]=check_general
    [wordlists]=check_wordlists
    [target-tools]=check_target_tools
)

CATEGORY_ORDER=(prereqs network web deser ad sccm-gpo pivoting cracking evasion general wordlists target-tools)

# ── Main ────────────────────────────────────────────────────────────────────

print_usage() {
    echo "Usage: bash preflight.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --list          List available categories"
    echo "  --json          Machine-readable JSON output"
    echo "  --<category>    Check a single category (e.g., --ad, --web)"
    echo ""
    echo "Categories: ${CATEGORY_ORDER[*]}"
}

run_category=""
for arg in "$@"; do
    case "$arg" in
        --help|-h)   print_usage; exit 0 ;;
        --list)      echo "Categories: ${CATEGORY_ORDER[*]}"; exit 0 ;;
        --json)      JSON_MODE=true ;;
        --*)
            cat="${arg#--}"
            if [[ -n "${CATEGORIES[$cat]:-}" ]]; then
                run_category="$cat"
            else
                echo "Unknown category: $cat" >&2
                echo "Available: ${CATEGORY_ORDER[*]}" >&2
                exit 1
            fi
            ;;
    esac
done

# Platform gate
if [[ "$(uname -s)" != "Linux" ]]; then
    echo "red-run preflight is designed for Linux attackboxes." >&2
    echo "Detected: $(uname -s)" >&2
    exit 1
fi

if ! $JSON_MODE; then
    echo "${BOLD}red-run preflight check${RESET}"
    echo "${DIM}$(uname -srm) — $(cat /etc/os-release 2>/dev/null | grep '^PRETTY_NAME=' | cut -d= -f2 | tr -d '"' || echo 'unknown distro')${RESET}"
fi

if [[ -n "$run_category" ]]; then
    ${CATEGORIES[$run_category]}
else
    for cat in "${CATEGORY_ORDER[@]}"; do
        ${CATEGORIES[$cat]}
    done
fi

# ── Summary ─────────────────────────────────────────────────────────────────

if $JSON_MODE; then
    echo "{"
    echo "  \"pass\": $PASS,"
    echo "  \"fail\": $FAIL,"
    echo "  \"warn\": $WARN,"
    echo "  \"results\": ["
    for i in "${!JSON_RESULTS[@]}"; do
        if [[ $i -lt $((${#JSON_RESULTS[@]} - 1)) ]]; then
            echo "    ${JSON_RESULTS[$i]},"
        else
            echo "    ${JSON_RESULTS[$i]}"
        fi
    done
    echo "  ]"
    echo "}"
else
    echo ""
    echo "${BOLD}Summary${RESET}"
    echo "  ${GREEN}✓ $PASS passed${RESET}    ${RED}✗ $FAIL missing${RESET}    ${YELLOW}○ $WARN optional${RESET}"
    if [[ $FAIL -gt 0 ]]; then
        echo ""
        echo "${DIM}Re-run with --<category> to check a specific area.${RESET}"
        echo "${DIM}See docs/dependencies.md for full install commands.${RESET}"
    fi
fi

exit $(( FAIL > 0 ? 1 : 0 ))
