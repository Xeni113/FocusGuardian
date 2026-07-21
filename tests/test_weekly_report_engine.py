from src.weekly_report_engine import generate_weekly_report


def test_single_day_report():
    stats = {"2026-07-17": {"youtube": 2, "reddit": 1}}

    report = generate_weekly_report(stats)

    assert report["total"] == 3
    assert report["worst"] == "youtube"
    assert report["categories"] == {"youtube": 2, "reddit": 1}


def test_multiple_days_are_combined():
    stats = {
        "2026-07-16": {"youtube": 2, "reddit": 1},
        "2026-07-17": {"youtube": 1, "instagram": 3},
    }

    report = generate_weekly_report(stats)

    assert report["total"] == 7
    assert report["categories"]["youtube"] == 3
    assert report["categories"]["reddit"] == 1
    assert report["categories"]["instagram"] == 3


def test_worst_category():
    stats = {
        "2026-07-16": {"youtube": 1, "instagram": 2},
        "2026-07-17": {"youtube": 1, "instagram": 3},
    }

    report = generate_weekly_report(stats)

    assert report["worst"] == "instagram"


def test_zero_count_category():
    stats = {"2026-07-17": {"youtube": 0, "reddit": 2}}

    report = generate_weekly_report(stats)

    assert report["total"] == 2
    assert report["worst"] == "reddit"


def test_empty_stats():
    report = generate_weekly_report({})

    assert report["total"] == 0
    assert report["worst"] is None
    assert report["categories"] == {}
