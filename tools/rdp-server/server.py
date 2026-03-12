"""MCP server providing headless RDP automation for pentesting subagents.

Provides ten tools:
- rdp_connect: Connect to RDP target, return session_id + initial screenshot
- rdp_screenshot: Capture desktop as PNG image
- rdp_click: Click at x,y coordinates
- rdp_double_click: Double-click at x,y coordinates
- rdp_type: Type text characters
- rdp_key: Send special key combinations (Return, Tab, super+r, ctrl+c)
- rdp_execute: Convenience — Win+R, type command, Enter, wait, screenshot
- rdp_scroll: Scroll up/down
- rdp_close: Disconnect RDP session
- list_rdp_sessions: Show active sessions

Architecture: pure Python RDP client via aardwolf library. No X11, Xvfb,
xdotool, or scrot needed. aardwolf decodes the RDP stream directly into
a PIL image buffer and accepts mouse/keyboard input natively.

Usage:
    uv run python server.py
"""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from mcp.server.fastmcp import FastMCP

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_LOGIN_WAIT = 8  # seconds to wait after connect for desktop to render


def create_server() -> FastMCP:
    """Create and configure the RDP MCP server."""
    mcp = FastMCP(
        "red-run-rdp-server",
        instructions=(
            "Provides headless RDP automation for red-run subagents. "
            "Use rdp_connect to start an RDP session, rdp_screenshot to "
            "capture the display, rdp_click/rdp_type/rdp_key for input, "
            "and rdp_execute for the common Win+R → command → Enter shortcut. "
            "Screenshots are the primary output — read them with the Read tool "
            "(multimodal). WARNING: Screenshots are token-expensive. Treat RDP "
            "as a bootstrap method — establish a reverse shell or enable WinRM "
            "ASAP, then switch to shell-server. Tips: 'cmd /k <command>' with "
            "rdp_execute keeps output visible; rdp_key('ctrl+l') focuses "
            "address bars; for interactive work, rdp_execute('cmd') then "
            "rdp_type + rdp_key('Return')."
        ),
    )

    sessions: dict[str, dict] = {}

    def _evidence_path(prefix: str, session_id: str) -> Path:
        """Build a screenshot save path."""
        evidence_dir = _PROJECT_ROOT / "engagement" / "evidence"
        if evidence_dir.exists():
            ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            return evidence_dir / f"{prefix}-{ts}.png"
        return _PROJECT_ROOT / f"{prefix}-{session_id}.png"

    async def _take_screenshot(session: dict) -> str:
        """Capture the desktop buffer and save as PNG. Returns file path."""
        from aardwolf.commons.queuedata.constants import VIDEO_FORMAT

        conn = session["conn"]
        buf = conn.get_desktop_buffer(VIDEO_FORMAT.PIL)
        if buf is None:
            raise RuntimeError("No desktop buffer available")

        path = _evidence_path("rdp", session["session_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        buf.save(str(path))
        return str(path)

    async def _send_click(conn, x: int, y: int, button, double: bool = False):
        """Send a mouse click (or double-click) at coordinates."""
        from aardwolf.commons.queuedata.constants import MOUSEBUTTON

        btn = {
            1: MOUSEBUTTON.MOUSEBUTTON_LEFT,
            2: MOUSEBUTTON.MOUSEBUTTON_MIDDLE,
            3: MOUSEBUTTON.MOUSEBUTTON_RIGHT,
        }.get(button, MOUSEBUTTON.MOUSEBUTTON_LEFT) if isinstance(button, int) else button

        clicks = 2 if double else 1
        for _ in range(clicks):
            await conn.send_mouse(btn, x, y, True)
            await asyncio.sleep(0.05)
            await conn.send_mouse(btn, x, y, False)
            await asyncio.sleep(0.1)

    async def _send_text(conn, text: str, delay: float = 0.02):
        """Type text characters one at a time."""
        for ch in text:
            await conn.send_key_char(ch, True)
            await asyncio.sleep(delay)
            await conn.send_key_char(ch, False)
            await asyncio.sleep(delay)

    # Scancode map for special keys and letter/number keys (make codes)
    _SCANCODE_MAP = {
        "return": (0x1C, False),
        "enter": (0x1C, False),
        "tab": (0x0F, False),
        "escape": (0x01, False),
        "backspace": (0x0E, False),
        "delete": (0x53, True),
        "space": (0x39, False),
        "up": (0x48, True),
        "down": (0x50, True),
        "left": (0x4B, True),
        "right": (0x4D, True),
        "home": (0x47, True),
        "end": (0x4F, True),
        "pageup": (0x49, True),
        "pagedown": (0x51, True),
        "insert": (0x52, True),
        "f1": (0x3B, False),
        "f2": (0x3C, False),
        "f3": (0x3D, False),
        "f4": (0x3E, False),
        "f5": (0x3F, False),
        "f6": (0x40, False),
        "f7": (0x41, False),
        "f8": (0x42, False),
        "f9": (0x43, False),
        "f10": (0x44, False),
        "f11": (0x57, False),
        "f12": (0x58, False),
        # Letter keys (US QWERTY scancodes)
        "a": (0x1E, False), "b": (0x30, False), "c": (0x2E, False),
        "d": (0x20, False), "e": (0x12, False), "f": (0x21, False),
        "g": (0x22, False), "h": (0x23, False), "i": (0x17, False),
        "j": (0x24, False), "k": (0x25, False), "l": (0x26, False),
        "m": (0x32, False), "n": (0x31, False), "o": (0x18, False),
        "p": (0x19, False), "q": (0x10, False), "r": (0x13, False),
        "s": (0x1F, False), "t": (0x14, False), "u": (0x16, False),
        "v": (0x2F, False), "w": (0x11, False), "x": (0x2D, False),
        "y": (0x15, False), "z": (0x2C, False),
        # Number keys
        "0": (0x0B, False), "1": (0x02, False), "2": (0x03, False),
        "3": (0x04, False), "4": (0x05, False), "5": (0x06, False),
        "6": (0x07, False), "7": (0x08, False), "8": (0x09, False),
        "9": (0x0A, False),
    }

    _MODIFIER_SCANCODES = {
        "ctrl": (0x1D, False),
        "alt": (0x38, False),
        "shift": (0x2A, False),
        "super": (0x5B, True),
        "win": (0x5B, True),
    }

    async def _send_key_combo(conn, keys: str):
        """Send a key combination like 'super+r', 'ctrl+c', 'Return'."""
        parts = [k.strip().lower() for k in keys.split("+")]

        # Separate modifiers from the final key
        modifiers = []
        final_key = None
        for part in parts:
            if part in _MODIFIER_SCANCODES:
                modifiers.append(part)
            else:
                final_key = part

        if final_key is None:
            return

        # Look up the final key scancode
        if final_key not in _SCANCODE_MAP:
            return

        sc, is_ext = _SCANCODE_MAP[final_key]

        # Press modifiers
        for mod in modifiers:
            mod_sc, mod_ext = _MODIFIER_SCANCODES[mod]
            await conn.send_key_scancode(mod_sc, True, mod_ext)
            await asyncio.sleep(0.02)

        # Press and release final key
        await conn.send_key_scancode(sc, True, is_ext)
        await asyncio.sleep(0.05)
        await conn.send_key_scancode(sc, False, is_ext)
        await asyncio.sleep(0.02)

        # Release modifiers (reverse order)
        for mod in reversed(modifiers):
            mod_sc, mod_ext = _MODIFIER_SCANCODES[mod]
            await conn.send_key_scancode(mod_sc, False, mod_ext)
            await asyncio.sleep(0.02)

    @mcp.tool()
    async def rdp_connect(
        host: str,
        user: str,
        password: str = "",
        domain: str = "",
        port: int = 3389,
        resolution: str = "1920x1080",
    ) -> str:
        """Connect to an RDP target and return a session with an initial screenshot.

        Uses a pure Python RDP client — no X11, Xvfb, or xfreerdp needed.
        Returns the session ID and an initial screenshot of the desktop.

        Args:
            host: Target hostname or IP.
            user: Username for RDP authentication.
            password: Password for RDP authentication (empty string for blank).
            domain: Optional domain name.
            port: RDP port (default 3389).
            resolution: Display resolution (default "1920x1080").
        """
        from aardwolf.connection import RDPConnection
        from aardwolf.commons.target import RDPTarget
        from aardwolf.commons.iosettings import RDPIOSettings
        from asyauth.common.credentials import UniCredential
        from asyauth.common.constants import asyauthProtocol, asyauthSecret

        session_id = str(uuid.uuid4())[:8]

        try:
            w, h = resolution.split("x")
            width, height = int(w), int(h)
        except ValueError:
            return f"ERROR: Invalid resolution '{resolution}' — expected WxH (e.g., 1920x1080)"

        target = RDPTarget(
            ip=host,
            port=port,
            hostname=host,
            domain=domain or None,
        )
        target.unsafe_ssl = True

        cred = UniCredential()
        cred.protocol = asyauthProtocol.NTLM
        cred.stype = asyauthSecret.PASSWORD
        cred.username = user
        cred.secret = password
        if domain:
            cred.domain = domain

        settings = RDPIOSettings()
        settings.video_width = width
        settings.video_height = height
        settings.video_bpp_min = 15
        settings.video_bpp_max = 32

        conn = RDPConnection(target, cred, settings)

        try:
            ok, err = await conn.connect()
            if err:
                return f"ERROR: RDP connection failed — {err}"
        except Exception as e:
            return f"ERROR: RDP connection failed — {e}"

        session = {
            "session_id": session_id,
            "conn": conn,
            "host": host,
            "port": port,
            "user": user,
            "domain": domain,
            "resolution": resolution,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        sessions[session_id] = session

        # Wait for desktop to render
        await asyncio.sleep(_LOGIN_WAIT)

        # Take initial screenshot
        try:
            screenshot_path = await _take_screenshot(session)
        except Exception:
            screenshot_path = None

        result = {
            "session_id": session_id,
            "host": host,
            "port": port,
            "user": user,
            "domain": domain or "(none)",
            "resolution": resolution,
            "status": "connected",
        }
        if screenshot_path:
            result["screenshot"] = screenshot_path
            result["message"] = (
                f"RDP session established. Initial screenshot saved to {screenshot_path}. "
                "Use rdp_screenshot to view the current display."
            )
        else:
            result["message"] = (
                "RDP session established but initial screenshot failed. "
                "Use rdp_screenshot to check the display."
            )

        return json.dumps(result, indent=2)

    @mcp.tool()
    async def rdp_screenshot(
        session_id: str,
        save_to: str = "",
    ) -> str:
        """Capture a PNG screenshot of the RDP session.

        Returns the screenshot file path. Read the file with the Read tool
        to view it (Claude Code is multimodal and can interpret images).

        Args:
            session_id: Session ID from rdp_connect.
            save_to: Optional path to save screenshot. Defaults to
                     engagement/evidence/rdp-<timestamp>.png.
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        session = sessions[session_id]

        try:
            if save_to:
                from aardwolf.commons.queuedata.constants import VIDEO_FORMAT

                path = Path(save_to)
                path.parent.mkdir(parents=True, exist_ok=True)
                buf = session["conn"].get_desktop_buffer(VIDEO_FORMAT.PIL)
                if buf is None:
                    return "ERROR: No desktop buffer available"
                buf.save(str(path))
                screenshot_path = str(path)
            else:
                screenshot_path = await _take_screenshot(session)
        except Exception as e:
            return f"ERROR: Screenshot failed — {e}"

        return json.dumps(
            {
                "screenshot": screenshot_path,
                "session_id": session_id,
                "host": session["host"],
                "message": f"Screenshot saved to {screenshot_path}",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_click(
        session_id: str,
        x: int,
        y: int,
        button: int = 1,
    ) -> str:
        """Click at coordinates in the RDP session.

        Args:
            session_id: Session ID from rdp_connect.
            x: X coordinate (pixels from left).
            y: Y coordinate (pixels from top).
            button: Mouse button — 1=left, 2=middle, 3=right.
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        try:
            await _send_click(sessions[session_id]["conn"], x, y, button)
        except Exception as e:
            return f"ERROR: Click failed — {e}"

        return json.dumps(
            {
                "action": "click",
                "x": x,
                "y": y,
                "button": button,
                "message": f"Clicked ({x}, {y}) button={button}",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_double_click(
        session_id: str,
        x: int,
        y: int,
    ) -> str:
        """Double-click at coordinates in the RDP session.

        Args:
            session_id: Session ID from rdp_connect.
            x: X coordinate.
            y: Y coordinate.
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        try:
            await _send_click(sessions[session_id]["conn"], x, y, 1, double=True)
        except Exception as e:
            return f"ERROR: Double-click failed — {e}"

        return json.dumps(
            {
                "action": "double_click",
                "x": x,
                "y": y,
                "message": f"Double-clicked ({x}, {y})",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_type(
        session_id: str,
        text: str,
        delay_ms: int = 20,
    ) -> str:
        """Type text in the RDP session.

        For special keys (Enter, Tab, etc.), use rdp_key instead.

        Args:
            session_id: Session ID from rdp_connect.
            text: Text to type.
            delay_ms: Milliseconds between keystrokes (default 20).
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        try:
            await _send_text(
                sessions[session_id]["conn"], text, delay=delay_ms / 1000.0
            )
        except Exception as e:
            return f"ERROR: Type failed — {e}"

        return json.dumps(
            {
                "action": "type",
                "text_length": len(text),
                "delay_ms": delay_ms,
                "message": f"Typed {len(text)} characters",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_key(
        session_id: str,
        keys: str,
    ) -> str:
        """Send special key combinations to the RDP session.

        Common examples:
        - "Return" — Enter key
        - "Tab" — Tab key
        - "Escape" — Escape key
        - "super+r" — Win+R (Run dialog)
        - "ctrl+c" — Ctrl+C
        - "ctrl+shift+escape" — Task Manager
        - "alt+f4" — Close window
        - "ctrl+a" — Select all
        - "BackSpace" — Backspace
        - "Delete" — Delete

        Args:
            session_id: Session ID from rdp_connect.
            keys: Key combination (e.g., "super+r", "Return", "ctrl+c").
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        try:
            await _send_key_combo(sessions[session_id]["conn"], keys)
        except Exception as e:
            return f"ERROR: Key failed — {e}"

        return json.dumps(
            {
                "action": "key",
                "keys": keys,
                "message": f"Sent key: {keys}",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_execute(
        session_id: str,
        command: str,
        wait_seconds: float = 3.0,
    ) -> str:
        """Execute a command via Win+R Run dialog and return a screenshot.

        Convenience tool that chains: Win+R, wait, type command, Enter,
        wait for output, screenshot. This is the most common RDP operation
        for pentesting — running commands and reading output visually.

        Args:
            session_id: Session ID from rdp_connect.
            command: Command to execute (e.g., "cmd /c whoami",
                     "powershell -c Get-Process", "notepad").
            wait_seconds: Seconds to wait after pressing Enter before
                          taking a screenshot (default 3.0).
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        session = sessions[session_id]
        conn = session["conn"]

        try:
            # Win+R to open Run dialog
            await _send_key_combo(conn, "super+r")
            await asyncio.sleep(1.0)

            # Type the command
            await _send_text(conn, command)
            await asyncio.sleep(0.3)

            # Press Enter
            await _send_key_combo(conn, "Return")

            # Wait for command output
            await asyncio.sleep(wait_seconds)

            # Take screenshot
            screenshot_path = await _take_screenshot(session)
        except Exception as e:
            return f"ERROR: Execute failed — {e}"

        return json.dumps(
            {
                "action": "execute",
                "command": command,
                "wait_seconds": wait_seconds,
                "screenshot": screenshot_path,
                "message": (
                    f"Executed via Win+R: {command}. "
                    f"Screenshot saved to {screenshot_path}. "
                    "Read the screenshot file to see the output."
                ),
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_scroll(
        session_id: str,
        direction: str = "down",
        clicks: int = 3,
    ) -> str:
        """Scroll in the RDP session.

        Args:
            session_id: Session ID from rdp_connect.
            direction: "up" or "down" (default "down").
            clicks: Number of scroll clicks (default 3).
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        from aardwolf.commons.queuedata.constants import MOUSEBUTTON

        conn = sessions[session_id]["conn"]
        btn = (
            MOUSEBUTTON.MOUSEBUTTON_WHEEL_UP
            if direction == "up"
            else MOUSEBUTTON.MOUSEBUTTON_WHEEL_DOWN
        )

        try:
            for _ in range(clicks):
                await conn.send_mouse(btn, 960, 540, True, steps=3)
                await asyncio.sleep(0.05)
                await conn.send_mouse(btn, 960, 540, False, steps=3)
                await asyncio.sleep(0.05)
        except Exception as e:
            return f"ERROR: Scroll failed — {e}"

        return json.dumps(
            {
                "action": "scroll",
                "direction": direction,
                "clicks": clicks,
                "message": f"Scrolled {direction} {clicks} clicks",
            },
            indent=2,
        )

    @mcp.tool()
    async def rdp_close(
        session_id: str,
    ) -> str:
        """Close an RDP session.

        Args:
            session_id: Session ID to close.
        """
        if session_id not in sessions:
            available = ", ".join(sessions.keys()) if sessions else "none"
            return f"ERROR: Session '{session_id}' not found. Available: {available}"

        session = sessions.pop(session_id)

        try:
            await session["conn"].terminate()
        except Exception:
            pass

        return json.dumps(
            {
                "status": "closed",
                "session_id": session_id,
                "host": session["host"],
                "message": "RDP session closed.",
            },
            indent=2,
        )

    @mcp.tool()
    async def list_rdp_sessions() -> str:
        """List all active RDP sessions.

        Returns a summary of all open RDP sessions with their targets
        and creation timestamps.
        """
        if not sessions:
            return "No active RDP sessions. Use rdp_connect() to start one."

        result = []
        for sid, session in sessions.items():
            result.append(
                {
                    "session_id": sid,
                    "host": session["host"],
                    "port": session["port"],
                    "user": session["user"],
                    "domain": session.get("domain") or "(none)",
                    "resolution": session["resolution"],
                    "created_at": session["created_at"],
                }
            )

        return json.dumps({"sessions": result}, indent=2)

    return mcp


def main() -> None:
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
