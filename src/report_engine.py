import json
import os

STATS_FILE = "data/stats.json"


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}

    with open(STATS_FILE, "r") as file:
        return json.load(file)


def generate_daily_report(date):
    stats = load_stats()

    if date not in stats:
        return None

    day_data = stats[date]

    total_distractions = sum(day_data.values())

    worst_target = max(
        day_data,
        key=day_data.get
    )

    report = {
        "date": date,
        "total_distractions": total_distractions,
        "worst_target": worst_target,
        "breakdown": day_data
    }

    return report


def print_report(report):

    if report is None:
        print("No data available.")
        return

    print("\n" + "=" * 50)
    print(f"Report for {report['date']}")
    print("=" * 50)

    print(
        f"Total distractions : "
        f"{report['total_distractions']}"
    )

    print(
        f"Worst distraction  : "
        f"{report['worst_target']}"
    )

    print("\nBreakdown:")

    for target, count in report["breakdown"].items():
        print(f"  {target:<15} {count}")

    print("=" * 50)