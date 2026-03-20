# Dashboard & Monitoring

red-run provides real-time visibility into agent execution through dashboards and background event polling. Two options are available for watching agents: **agentsee** (recommended) for full operator control, or the **built-in terminal dashboard** for lightweight observation.

## agentsee (Recommended)

[agentsee](https://github.com/blacklanternsecurity/agentsee) is an operator control plane for Claude Code agents. It gives you a browser-based dashboard where you can watch agents work in real time, pause them mid-run, chat with them to redirect or ask questions, and switch between autonomous and supervised execution modes.

### Why use agentsee with red-run

red-run's orchestrator provides human-in-the-loop control at the **routing level** — you approve which agent to spawn and what skill to run. But once an agent is running, it's autonomous until it finishes. agentsee fills that gap with **runtime control**:

- **Hold/Release** — pause any agent at its next tool call, inspect what it's doing, then resume. Useful when you see an agent heading down the wrong path or want to wait for another agent's results before continuing.
- **Leash mode** — require an agent to check in every N tool calls. Set `leash=1` for step-by-step approval, `leash=10` for periodic check-ins, or remove the leash for full autonomy. Adjustable per-agent at any time.
- **Bidirectional chat** — when an agent is held or hits a leash checkpoint, a chat panel opens. Send instructions ("try port 8443 instead", "skip the brute force, we have creds"), ask questions ("what did you find in that config file?"), or redirect the agent entirely. Two reply modes: "Send + Release" to let it run, or "Send + Keep held" to continue the conversation.
- **Multi-agent tiling** — auto-tiles agent panes in a grid layout. Real-time streaming of agent reasoning, tool calls, and results with the same color coding as the built-in dashboard.
- **Tab workspaces** — group agents by engagement, target, or task phase across tabs.

### Setup

agentsee is a separate project. Install it alongside red-run:

```bash
git clone https://github.com/blacklanternsecurity/agentsee.git
cd agentsee
npm install && cd dashboard && npm install && cd ..
npm run build
bash install.sh   # configures Claude Code hooks and MCP server
```

The installer adds PreToolUse/PostToolUse hooks to Claude Code's settings and registers the agentsee MCP server. It can optionally patch red-run's agent files in `~/.claude/agents/` to give subagents access to `operator_checkpoint` and `operator_notify` tools.

Start the server before launching Claude Code (MCP connections are established at startup):

```bash
node build/server.js
```

Then open `http://localhost:4900` in a browser. Agents appear automatically as they spawn.

See the [agentsee README](https://github.com/blacklanternsecurity/agentsee) for full documentation, keyboard shortcuts, REST API, and configuration options.

### Design notes

agentsee is **fail-open** — if the server isn't running, hooks exit 0 and agents run normally. It adds no hard dependency to red-run. The PreToolUse hook makes an HTTP call before each tool invocation; if the server is unreachable, the tool call proceeds without delay.

## Built-in Terminal Dashboard

The built-in dashboard (`operator/agent-dashboard/tail-agent.py`) is a lightweight, read-only terminal viewer that parses Claude Code's raw JSONL transcripts. No server, no npm, no dependencies beyond Python 3. It's useful for quick observation when you don't need runtime control, or as a fallback when agentsee isn't installed.

### Single-Agent Modes

```bash
# One-shot — print formatted output and exit
python3 operator/agent-dashboard/tail-agent.py <output_file>

# Follow — live-tail like tail -f (Ctrl-C to stop)
python3 operator/agent-dashboard/tail-agent.py -f <output_file>

# Pipe — read from stdin
tail -f <output_file> | python3 operator/agent-dashboard/tail-agent.py
```

### Multi-Agent Dashboard

The curses-based dashboard shows multiple agents side by side in a split-pane terminal view. It auto-discovers new agents from Claude Code's tasks directory and subagent JSONL directories:

```bash
# Auto-discover agents (recommended)
bash operator/agent-dashboard/dashboard.sh

# Explicit label:path pairs
python3 operator/agent-dashboard/tail-agent.py --dashboard web:path1 ad:path2
```

The dashboard starts with "Waiting for agents..." and picks up new agents automatically as they spawn.

### Keybindings

| Key | Action |
|-----|--------|
| `Tab` | Switch to next pane |
| `Shift-Tab` | Switch to previous pane |
| `j` / `Down` | Scroll down |
| `k` / `Up` | Scroll up |
| `PgDn` | Page down |
| `PgUp` | Page up |
| `G` / `End` | Jump to bottom (resume live follow) |
| `g` / `Home` | Jump to top |
| `q` / `Ctrl-C` | Quit |

The status bar shows `LIVE` when auto-following new output or `scrolled +N` when scrolled up. Scrolling to the bottom re-enables live follow.

### Color Coding

| Color | Category | Content |
|-------|----------|---------|
| Cyan | Agent reasoning | Text output from the agent's thinking and analysis |
| Yellow (bold, `▶` prefix) | Shell/Bash commands | `send_command`, `start_process`, `start_listener`, Bash tool calls |
| Dim | Tool calls | Skill loads, state queries, file reads/writes, browser actions |

In dashboard mode, each pane header uses a rotating color palette (cyan, green, magenta, yellow) with the focused pane highlighted in reverse video.

### Output Format

The dashboard parses JSONL lines with `"type":"assistant"` and formats tool calls as compact one-liners:

| Format | Source |
|--------|--------|
| `SHELL[sid] command` | `send_command` |
| `LISTEN port=N label=X` | `start_listener` |
| `PROC command` | `start_process` |
| `BASH (description) command` | Bash tool |
| `SKILL get_skill(name)` | skill-router calls |
| `STATE get_summary` | state-server calls |
| `BROWSER navigate(url=...)` | browser-server calls |
| `READ/WRITE/EDIT path` | Built-in file tools |

## Transcript Capture

Every agent's full JSONL transcript is automatically saved to `engagement/evidence/logs/` when the agent finishes. This is the accountability layer — the dashboard shows you what agents are doing in real time, and transcripts give you a permanent record of every tool call, command, and decision each agent made.

A `SubagentStop` hook (`tools/hooks/save-agent-log.sh`) handles this automatically:

1. Claude Code fires the `SubagentStop` event when any agent finishes
2. The hook reads `agent_transcript_path` and `agent_type` from the event JSON
3. Copies the transcript to `engagement/evidence/logs/{timestamp}-{agent-type}.jsonl`

Only red-run agents are captured (network-recon, web-discovery, web-exploit, ad-discovery, ad-exploit, password-spray, linux-privesc, windows-privesc, evasion, credential-cracking). Built-in subagents (Explore, Plan, general-purpose) are ignored.

No engagement directory = hook exits silently. The retrospective skill parses these logs for post-engagement analysis.

## Event Watcher

The event watcher (`tools/hooks/event-watcher.sh`) acts as a push notification from discovery agents to the orchestrator. The orchestrator spawns one alongside every discovery agent as a background process.

**How it works:**

1. The orchestrator spawns `event-watcher.sh` with `run_in_background: true` alongside a discovery agent
2. The script polls `state_events` every 5 seconds for new rows
3. When a discovery agent writes an interim finding (credential, vuln, pivot, blocked), a new row appears
4. The watcher detects the change, waits 5 seconds (debounce to let the agent finish its batch), outputs the events as JSON, and **exits**
5. The process termination notifies the orchestrator, which checks the database for the new findings and can route accordingly — e.g., spraying newly discovered credentials against other targets

Without this, the orchestrator would have to continuously poll the database itself between agent turns, wasting tokens on repeated `poll_events()` calls that usually return nothing.

**Usage:**

```bash
# Spawned by orchestrator with run_in_background: true
bash tools/hooks/event-watcher.sh <cursor> <db_path>
```

**Parameters:**

- `cursor` — last `state_events` ID seen (events with `id > cursor` are new)
- `db_path` — path to `engagement/state.db`
- 10-minute timeout prevents zombie watchers if no events arrive

> **Note:** The event watcher uses Python 3's built-in `sqlite3` module. No sqlite3 CLI binary is required.

## Configuration

### Hook Setup

The `SubagentStop` hook is configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash tools/hooks/save-agent-log.sh"
          }
        ]
      }
    ]
  }
}
```

The hook always exits 0 to never block Claude Code, regardless of whether logging succeeds.
