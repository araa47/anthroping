# Anthroping

macOS notification utility for Claude Code hooks. Sends alerts/notifications when Claude finishes work or needs input.

## Project Structure

```
anthroping.py     # Main CLI - all logic in one file
pyproject.toml    # Project config (hatchling build)
tests/            # pytest tests
```

## Commands

```bash
# Run locally
uv run anthroping done --alert

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run pyright
```

## Code Style

- Python 3.13+
- Strict pyright type checking
- Ruff for linting (E, F, B rules)
- Line length: 80 chars (isort), no E501 enforcement (ruff)

## Key Patterns

- `NotificationEvent` enum for event types (done, input, error, waiting, thinking)
- Each event has: title, message, sound, subtitle, icon
- Two notification modes: standard notification vs alert dialog (--alert flag)
- AppleScript for macOS notifications and Cursor window management

## Testing

Tests use pytest. Run with `uv run pytest tests/`.

## Integration

Used as a Claude Code hook via uvx:
```bash
uvx --from git+https://github.com/araa47/anthroping anthroping done --alert --project "$PWD"
```
