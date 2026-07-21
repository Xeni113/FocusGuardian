from src import rule_engine


def test_monitored_process(monkeypatch):
    monkeypatch.setattr(
        rule_engine,
        "config",
        {"processes": ["discord.exe", "spotify.exe"], "keywords": []},
    )

    info = {"process_name": "discord.exe", "window_title": "Discord"}

    assert rule_engine.is_monitored(info) is True


def test_process_matching_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": []}
    )

    info = {"process_name": "DISCORD.EXE", "window_title": "Discord"}

    assert rule_engine.is_monitored(info) is True


def test_monitored_keyword(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": [], "keywords": ["youtube"]}
    )

    info = {"process_name": "msedge.exe", "window_title": "YouTube - Microsoft Edge"}

    assert rule_engine.is_monitored(info) is True


def test_keyword_matching_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": [], "keywords": ["youtube"]}
    )

    info = {"process_name": "msedge.exe", "window_title": "YOUTUBE - MICROSOFT EDGE"}

    assert rule_engine.is_monitored(info) is True


def test_keyword_can_match_inside_long_title(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": [], "keywords": ["reddit"]}
    )

    info = {
        "process_name": "chrome.exe",
        "window_title": "Interesting Discussion - Reddit - Google Chrome",
    }

    assert rule_engine.is_monitored(info) is True


def test_unmonitored_application(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    info = {
        "process_name": "code.exe",
        "window_title": "FocusGuardian - Visual Studio Code",
    }

    assert rule_engine.is_monitored(info) is False


def test_empty_rules_monitor_nothing(monkeypatch):
    monkeypatch.setattr(rule_engine, "config", {"processes": [], "keywords": []})

    info = {"process_name": "discord.exe", "window_title": "YouTube"}

    assert rule_engine.is_monitored(info) is False


def test_process_rule_has_priority_over_missing_keyword(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["spotify.exe"], "keywords": ["youtube"]}
    )

    info = {"process_name": "spotify.exe", "window_title": "My Playlist"}

    assert rule_engine.is_monitored(info) is True


def test_missing_process_name(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    info = {"window_title": "YouTube - Microsoft Edge"}

    assert rule_engine.is_monitored(info) is True


def test_missing_window_title(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    info = {"process_name": "discord.exe"}

    assert rule_engine.is_monitored(info) is True


def test_empty_info(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    assert rule_engine.is_monitored({}) is False


def test_none_info(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    assert rule_engine.is_monitored(None) is False


def test_none_field_values(monkeypatch):
    monkeypatch.setattr(
        rule_engine, "config", {"processes": ["discord.exe"], "keywords": ["youtube"]}
    )

    info = {"process_name": None, "window_title": None}

    assert rule_engine.is_monitored(info) is False


def test_missing_config_sections(monkeypatch):
    monkeypatch.setattr(rule_engine, "config", {})

    info = {"process_name": "discord.exe", "window_title": "YouTube"}

    assert rule_engine.is_monitored(info) is False
