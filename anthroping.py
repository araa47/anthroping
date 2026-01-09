#!/usr/bin/env python3
"""
anthroping - macOS notifications for Claude Code

Get notified when Claude Code needs your attention with distinct sounds for different events.

Usage:
  uvx anthroping <event> [message] [--alert] [--project PATH]
  anthroping <event> [message] [--alert] [--project PATH]

Events:
  done      Work completed successfully
  input     Claude needs your input
  error     Something went wrong
  waiting   Claude is waiting for approval
  thinking  Long task in progress

Options:
  --alert           Show as popup dialog (always visible, bypasses notification settings)
  --project PATH    Include project name in alert and enable "Go to Window" button
"""

import subprocess
import sys
from enum import Enum


class NotificationEvent(Enum):
    DONE = "done"
    INPUT = "input"
    ERROR = "error"
    WAITING = "waiting"
    THINKING = "thinking"


# Event configurations with distinct sounds and messages
EVENTS = {
    NotificationEvent.DONE: {
        "title": "✅ Claude Complete",
        "message": "Work finished successfully!",
        "sound": "Glass",  # Pleasant completion sound
        "subtitle": "Ready for review",
        "icon": "✅",
    },
    NotificationEvent.INPUT: {
        "title": "🤔 Input Needed",
        "message": "Claude is waiting for your response",
        "sound": "Ping",  # Attention-grabbing but not alarming
        "subtitle": "Action required",
        "icon": "🤔",
    },
    NotificationEvent.ERROR: {
        "title": "❌ Error Occurred",
        "message": "Something needs your attention",
        "sound": "Basso",  # Deep sound for errors
        "subtitle": "Check Claude",
        "icon": "❌",
    },
    NotificationEvent.WAITING: {
        "title": "⏳ Awaiting Approval",
        "message": "Claude needs permission to continue",
        "sound": "Purr",  # Gentle reminder
        "subtitle": "Approve to proceed",
        "icon": "⏳",
    },
    NotificationEvent.THINKING: {
        "title": "🧠 Still Working",
        "message": "Long task in progress...",
        "sound": "Pop",  # Soft notification
        "subtitle": "Be patient",
        "icon": "🧠",
    },
}


def play_sound(sound_name: str) -> None:
    """Play a system sound."""
    sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
    subprocess.Popen(["afplay", sound_path])  # Non-blocking


def send_notification(
    event: NotificationEvent,
    custom_message: str | None = None,
) -> None:
    """Send a macOS notification with sound."""
    config = EVENTS[event]
    message = custom_message or config["message"]

    # AppleScript for rich notification
    script = f'''
    display notification "{message}" with title "{config["title"]}" subtitle "{config["subtitle"]}" sound name "{config["sound"]}"
    '''
    subprocess.run(["osascript", "-e", script], check=True)


def send_alert_dialog(
    event: NotificationEvent,
    custom_message: str | None = None,
    project_path: str | None = None,
) -> None:
    """Send a popup alert dialog - ALWAYS visible, can't be missed!"""
    config = EVENTS[event]
    message = custom_message or config["message"]

    # Play sound first (non-blocking)
    play_sound(config["sound"])

    # Extract project name from path for window matching
    project_name = ""
    if project_path:
        project_name = project_path.rstrip("/").split("/")[-1]

    # AppleScript to show alert and optionally go to matching Cursor window
    if project_name:
        script = f'''
        set dialogResult to display dialog "{config["icon"]} {message}

Project: {project_name}" with title "{config["title"]}" buttons {{"OK", "Go to Window"}} default button "Go to Window" giving up after 10
        if button returned of dialogResult is "Go to Window" then
            tell application "System Events"
                tell process "Cursor"
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
            tell application "Cursor" to activate
        end if
        '''
    else:
        script = f'''
        display dialog "{config["icon"]} {message}" with title "{config["title"]}" buttons {{"OK"}} default button "OK" giving up after 8
        '''

    subprocess.Popen(["osascript", "-e", script])  # Non-blocking


def send_say_notification(
    event: NotificationEvent,
    custom_message: str | None = None,
) -> None:
    """Speak the notification out loud."""
    config = EVENTS[event]
    message = custom_message or config["message"]
    # Use macOS say command for voice notification
    subprocess.Popen(["say", "-v", "Samantha", message])


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable events:")
        for event in NotificationEvent:
            config = EVENTS[event]
            print(f"  {event.value:10} - {config['title']}")
        print("\nExamples:")
        print("  anthroping done")
        print("  anthroping input --alert")
        print("  anthroping done --alert --project /path/to/project")
        print("  uvx anthroping done --alert")
        sys.exit(1)

    # Parse args
    args = sys.argv[1:]
    use_alert = "--alert" in args
    project_path = None

    if use_alert:
        args.remove("--alert")

    # Extract --project argument
    if "--project" in args:
        idx = args.index("--project")
        args.pop(idx)
        if idx < len(args):
            project_path = args.pop(idx)

    event_name = args[0].lower()
    custom_message = " ".join(args[1:]) if len(args) > 1 else None

    # Match event
    try:
        event = NotificationEvent(event_name)
    except ValueError:
        print(f"Unknown event: {event_name}")
        print(f"Valid events: {', '.join(e.value for e in NotificationEvent)}")
        sys.exit(1)

    if use_alert:
        send_alert_dialog(event, custom_message, project_path)
        print(f"🔔 Alert shown: {EVENTS[event]['title']}")
    else:
        send_notification(event, custom_message)
        print(f"🔔 Notification sent: {EVENTS[event]['title']}")


if __name__ == "__main__":
    main()

