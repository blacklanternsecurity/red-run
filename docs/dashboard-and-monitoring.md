# Dashboard & Monitoring

red-run provides real-time visibility into teammate execution through Claude Code agent teams and the state dashboard.

## Agent Teams (Primary)

red-run uses [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams) for teammate coordination and visibility. Each teammate runs in its own tmux pane, giving the operator a live view of all parallel work.

**Operator controls:**

- **Watch** — see each teammate's output in its own tmux pane (reasoning, commands, results)
- **Interrupt** — press Escape in a teammate's pane to stop its current turn
- **Redirect** — type directly to any teammate to give new instructions or ask questions
- **Monitor task list** — press Ctrl+T to toggle the shared task list showing all assigned work

For split-pane mode, start Claude Code inside a tmux session. Without tmux, teammates run in-process mode — cycle through them with Shift+Down.

### Setup

Add to `.claude/settings.json` (project-level):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Built-in Terminal Dashboard

The built-in dashboard (`operator/agent-dashboard/tail-agent.py`) is a lightweight, read-only terminal viewer that parses Claude Code's raw JSONL transcripts. No server, no npm, no dependencies beyond Python 3. It's useful for observation of legacy subagent runs or as a supplementary view.

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
