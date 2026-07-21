import json

from src import time_stats_engine


def test_load_stats_missing_file(monkeypatch):
    monkeypatch.setattr(time_stats_engine.os.path, "exists", lambda path: False)

    assert time_stats_engine.load_stats() == {}


def test_load_stats_existing_file(tmp_path, monkeypatch):
    test_file = tmp_path / "time_stats.json"

    test_data = {"2026-07-21": {"youtube": 30}}

    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    monkeypatch.setattr(time_stats_engine, "STATS_FILE", str(test_file))

    assert time_stats_engine.load_stats() == test_data


def test_save_stats(tmp_path, monkeypatch):
    test_file = tmp_path / "time_stats.json"

    monkeypatch.setattr(time_stats_engine, "STATS_FILE", str(test_file))

    test_data = {"2026-07-21": {"youtube": 25}}

    time_stats_engine.save_stats(test_data)

    saved_data = json.loads(test_file.read_text(encoding="utf-8"))

    assert saved_data == test_data


def test_record_first_category(monkeypatch):
    stored = {}

    monkeypatch.setattr(time_stats_engine, "load_stats", lambda: {})

    monkeypatch.setattr(
        time_stats_engine, "save_stats", lambda stats: stored.update(stats)
    )

    time_stats_engine.record_time("youtube", 15)

    today = str(time_stats_engine.date.today())

    assert stored[today]["youtube"] == 15


def test_record_time_accumulates(monkeypatch):
    today = str(time_stats_engine.date.today())

    existing_stats = {today: {"youtube": 15}}

    saved = {}

    monkeypatch.setattr(time_stats_engine, "load_stats", lambda: existing_stats)

    monkeypatch.setattr(
        time_stats_engine, "save_stats", lambda stats: saved.update(stats)
    )

    time_stats_engine.record_time("youtube", 10)

    assert saved[today]["youtube"] == 25


def test_different_categories_are_kept_separate(monkeypatch):
    today = str(time_stats_engine.date.today())

    existing_stats = {today: {"youtube": 20}}

    saved = {}

    monkeypatch.setattr(time_stats_engine, "load_stats", lambda: existing_stats)

    monkeypatch.setattr(
        time_stats_engine, "save_stats", lambda stats: saved.update(stats)
    )

    time_stats_engine.record_time("instagram", 12)

    assert saved[today]["youtube"] == 20
    assert saved[today]["instagram"] == 12


def test_existing_previous_days_are_preserved(monkeypatch):
    existing_stats = {"2026-07-20": {"youtube": 50}}

    saved = {}

    monkeypatch.setattr(time_stats_engine, "load_stats", lambda: existing_stats)

    monkeypatch.setattr(
        time_stats_engine, "save_stats", lambda stats: saved.update(stats)
    )

    time_stats_engine.record_time("youtube", 10)

    assert saved["2026-07-20"]["youtube"] == 50


def test_zero_seconds_can_be_recorded(monkeypatch):
    stored = {}

    monkeypatch.setattr(time_stats_engine, "load_stats", lambda: {})

    monkeypatch.setattr(
        time_stats_engine, "save_stats", lambda stats: stored.update(stats)
    )

    time_stats_engine.record_time("youtube", 0)

    today = str(time_stats_engine.date.today())

    assert stored[today]["youtube"] == 0
