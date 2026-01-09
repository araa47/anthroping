# Anthroping

macOS notification utility for Claude Code hooks. Sends alerts/notifications when Claude finishes work or needs input.

## Structure

```
anthroping.py     # Main CLI - all logic in one file
tests/            # pytest tests
```

## Commands

```bash
uv run anthroping done --alert          # Test locally
uv run pytest                           # Run tests
uv run ruff check .                     # Lint
```

## Install Options

```bash
# Fast: install globally so `anthroping` command works everywhere
uv tool install git+https://github.com/araa47/anthroping

# Slow: run via uvx (fetches each time)
uvx --from git+https://github.com/araa47/anthroping anthroping done
```

## Code Style

- Python 3.13+, strict type hints
- Ruff linting (E, F, B rules)
- Single-file architecture - keep it simple

## Key Components

- `NotificationEvent` enum: done, input, error, waiting, thinking, subagent
- `DEFAULT_EVENTS` dict: default config for each event (title, message, sound, subtitle, icon)
- `APP_NAMES` dict: maps app flags to process names (cursor→Cursor, vscode→Code)
- `sanitize_for_applescript()`: escapes special characters to prevent injection
- `parse_arg()`: extracts CLI flags
- `send_notification()`: macOS notification via AppleScript
- `send_alert_dialog()`: popup dialog via AppleScript with Cursor/VS Code integration

## CLI Flags

All customization via CLI - no config file:
- `--alert`: popup instead of notification
- `--sound NAME`: override sound
- `--title TEXT`: override title
- `--message TEXT`: override message
- `--icon EMOJI`: override icon
- `--project PATH`: window integration (extracts project name)
- `--app NAME`: editor app (cursor, vscode)
- `--timeout SEC`: alert dismiss timeout
