from src.session_engine import SessionEngine


def test_initial_state():
    engine = SessionEngine()

    assert engine.current_target is None
    assert engine.start_time is None
    assert engine.is_active() is False
    assert engine.get_current_session() is None


def test_start_session(monkeypatch):
    engine = SessionEngine()

    monkeypatch.setattr("src.session_engine.time.time", lambda: 100.0)

    engine.start_session("youtube")

    assert engine.current_target == "youtube"
    assert engine.start_time == 100.0
    assert engine.is_active() is True


def test_start_session_with_none_does_nothing():
    engine = SessionEngine()

    engine.start_session(None)

    assert engine.current_target is None
    assert engine.start_time is None
    assert engine.is_active() is False


def test_end_session(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 115.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")
    result = engine.end_session()

    assert result == {
        "target": "youtube",
        "duration": 15,
    }

    assert engine.current_target is None
    assert engine.start_time is None
    assert engine.is_active() is False


def test_end_session_when_inactive():
    engine = SessionEngine()

    assert engine.end_session() is None


def test_same_target_does_not_restart_session(monkeypatch):
    engine = SessionEngine()

    monkeypatch.setattr("src.session_engine.time.time", lambda: 100.0)

    engine.start_session("youtube")

    original_start_time = engine.start_time

    result = engine.switch_target("youtube")

    assert result is None
    assert engine.current_target == "youtube"
    assert engine.start_time == original_start_time


def test_switch_from_none_to_target(monkeypatch):
    engine = SessionEngine()

    monkeypatch.setattr("src.session_engine.time.time", lambda: 200.0)

    result = engine.switch_target("youtube")

    assert result is None
    assert engine.current_target == "youtube"
    assert engine.start_time == 200.0


def test_switch_from_target_to_none(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 120.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")

    result = engine.switch_target(None)

    assert result == {
        "target": "youtube",
        "duration": 20,
    }

    assert engine.current_target is None
    assert engine.start_time is None


def test_switch_between_targets(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 110.0, 110.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")

    old_session = engine.switch_target("instagram")

    assert old_session == {
        "target": "youtube",
        "duration": 10,
    }

    assert engine.current_target == "instagram"
    assert engine.start_time == 110.0


def test_get_current_session(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 112.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")

    session = engine.get_current_session()

    assert session == {
        "target": "youtube",
        "duration": 12,
    }


def test_negative_duration_is_clamped_to_zero(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 90.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")

    result = engine.end_session()

    assert result["duration"] == 0


def test_multiple_independent_sessions(monkeypatch):
    engine = SessionEngine()

    times = iter([100.0, 115.0, 200.0, 210.0])

    monkeypatch.setattr("src.session_engine.time.time", lambda: next(times))

    engine.start_session("youtube")
    first_session = engine.end_session()

    engine.start_session("youtube")
    second_session = engine.end_session()

    assert first_session == {
        "target": "youtube",
        "duration": 15,
    }

    assert second_session == {
        "target": "youtube",
        "duration": 10,
    }
