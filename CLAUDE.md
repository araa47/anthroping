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

## Code Style

- Python 3.13+, strict type hints
- Ruff linting (E, F, B rules)
- Single-file architecture - keep it simple

## Key Components

- `NotificationEvent` enum: done, input, error, waiting, thinking
- `DEFAULT_EVENTS` dict: default config for each event (title, message, sound, subtitle, icon)
- `parse_arg()`: extracts CLI flags
- `send_notification()`: macOS notification via AppleScript
- `send_alert_dialog()`: popup dialog via AppleScript with Cursor integration

## CLI Flags

All customization via CLI - no config file:
- `--alert`: popup instead of notification
- `--sound NAME`: override sound
- `--title TEXT`: override title
- `--message TEXT`: override message
- `--icon EMOJI`: override icon
- `--project PATH`: Cursor window integration
- `--timeout SEC`: alert dismiss timeout
