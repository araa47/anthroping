# anthroping

macOS notifications for Claude Code. Get notified when Claude finishes work or needs your input.

## Requirements

- macOS
- [uv](https://github.com/astral-sh/uv) installed (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Setup Notifications

For notifications to work, grant permission to Script Editor (which runs the AppleScript):

1. Open **System Settings** > **Notifications**
2. Find **Script Editor** and enable **Allow Notifications**
3. Set alert style to **Alerts** or **Banners** as preferred

If Script Editor doesn't appear in the list, run this first to trigger the permission prompt:

```bash
osascript -e 'display notification "Test" with title "Test"'
```

## Quick Start

Add this to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uvx --from git+https://github.com/araa47/anthroping anthroping done --alert --project \"$PWD\""
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uvx --from git+https://github.com/araa47/anthroping anthroping input --alert --project \"$PWD\""
          }
        ]
      }
    ]
  }
}
```

That's it! No installation required - `uvx` fetches and runs the tool directly from GitHub.

## Events

| Event | Description | Sound |
|-------|-------------|-------|
| `done` | Work completed successfully | Glass |
| `input` | Claude needs your input | Ping |
| `error` | Something went wrong | Basso |
| `waiting` | Claude is waiting for approval | Purr |
| `thinking` | Long task in progress | Pop |

## Options

| Option | Description |
|--------|-------------|
| `--alert` | Show as popup dialog instead of notification (always visible, can't be missed) |
| `--project PATH` | Include project name in alert and show "Go to Window" button for Cursor |

## Examples

```bash
# Simple notification (from GitHub)
uvx --from git+https://github.com/araa47/anthroping anthroping done

# Alert popup (recommended for hooks)
uvx --from git+https://github.com/araa47/anthroping anthroping input --alert

# With project path (shows "Go to Window" button)
uvx --from git+https://github.com/araa47/anthroping anthroping done --alert --project /path/to/project

# If installed locally
anthroping done --alert
```

## Alert vs Notification

- **Notification** (default): Standard macOS notification that appears in the corner. May be missed if Do Not Disturb is on.
- **Alert** (`--alert`): Popup dialog that stays on screen until dismissed. Recommended for Claude Code hooks since you won't miss it.

## Development

```bash
# Clone and setup
git clone https://github.com/araa47/anthroping
cd anthroping

# If using direnv
direnv allow

# Or manually with uv
uv sync --all-extras --dev

# Run locally
uv run anthroping done --alert
```
