#!/usr/bin/env bash
# Pre-engagement configuration wizard.
# Writes engagement/config.yaml so the orchestrator skips its built-in wizard.
# Run before ./run.sh to pre-configure scan type, proxy, spray, cracking, and C2.
set -euo pipefail
cd "$(dirname "$0")"

CONFIG="engagement/config.yaml"
TEMPLATE="operator/templates/config.yaml"

if [[ -f "$CONFIG" ]]; then
    echo "Config already exists: $CONFIG"
    read -rp "Overwrite? [y/N] " ow
    [[ "${ow,,}" == "y" ]] || { echo "Keeping existing config."; exit 0; }
fi

mkdir -p engagement

echo ""
echo "=== red-run engagement setup ==="
echo ""

# --- Q1: Scan type ---
echo "Q1 — Default network scan type"
echo "  1) quick  (top 1000 ports)"
echo "  2) full   (all 65535 ports)"
read -rp "  Choice [1]: " q1
case "${q1:-1}" in
    2) scan_type="full" ;;
    *) scan_type="quick" ;;
esac

# --- Q2: Web proxy ---
echo ""
echo "Q2 — Web proxy for HTTP traffic"
echo "  1) Burp 127.0.0.1:8080 (recommended)"
echo "  2) Custom URL"
echo "  3) No proxy"
read -rp "  Choice [1]: " q2
case "${q2:-1}" in
    2) read -rp "  Proxy URL (e.g., http://10.0.0.1:8080): " proxy_url
       proxy_enabled="true" ;;
    3) proxy_enabled="false"; proxy_url="" ;;
    *) proxy_enabled="true"; proxy_url="http://127.0.0.1:8080" ;;
esac

# --- Q3: Spray tier ---
echo ""
echo "Q3 — Password spray default tier"
echo "  1) light   (~30 passwords)"
echo "  2) medium  (~10k passwords)"
echo "  3) heavy   (~100k passwords)"
echo "  4) skip    (no spraying)"
read -rp "  Choice [1]: " q3
case "${q3:-1}" in
    2) spray_tier="medium" ;;
    3) spray_tier="heavy" ;;
    4) spray_tier="skip" ;;
    *) spray_tier="light" ;;
esac

# --- Q4: Hash recovery ---
echo ""
echo "Q4 — Hash recovery method"
echo "  1) local    (hashcat/john on this machine)"
echo "  2) export   (save hashes for external rig)"
echo "  3) skip     (no recovery)"
read -rp "  Choice [1]: " q4
case "${q4:-1}" in
    2) cracking_method="export" ;;
    3) cracking_method="skip" ;;
    *) cracking_method="local" ;;
esac

# --- Q5: Shell backend ---
echo ""
echo "Q5 — Shell backend"
echo "  1) shell-server  (raw TCP/PTY, always available)"
if pgrep -f "sliver-server daemon" &>/dev/null; then
    echo "  2) sliver        (Sliver C2 — daemon running)"
    has_sliver=1
elif [[ -f "engagement/sliver.cfg" ]]; then
    echo "  2) sliver        (Sliver C2 — config found, daemon not running)"
    has_sliver=1
else
    echo "  2) sliver        (not configured)"
    has_sliver=0
fi
echo "  3) custom        (your own C2 + MCP server)"
read -rp "  Choice [1]: " q5

shell_backend="shell-server"
sliver_config=""
custom_mcp=""
custom_ref=""

case "${q5:-1}" in
    2)
        default_cfg="engagement/sliver.cfg"
        if [[ -f "$default_cfg" ]]; then
            echo "  Found operator config: $default_cfg"
            shell_backend="sliver"
            sliver_config="$default_cfg"
        else
            echo ""
            echo "  No operator config found at $default_cfg."
            echo ""
            echo "  1) Generate now (local daemon — sliver-server must be running)"
            echo "  2) Provide path to existing config (local or from remote C2)"
            echo "  3) Cancel — fall back to shell-server"
            read -rp "  Choice [3]: " sliver_setup
            case "${sliver_setup:-3}" in
                1)
                    if ! pgrep -f "sliver-server daemon" &>/dev/null; then
                        echo "  Sliver daemon not running."
                        echo "  Start it first:  sliver-server daemon &"
                        echo "  Then re-run ./config.sh."
                        echo "  Falling back to shell-server."
                    elif ! command -v sliver-server &>/dev/null; then
                        echo "  sliver-server not found on PATH."
                        echo "  See docs/installation.md for install steps."
                        echo "  Falling back to shell-server."
                    else
                        echo "  Generating operator config..."
                        if sliver-server operator --name red-run --lhost 127.0.0.1 \
                            --permissions all --save "$default_cfg" 2>&1; then
                            echo "  Config saved to $default_cfg"
                            shell_backend="sliver"
                            sliver_config="$default_cfg"
                        else
                            echo "  Failed to generate config."
                            echo "  Falling back to shell-server."
                        fi
                    fi
                    ;;
                2)
                    read -rp "  Path to operator config: " cfg_path
                    if [[ -f "$cfg_path" ]]; then
                        cp "$cfg_path" "$default_cfg"
                        echo "  Copied to $default_cfg"
                        shell_backend="sliver"
                        sliver_config="$default_cfg"
                    else
                        echo "  File not found: $cfg_path"
                        echo "  Falling back to shell-server."
                    fi
                    ;;
                *)
                    echo "  Falling back to shell-server."
                    ;;
            esac
        fi
        ;;
    3)
        shell_backend="custom"
        read -rp "  MCP server name (as registered in .mcp.json): " custom_mcp
        read -rp "  Reference doc path (markdown): " custom_ref
        if [[ -n "$custom_ref" && ! -f "$custom_ref" ]]; then
            echo "  Warning: $custom_ref not found. shell-mgr will need it at runtime."
        fi
        ;;
esac

# --- Write config ---
cat > "$CONFIG" << YAML
# red-run engagement configuration
# Generated by config.sh. Edit at any time.

scan_type: ${scan_type}
YAML

if [[ "$proxy_enabled" == "true" ]]; then
    cat >> "$CONFIG" << YAML

web_proxy:
  enabled: true
  url: "${proxy_url}"
YAML
else
    cat >> "$CONFIG" << YAML

web_proxy:
  enabled: false
YAML
fi

cat >> "$CONFIG" << YAML

spray:
  default_tier: ${spray_tier}

cracking:
  default_method: ${cracking_method}

shell:
  backend: ${shell_backend}
YAML

if [[ "$shell_backend" == "sliver" && -n "$sliver_config" ]]; then
    echo "  sliver_config: \"${sliver_config}\"" >> "$CONFIG"
fi

if [[ "$shell_backend" == "custom" ]]; then
    [[ -n "$custom_mcp" ]] && echo "  custom_mcp: \"${custom_mcp}\"" >> "$CONFIG"
    [[ -n "$custom_ref" ]] && echo "  custom_ref: \"${custom_ref}\"" >> "$CONFIG"
fi

# --- Patch .mcp.json for C2 backends ---
MCP_JSON=".mcp.json"
if [[ "$shell_backend" == "sliver" && -f "$MCP_JSON" ]]; then
    if ! grep -q '"sliver-server"' "$MCP_JSON"; then
        echo ""
        echo "Adding sliver-server to .mcp.json..."
        # Insert sliver-server SSE entry after shell-server
        python3 -c "
import json, sys
with open('$MCP_JSON') as f:
    cfg = json.load(f)
cfg['mcpServers']['sliver-server'] = {'type': 'sse', 'url': 'http://127.0.0.1:8023/sse'}
with open('$MCP_JSON', 'w') as f:
    json.dump(cfg, f, indent=2)
    f.write('\n')
print('  sliver-server added to .mcp.json')
" 2>&1
        echo "  Note: restart Claude Code session for MCP changes to take effect."
    else
        echo "  sliver-server already in .mcp.json"
    fi

    # Ensure sliver-server tools are auto-allowed in settings.json
    SETTINGS_JSON=".claude/settings.json"
    if [[ -f "$SETTINGS_JSON" ]]; then
        if ! grep -q '"mcp__sliver-server__\*"' "$SETTINGS_JSON"; then
            echo "Adding sliver-server to allowedTools in settings.json..."
            python3 -c "
import json
with open('$SETTINGS_JSON') as f:
    cfg = json.load(f)
allow = cfg.get('permissions', {}).get('allow', [])
entry = 'mcp__sliver-server__*'
if entry not in allow:
    # Insert after shell-server entry if present, else append
    try:
        idx = next(i for i, v in enumerate(allow) if 'shell-server' in v) + 1
    except StopIteration:
        idx = len(allow)
    allow.insert(idx, entry)
    cfg.setdefault('permissions', {})['allow'] = allow
    with open('$SETTINGS_JSON', 'w') as f:
        json.dump(cfg, f, indent=2)
        f.write('\n')
    print('  sliver-server added to allowedTools')
" 2>&1
        else
            echo "  sliver-server already in allowedTools"
        fi
    fi
fi

echo ""
echo "Config written to $CONFIG"
echo "Run ./run.sh to start the engagement."
