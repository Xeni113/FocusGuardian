import json

from src import stats_engine

# ============================================================
# FILE MANAGEMENT TESTS
# ============================================================


def test_load_stats_missing_file(tmp_path, monkeypatch):
    test_file = tmp_path / "stats.json"

    monkeypatch.setattr(stats_engine, "DATA_DIR", str(tmp_path))

    monkeypatch.setattr(stats_engine, "STATS_FILE", str(test_file))

    result = stats_engine.load_stats()

    assert result == {}


def test_load_stats_existing_file(tmp_path, monkeypatch):
    test_file = tmp_path / "stats.json"

    test_data = {"2026-07-21": {"youtube": 3}}

    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    monkeypatch.setattr(stats_engine, "DATA_DIR", str(tmp_path))

    monkeypatch.setattr(stats_engine, "STATS_FILE", str(test_file))

    result = stats_engine.load_stats()

    assert result == test_data


def test_load_stats_corrupted_json(tmp_path, monkeypatch):
    test_file = tmp_path / "stats.json"

    test_file.write_text("{ this is invalid json", encoding="utf-8")

    monkeypatch.setattr(stats_engine, "DATA_DIR", str(tmp_path))

    monkeypatch.setattr(stats_engine, "STATS_FILE", str(test_file))

    result = stats_engine.load_stats()

    assert result == {}


def test_save_stats(tmp_path, monkeypatch):
    test_file = tmp_path / "stats.json"

    monkeypatch.setattr(stats_engine, "DATA_DIR", str(tmp_path))

    monkeypatch.setattr(stats_engine, "STATS_FILE", str(test_file))

    test_data = {"2026-07-21": {"youtube": 4, "reddit": 2}}

    stats_engine.save_stats(test_data)

    saved_data = json.loads(test_file.read_text(encoding="utf-8"))

    assert saved_data == test_data


# ============================================================
# TARGET CLASSIFICATION TESTS
# ============================================================


def test_categorize_youtube():
    info = {"process_name": "msedge.exe", "window_title": "YouTube - Microsoft Edge"}

    assert stats_engine.categorize_target(info) == "youtube"


def test_categorize_reddit():
    info = {"process_name": "chrome.exe", "window_title": "Reddit - Google Chrome"}

    assert stats_engine.categorize_target(info) == "reddit"


def test_categorize_instagram():
    info = {"process_name": "msedge.exe", "window_title": "Instagram - Microsoft Edge"}

    assert stats_engine.categorize_target(info) == "instagram"


def test_categorize_spotify_by_title():
    info = {"process_name": "msedge.exe", "window_title": "Spotify - Microsoft Edge"}

    assert stats_engine.categorize_target(info) == "spotify"


def test_categorize_spotify_by_process():
    info = {"process_name": "Spotify.exe", "window_title": "Music"}

    assert stats_engine.categorize_target(info) == "spotify"


def test_productive_site_has_priority():
    info = {"process_name": "msedge.exe", "window_title": "ChatGPT - Microsoft Edge"}

    assert stats_engine.categorize_target(info) == "productive"


def test_github_is_productive():
    info = {"process_name": "chrome.exe", "window_title": "FocusGuardian · GitHub"}

    assert stats_engine.categorize_target(info) == "productive"


def test_physics_wallah_is_productive():
    info = {
        "process_name": "msedge.exe",
        "window_title": "Physics Wallah - Microsoft Edge",
    }

    assert stats_engine.categorize_target(info) == "productive"


def test_unknown_browser():
    info = {"process_name": "msedge.exe", "window_title": "Some Random Website"}

    assert stats_engine.categorize_target(info) == "unknown_browser"


def test_other_application_uses_process_name():
    info = {"process_name": "notepad.exe", "window_title": "Untitled - Notepad"}

    assert stats_engine.categorize_target(info) == "notepad.exe"


def test_missing_process_and_title_returns_unknown():
    assert stats_engine.categorize_target({}) == "unknown"


def test_classification_is_case_insensitive():
    info = {"process_name": "MSEDGE.EXE", "window_title": "YOUTUBE - MICROSOFT EDGE"}

    assert stats_engine.categorize_target(info) == "youtube"


def test_get_category_uses_categorization():
    info = {"process_name": "chrome.exe", "window_title": "Reddit"}

    assert stats_engine.get_category(info) == "reddit"


# ============================================================
# RECORDING TESTS
# ============================================================


def test_record_first_distraction(monkeypatch):
    saved = {}

    monkeypatch.setattr(stats_engine, "load_stats", lambda: {})

    monkeypatch.setattr(stats_engine, "save_stats", lambda stats: saved.update(stats))

    info = {"process_name": "msedge.exe", "window_title": "YouTube"}

    result = stats_engine.record_distraction(info)

    today = str(stats_engine.date.today())

    assert result["youtube"] == 1
    assert saved[today]["youtube"] == 1


def test_record_repeated_distraction(monkeypatch):
    today = str(stats_engine.date.today())

    existing = {today: {"youtube": 2}}

    saved = {}

    monkeypatch.setattr(stats_engine, "load_stats", lambda: existing)

    monkeypatch.setattr(stats_engine, "save_stats", lambda stats: saved.update(stats))

    info = {"process_name": "msedge.exe", "window_title": "YouTube"}

    result = stats_engine.record_distraction(info)

    assert result["youtube"] == 3
    assert saved[today]["youtube"] == 3


def test_record_different_categories(monkeypatch):
    today = str(stats_engine.date.today())

    existing = {today: {"youtube": 2}}

    saved = {}

    monkeypatch.setattr(stats_engine, "load_stats", lambda: existing)

    monkeypatch.setattr(stats_engine, "save_stats", lambda stats: saved.update(stats))

    info = {"process_name": "chrome.exe", "window_title": "Reddit"}

    result = stats_engine.record_distraction(info)

    assert result["youtube"] == 2
    assert result["reddit"] == 1


def test_previous_days_are_preserved(monkeypatch):
    existing = {"2026-07-20": {"youtube": 5}}

    saved = {}

    monkeypatch.setattr(stats_engine, "load_stats", lambda: existing)

    monkeypatch.setattr(stats_engine, "save_stats", lambda stats: saved.update(stats))

    info = {"process_name": "msedge.exe", "window_title": "YouTube"}

    stats_engine.record_distraction(info)

    assert saved["2026-07-20"]["youtube"] == 5


# ============================================================
# TODAY STATISTICS TESTS
# ============================================================


def test_get_today_stats(monkeypatch):
    today = str(stats_engine.date.today())

    monkeypatch.setattr(
        stats_engine, "load_stats", lambda: {today: {"youtube": 3, "reddit": 2}}
    )

    result = stats_engine.get_today_stats()

    assert result == {"youtube": 3, "reddit": 2}


def test_get_today_stats_when_empty(monkeypatch):
    monkeypatch.setattr(stats_engine, "load_stats", lambda: {})

    assert stats_engine.get_today_stats() == {}


def test_total_events_today(monkeypatch):
    monkeypatch.setattr(
        stats_engine,
        "get_today_stats",
        lambda: {"youtube": 3, "reddit": 2, "instagram": 1},
    )

    assert stats_engine.get_total_events_today() == 6


def test_total_events_today_when_empty(monkeypatch):
    monkeypatch.setattr(stats_engine, "get_today_stats", lambda: {})

    assert stats_engine.get_total_events_today() == 0
