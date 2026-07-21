from src import report_engine


def test_generate_daily_report(monkeypatch):
    fake_stats = {"2026-07-17": {"youtube": 3, "reddit": 1, "instagram": 2}}

    monkeypatch.setattr(report_engine, "load_stats", lambda: fake_stats)

    report = report_engine.generate_daily_report("2026-07-17")

    assert report["date"] == "2026-07-17"
    assert report["total_distractions"] == 6
    assert report["worst_target"] == "youtube"
    assert report["breakdown"] == {"youtube": 3, "reddit": 1, "instagram": 2}


def test_missing_date_returns_none(monkeypatch):
    fake_stats = {"2026-07-17": {"youtube": 2}}

    monkeypatch.setattr(report_engine, "load_stats", lambda: fake_stats)

    report = report_engine.generate_daily_report("2026-07-18")

    assert report is None


def test_load_stats_missing_file(monkeypatch):
    monkeypatch.setattr(report_engine.os.path, "exists", lambda path: False)

    assert report_engine.load_stats() == {}


def test_print_report_none(capsys):
    report_engine.print_report(None)

    captured = capsys.readouterr()

    assert "No data available." in captured.out


def test_print_report_output(capsys):
    report = {
        "date": "2026-07-17",
        "total_distractions": 3,
        "worst_target": "youtube",
        "breakdown": {"youtube": 2, "reddit": 1},
    }

    report_engine.print_report(report)

    captured = capsys.readouterr()

    assert "Report for 2026-07-17" in captured.out
    assert "Total distractions" in captured.out
    assert "youtube" in captured.out
