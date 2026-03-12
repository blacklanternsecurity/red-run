# RDP Server

MCP server providing headless RDP automation for red-run subagents.

## Architecture

Pure Python RDP client using the `aardwolf` library. No X11, Xvfb, xfreerdp,
xdotool, or scrot needed. aardwolf decodes the RDP stream directly into a PIL
image buffer and accepts mouse/keyboard input natively via the RDP protocol.

```
aardwolf (Python RDP client)
  ├── RDP bitmap decoding → PIL Image (screenshot)
  ├── RDP mouse input → click, double-click, scroll
  └── RDP keyboard input → scancodes, characters
```

## Tools

| Tool | Purpose |
|------|---------|
| `rdp_connect(host, user, password, domain, port, resolution)` | Connect via RDP, return session_id + initial screenshot |
| `rdp_screenshot(session_id, save_to)` | Capture desktop as PNG |
| `rdp_click(session_id, x, y, button)` | Click at coordinates |
| `rdp_double_click(session_id, x, y)` | Double-click at coordinates |
| `rdp_type(session_id, text, delay_ms)` | Type text (configurable inter-key delay) |
| `rdp_key(session_id, keys)` | Send special keys (e.g., `super+r`, `Return`, `ctrl+c`) |
| `rdp_execute(session_id, command, wait_seconds)` | Win+R → type command → Enter → wait → screenshot |
| `rdp_scroll(session_id, direction, clicks)` | Scroll up/down |
| `rdp_close(session_id)` | Disconnect RDP session |
| `list_rdp_sessions()` | Show active sessions |

## Prerequisites

Python only — no system packages required. Dependencies installed via `uv sync`:

- `mcp[cli]` — MCP server framework
- `aardwolf` — Python RDP client (handles NLA/NTLM authentication)

## Running

```bash
# Via MCP (configured in .mcp.json)
uv run --directory tools/rdp-server python server.py

# Or directly
cd tools/rdp-server && uv run python server.py
```

## Usage Pattern

The most common pentesting workflow:

1. `rdp_connect(host, user, password)` — establish RDP session
2. `rdp_execute(session_id, "cmd /k whoami")` — run command via Win+R
3. Read the screenshot to see output
4. `rdp_execute(session_id, "powershell -e <base64>")` — establish reverse shell
5. `rdp_close(session_id)` — cleanup

For GUI interaction (MMC, regedit, browser navigation):

1. `rdp_screenshot` — see current state
2. `rdp_click` / `rdp_double_click` — interact with UI elements
3. `rdp_type` — fill text fields
4. `rdp_key` — keyboard shortcuts
5. `rdp_screenshot` — verify result
