from anthroping import NotificationEvent, EVENTS


def test_all_events_have_config():
    """Every event type should have a complete configuration."""
    for event in NotificationEvent:
        config = EVENTS[event]
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
