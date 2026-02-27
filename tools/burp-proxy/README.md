# Burp MCP Proxy

Connects Claude Code to a running Burp Suite Pro instance via PortSwigger's
[MCP server](https://github.com/PortSwigger/mcp-server). This enables the
`web-discovery-burp` co-pilot skill to read proxy history, triage scanner
findings, manage Collaborator payloads, and push requests to Repeater.

## Prerequisites

- **Burp Suite Professional** (Community Edition does not support extensions)
- **Java 21+** (`java -version` to check)
- **Burp MCP extension** installed in Burp Suite

## Setup

### 1. Install the Burp MCP extension

In Burp Suite:
1. Go to **Extensions** > **BApp Store**
2. Search for **MCP Server** (by PortSwigger)
3. Click **Install**
4. Verify the extension is loaded and shows "MCP SSE server started on port 9876"

### 2. Export the MCP proxy jar

The proxy jar bridges Claude Code (stdio MCP) to Burp's SSE endpoint.

**Option A** — Download from the extension:
1. In Burp, go to **Extensions** > **MCP Server** > **Export proxy jar**
2. Save as `mcp-proxy-all.jar` in this directory (`tools/burp-proxy/`)

**Option B** — Build from source:
```bash
git clone https://github.com/PortSwigger/mcp-proxy
cd mcp-proxy
./gradlew shadowJar
cp build/libs/mcp-proxy-all.jar /path/to/red-run/tools/burp-proxy/
```

### 3. Verify

```bash
# From the red-run repo root
./install.sh
# Should print: [burp-proxy] Proxy jar found, Java available: OK
```

## How it works

```
Claude Code  <--stdio-->  mcp-proxy-all.jar  <--SSE-->  Burp MCP Extension
                          (this directory)               (localhost:9876)
```

The proxy jar translates between Claude Code's stdio-based MCP protocol and
Burp's SSE-based MCP endpoint. Burp must be running with the MCP extension
loaded before Claude Code starts.

## Configuration

The default SSE URL is `http://127.0.0.1:9876`. If you changed the port in
Burp's MCP extension settings, update the `--sse-url` argument in `.mcp.json`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `burp` MCP server fails to start | Is `mcp-proxy-all.jar` in this directory? |
| "Connection refused" in proxy jar output | Is Burp running with the MCP extension loaded? |
| Java version error | Burp MCP proxy requires Java 21+. Check `java -version`. |
| SSE connection timeout | Check that the port in `.mcp.json` matches Burp's MCP extension port |
| Other MCP servers still work, only Burp fails | Expected when Burp isn't running. Other servers are unaffected. |

## Files

- `mcp-proxy-all.jar` — the MCP proxy (gitignored, user-provided)
- `.gitkeep` — keeps this directory in git
- `README.md` — this file
