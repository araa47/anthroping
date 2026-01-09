#!/usr/bin/env python3
"""
anthroping - macOS notifications for Claude Code

Usage:
  anthroping <event> [options]

Events:
  done      Work completed successfully
  input     Claude needs your input
  error     Something went wrong
  waiting   Claude is waiting for approval
  thinking  Long task in progress
  subagent  Background task (subagent) finished

Options:
  --alert            Show as popup dialog (always visible)
  --project PATH     Include project name and enable "Go to Window" button
  --app NAME         Editor app for window switching (cursor, vscode, default: cursor)
  --sound NAME       Override the default sound for this event
  --title TEXT       Override the title
  --message TEXT     Override the message
  --icon EMOJI       Override the icon
  --timeout SECONDS  Alert auto-dismiss timeout (default: 10)
  --sounds           List available macOS sounds
"""

import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import TypedDict


class EventConfig(TypedDict):
    """Event configuration with all required fields."""

    title: str
    message: str
    sound: str
    subtitle: str
    icon: str


class NotificationEvent(Enum):
    DONE = "done"
    INPUT = "input"
    ERROR = "error"
    WAITING = "waiting"
    THINKING = "thinking"
    SUBAGENT = "subagent"  # For SubagentStop hooks (v1.0.41+)


DEFAULT_EVENTS: dict[NotificationEvent, EventConfig] = {
    NotificationEvent.DONE: {
        "title": "Claude Complete",
        "message": "Work finished successfully!",
        "sound": "Glass",
        "subtitle": "Ready for review",
        "icon": "✅",
    },
    NotificationEvent.INPUT: {
        "title": "Input Needed",
        "message": "Claude is waiting for your response",
        "sound": "Ping",
        "subtitle": "Action required",
        "icon": "🤔",
    },
    NotificationEvent.ERROR: {
        "title": "Error Occurred",
        "message": "Something needs your attention",
        "sound": "Basso",
        "subtitle": "Check Claude",
        "icon": "❌",
    },
    NotificationEvent.WAITING: {
        "title": "Awaiting Approval",
        "message": "Claude needs permission to continue",
        "sound": "Purr",
        "subtitle": "Approve to proceed",
        "icon": "⏳",
    },
    NotificationEvent.THINKING: {
        "title": "Still Working",
        "message": "Long task in progress...",
        "sound": "Pop",
        "subtitle": "Be patient",
        "icon": "🧠",
    },
    NotificationEvent.SUBAGENT: {
        "title": "Subagent Complete",
        "message": "Background task finished",
        "sound": "Blow",
        "subtitle": "Check results",
        "icon": "🔧",
    },
}


def sanitize_for_applescript(text: str) -> str:
    """Escape special characters for safe AppleScript string embedding."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def play_sound(sound_name: str) -> None:
    """Play a macOS system sound."""
    sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
    if Path(sound_path).exists():
        subprocess.Popen(["afplay", sound_path])


def send_notification(config: EventConfig) -> None:
    """Send a macOS notification with sound."""
    title = sanitize_for_applescript(f"{config['icon']} {config['title']}")
    message = sanitize_for_applescript(config["message"])
    subtitle = sanitize_for_applescript(config["subtitle"])
    sound = sanitize_for_applescript(config["sound"])
    script = f"""
    display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"
    """
    subprocess.run(["osascript", "-e", script], check=True)


APP_NAMES: dict[str, str] = {
    "cursor": "Cursor",
    "vscode": "Code",
    "code": "Code",
}


def send_alert_dialog(
    config: EventConfig,
    project_path: str | None = None,
    timeout: int = 10,
    app: str = "cursor",
) -> None:
    """Send a popup alert dialog that stays visible until dismissed."""
    # Ensure timeout is within reasonable bounds (1-300 seconds)
    timeout = max(1, min(timeout, 300))
    play_sound(config["sound"])

    # Sanitize all user-controllable inputs
    icon = sanitize_for_applescript(config["icon"])
    message = sanitize_for_applescript(config["message"])
    title = sanitize_for_applescript(config["title"])

    project_name = ""
    if project_path:
        project_name = sanitize_for_applescript(project_path.rstrip("/").split("/")[-1])

    app_name = APP_NAMES.get(app.lower(), "Cursor")

    if project_name:
        script = f"""
        set dialogResult to display dialog "{icon} {message}

Project: {project_name}" with title "{title}" buttons {{"OK", "Go to Window"}} default button "Go to Window" giving up after {timeout}
        if button returned of dialogResult is "Go to Window" then
            tell application "System Events"
                tell process "{app_name}"
                    set frontmost to true
                    set windowList to every window
                    repeat with w in windowList
                        set winName to name of w
                        if winName contains "{project_name}" then
                            perform action "AXRaise" of w
                            exit repeat
                        end if
                    end repeat
                end tell
            end tell
            tell application "{app_name}" to activate
        end if
        """
    else:
        script = f"""
        display dialog "{icon} {message}" with title "{title}" buttons {{"OK"}} default button "OK" giving up after {timeout}
        """

    subprocess.Popen(["osascript", "-e", script])


def list_sounds() -> None:
    """List available macOS system sounds."""
    sound_dir = Path("/System/Library/Sounds")
    if sound_dir.exists():
        sounds = sorted(p.stem for p in sound_dir.glob("*.aiff"))
        print("Available macOS sounds:")
        for sound in sounds:
            print(f"  {sound}")


def parse_arg(args: list[str], flag: str) -> str | None:
    """Extract a flag value from args, modifying args in place."""
    if flag in args:
        idx = args.index(flag)
        args.pop(idx)
        if idx < len(args):
            return args.pop(idx)
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    args = sys.argv[1:]

    # Handle --sounds command
    if "--sounds" in args:
        list_sounds()
        return

    # Parse flags
    use_alert = "--alert" in args
    if use_alert:
        args.remove("--alert")

    project_path = parse_arg(args, "--project")
    app = parse_arg(args, "--app") or "cursor"
    sound_override = parse_arg(args, "--sound")
    title_override = parse_arg(args, "--title")
    message_override = parse_arg(args, "--message")
    icon_override = parse_arg(args, "--icon")
    timeout_str = parse_arg(args, "--timeout")
    timeout = int(timeout_str) if timeout_str else 10

    if not args:
        print("Error: No event specified")
        sys.exit(1)

    event_name = args[0].lower()

    try:
        event = NotificationEvent(event_name)
    except ValueError:
        print(f"Unknown event: {event_name}")
        print(f"Valid events: {', '.join(e.value for e in NotificationEvent)}")
        sys.exit(1)

    # Build config from defaults + overrides
    defaults = DEFAULT_EVENTS[event]
    config: EventConfig = {
        "title": title_override or defaults["title"],
        "message": message_override or defaults["message"],
        "sound": sound_override or defaults["sound"],
        "subtitle": defaults["subtitle"],
        "icon": icon_override or defaults["icon"],
    }

    if use_alert:
        send_alert_dialog(config, project_path, timeout, app)
    else:
        send_notification(config)

    print(f"🔔 {config['title']}")


if __name__ == "__main__":
    main()
