from src.streak_engine import calculate_streak


def test_empty_stats():
    assert calculate_streak({}) == 0


def test_single_successful_day():
    stats = {"2026-07-17": {"youtube": 1}}

    assert calculate_streak(stats) == 1


def test_single_failed_day():
    stats = {"2026-07-17": {"youtube": 2}}

    assert calculate_streak(stats) == 0


def test_multiple_successful_days():
    stats = {
        "2026-07-15": {"youtube": 1},
        "2026-07-16": {"reddit": 1},
        "2026-07-17": {"spotify": 2},
    }

    assert calculate_streak(stats) == 3


def test_streak_stops_at_failed_day():
    stats = {
        "2026-07-14": {"youtube": 1},
        "2026-07-15": {"instagram": 2},
        "2026-07-16": {"reddit": 1},
        "2026-07-17": {"spotify": 1},
    }

    assert calculate_streak(stats) == 2


def test_threshold_boundary():
    stats = {"2026-07-17": {"reddit": 2}}

    assert calculate_streak(stats) == 1


def test_below_threshold_boundary():
    stats = {"2026-07-17": {"reddit": 2, "spotify": 1}}

    assert calculate_streak(stats) == 0


def test_dates_are_processed_chronologically():
    stats = {
        "2026-07-17": {"spotify": 1},
        "2026-07-15": {"instagram": 2},
        "2026-07-16": {"youtube": 1},
    }

    assert calculate_streak(stats) == 2
