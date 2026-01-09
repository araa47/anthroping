from anthroping import DEFAULT_EVENTS, NotificationEvent, parse_arg


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
    }
    for event, sound in expected_sounds.items():
        assert DEFAULT_EVENTS[event]["sound"] == sound
