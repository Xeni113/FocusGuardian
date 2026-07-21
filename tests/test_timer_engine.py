from src.timer_engine import TimerEngine


def test_initial_state():
    timer = TimerEngine()

    assert timer.reminder_delay == 10
    assert timer.start_time is None
    assert timer.current_target is None


def test_custom_reminder_delay():
    timer = TimerEngine(reminder_delay=30)

    assert timer.reminder_delay == 30


def test_first_target_starts_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    monkeypatch.setattr("src.timer_engine.time.time", lambda: 100.0)

    result = timer.update("youtube")

    assert result is False
    assert timer.current_target == "youtube"
    assert timer.start_time == 100.0


def test_same_target_before_delay(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 105.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False
    assert timer.update("youtube") is False


def test_same_target_exactly_at_delay(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 110.0, 110.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False
    assert timer.update("youtube") is True

    assert timer.start_time == 110.0


def test_same_target_after_delay(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 115.0, 115.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False
    assert timer.update("youtube") is True

    assert timer.start_time == 115.0


def test_timer_restarts_after_trigger(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 110.0, 110.0, 115.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False

    assert timer.update("youtube") is True

    assert timer.update("youtube") is False


def test_switching_target_restarts_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 105.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False

    result = timer.update("reddit")

    assert result is False
    assert timer.current_target == "reddit"
    assert timer.start_time == 105.0


def test_switching_target_does_not_trigger_old_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 120.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False

    result = timer.update("reddit")

    assert result is False
    assert timer.current_target == "reddit"
    assert timer.start_time == 120.0


def test_reset():
    timer = TimerEngine()

    timer.current_target = "youtube"
    timer.start_time = 100.0

    timer.reset()

    assert timer.current_target is None
    assert timer.start_time is None


def test_update_after_reset_starts_fresh_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    timer.current_target = "youtube"
    timer.start_time = 100.0

    timer.reset()

    monkeypatch.setattr("src.timer_engine.time.time", lambda: 500.0)

    result = timer.update("youtube")

    assert result is False
    assert timer.current_target == "youtube"
    assert timer.start_time == 500.0


def test_zero_delay_triggers_on_second_update(monkeypatch):
    timer = TimerEngine(reminder_delay=0)

    times = iter([100.0, 100.0, 100.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    assert timer.update("youtube") is False
    assert timer.update("youtube") is True


def test_none_target_on_new_timer_is_safe():
    timer = TimerEngine(reminder_delay=10)

    result = timer.update(None)

    assert result is False
    assert timer.current_target is None
    assert timer.start_time is None


def test_none_target_resets_active_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    monkeypatch.setattr("src.timer_engine.time.time", lambda: 100.0)

    timer.update("youtube")

    assert timer.current_target == "youtube"
    assert timer.start_time == 100.0

    result = timer.update(None)

    assert result is False
    assert timer.current_target is None
    assert timer.start_time is None


def test_target_after_none_starts_fresh_timer(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    times = iter([100.0, 500.0])

    monkeypatch.setattr("src.timer_engine.time.time", lambda: next(times))

    timer.update("youtube")

    timer.update(None)

    result = timer.update("youtube")

    assert result is False
    assert timer.current_target == "youtube"
    assert timer.start_time == 500.0


def test_missing_start_time_recovers_safely(monkeypatch):
    timer = TimerEngine(reminder_delay=10)

    timer.current_target = "youtube"
    timer.start_time = None

    monkeypatch.setattr("src.timer_engine.time.time", lambda: 300.0)

    result = timer.update("youtube")

    assert result is False
    assert timer.current_target == "youtube"
    assert timer.start_time == 300.0
