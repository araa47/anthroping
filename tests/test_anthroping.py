from typing import Any
from unittest.mock import MagicMock, patch

from anthroping import (
    DEFAULT_EVENTS,
    NotificationEvent,
    parse_arg,
    sanitize_for_applescript,
    send_alert_dialog,
)


def test_all_events_have_config():
    """Every event type should have a complete configuration."""
    for event in NotificationEvent:
        config = DEFAULT_EVENTS[event]
        assert "title" in config
        assert "message" in config
        assert "sound" in config
        assert "subtitle" in config
        assert "icon" in config


def test_event_values():
    """Event enum values should match expected strings."""
    assert NotificationEvent.DONE.value == "done"
    assert NotificationEvent.INPUT.value == "input"
    assert NotificationEvent.ERROR.value == "error"
    assert NotificationEvent.WAITING.value == "waiting"
    assert NotificationEvent.THINKING.value == "thinking"
    assert NotificationEvent.SUBAGENT.value == "subagent"


def test_parse_arg_extracts_value():
    """parse_arg extracts flag value and modifies args in place."""
    args = ["done", "--sound", "Funk", "--alert"]
    result = parse_arg(args, "--sound")
    assert result == "Funk"
    assert args == ["done", "--alert"]


def test_parse_arg_returns_none_if_missing():
    """parse_arg returns None if flag not present."""
    args = ["done", "--alert"]
    result = parse_arg(args, "--sound")
    assert result is None
    assert args == ["done", "--alert"]


def test_default_sounds():
    """Default sounds should be set for all events."""
    expected_sounds = {
        NotificationEvent.DONE: "Glass",
        NotificationEvent.INPUT: "Ping",
        NotificationEvent.ERROR: "Basso",
        NotificationEvent.WAITING: "Purr",
        NotificationEvent.THINKING: "Pop",
        NotificationEvent.SUBAGENT: "Blow",
    }
    for event, sound in expected_sounds.items():
        assert DEFAULT_EVENTS[event]["sound"] == sound


def test_sanitize_for_applescript():
    """sanitize_for_applescript should escape special characters."""
    assert sanitize_for_applescript('Hello "World"') == 'Hello \\"World\\"'
    assert sanitize_for_applescript("path\\to\\file") == "path\\\\to\\\\file"
    assert sanitize_for_applescript("normal text") == "normal text"
    assert sanitize_for_applescript('mixed "quotes" and \\slashes') == (
        'mixed \\"quotes\\" and \\\\slashes'
    )


@patch("anthroping.subprocess.Popen")
@patch("anthroping.play_sound")
def test_send_alert_dialog_timeout_bounds(
    _mock_play_sound: MagicMock, mock_popen: MagicMock
) -> None:
    """send_alert_dialog should clamp timeout to reasonable bounds."""
    config = DEFAULT_EVENTS[NotificationEvent.DONE]

    # Test that very large timeout is clamped to 300
    send_alert_dialog(config, timeout=9999)
    call_args: Any = mock_popen.call_args[0][0]
    script: str = call_args[2]  # osascript -e <script>
    assert "giving up after 300" in script

    # Test that negative timeout is clamped to 1
    send_alert_dialog(config, timeout=-5)
    call_args = mock_popen.call_args[0][0]
    script = call_args[2]
    assert "giving up after 1" in script

    # Test that zero timeout is clamped to 1
    send_alert_dialog(config, timeout=0)
    call_args = mock_popen.call_args[0][0]
    script = call_args[2]
    assert "giving up after 1" in script
