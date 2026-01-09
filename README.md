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

| Event | Description | Default Sound |
|-------|-------------|---------------|
| `done` | Work completed successfully | Glass |
| `input` | Claude needs your input | Ping |
| `error` | Something went wrong | Basso |
| `waiting` | Claude is waiting for approval | Purr |
| `thinking` | Long task in progress | Pop |

## Options

| Option | Description |
|--------|-------------|
| `--alert` | Show as popup dialog instead of notification |
| `--project PATH` | Include project name and "Go to Window" button for Cursor |
| `--sound NAME` | Override the default sound |
| `--title TEXT` | Override the title |
| `--message TEXT` | Override the message |
| `--icon EMOJI` | Override the icon |
| `--timeout SEC` | Alert auto-dismiss timeout (default: 10) |
| `--sounds` | List available macOS sounds |

## Customization

Customize directly in your hooks - no config file needed:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uvx --from git+https://github.com/araa47/anthroping anthroping done --alert --project \"$PWD\" --sound Funk --icon 🎉"
          }
        ]
      }
    ]
  }
}
```

### Available Sounds

Run `anthroping --sounds` to list all available macOS sounds:

```
Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink
```

## Examples

```bash
# Basic notification
anthroping done

# Alert popup with custom sound
anthroping done --alert --sound Funk

# Custom everything
anthroping done --alert --sound Hero --title "All Done!" --icon 🎉

# With project (for Cursor integration)
anthroping input --alert --project /path/to/project
```

## Alert vs Notification

- **Notification** (default): Standard macOS notification. May be missed if Do Not Disturb is on.
- **Alert** (`--alert`): Popup dialog that stays visible until dismissed. Recommended for hooks.

## Development

```bash
git clone https://github.com/araa47/anthroping
cd anthroping
uv sync --all-extras --dev
uv run anthroping done --alert
```
