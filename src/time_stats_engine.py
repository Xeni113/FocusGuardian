import json
import os
from datetime import date

STATS_FILE = "data/time_stats.json"


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}

    with open(STATS_FILE, "r") as file:
        return json.load(file)


def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)


def record_time(category, seconds):
    stats = load_stats()

    today = str(date.today())

    if today not in stats:
        stats[today] = {}

    if category not in stats[today]:
        stats[today][category] = 0

    stats[today][category] += seconds

    save_stats(stats)