from datetime import date
import json
import os


STATS_FILE = "data/stats.json"


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}

    with open(STATS_FILE, "r") as file:
        return json.load(file)


def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)


def categorize_target(info):
    title = info["window_title"].lower()

    if "youtube" in title:
        return "youtube"

    if "reddit" in title:
        return "reddit"

    if "instagram" in title:
        return "instagram"

    if "lyrics" in title:
        return "lyrics"

    if "spotify" in title:
        return "spotify"

    return info["process_name"].lower()

def record_distraction(info):
    stats = load_stats()

    today = str(date.today())

    if today not in stats:
        stats[today] = {}

    category = categorize_target(info)

    if category not in stats[today]:
        stats[today][category] = 0

    stats[today][category] += 1

    save_stats(stats)