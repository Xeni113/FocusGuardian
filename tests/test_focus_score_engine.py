from src.focus_score_engine import calculate_focus_score


def test_no_distractions():
    assert calculate_focus_score({}) == 100


def test_single_youtube_distraction():
    assert calculate_focus_score({"youtube": 1}) == 80


def test_multiple_known_distractions():
    stats = {"youtube": 1, "instagram": 1, "spotify": 1}

    assert calculate_focus_score(stats) == 50


def test_multiple_counts():
    stats = {"youtube": 2, "reddit": 1}

    assert calculate_focus_score(stats) == 45


def test_unknown_category_uses_default_penalty():
    assert calculate_focus_score({"unknown_app": 2}) == 90


def test_score_cannot_go_below_zero():
    assert calculate_focus_score({"instagram": 10}) == 0


def test_browser_penalty():
    stats = {"chrome.exe": 1, "msedge.exe": 1}

    assert calculate_focus_score(stats) == 90
