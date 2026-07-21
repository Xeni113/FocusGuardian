import json
import os
from datetime import date


DATA_DIR = "data"
STATS_FILE = os.path.join(DATA_DIR, "stats.json")


# ============================================================
# FILE MANAGEMENT
# ============================================================

def ensure_data_directory():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_stats():
    ensure_data_directory()

    if not os.path.exists(STATS_FILE):
        return {}

    try:
        with open(STATS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        # Prevent FocusGuardian from crashing because of damaged stats.
        return {}


def save_stats(stats):
    ensure_data_directory()

    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)


# ============================================================
# TARGET CLASSIFICATION
# ============================================================

def categorize_target(info):

    process_name = info.get("process_name", "").lower()
    title = info.get("window_title", "").lower()

    # --------------------------------------------------------
    # PRODUCTIVE / STUDY WEBSITES
    # --------------------------------------------------------

    productive_keywords = [
        "physics wallah",
        "pw.live",
        "chatgpt",
        "github",
        "stackoverflow",
        "visual studio code",
        "leetcode",
        "geeksforgeeks",
        "wikipedia",
        "google docs",
        "google drive",
    ]

    for keyword in productive_keywords:
        if keyword in title:
            return "productive"


    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    if "youtube" in title:
        return "youtube"


    # --------------------------------------------------------
    # REDDIT
    # --------------------------------------------------------

    if "reddit" in title:
        return "reddit"


    # --------------------------------------------------------
    # INSTAGRAM
    # --------------------------------------------------------

    if "instagram" in title:
        return "instagram"


    # --------------------------------------------------------
    # SPOTIFY
    # --------------------------------------------------------

    if "spotify" in title or "spotify" in process_name:
        return "spotify"


    # --------------------------------------------------------
    # BROWSER DETECTION
    # --------------------------------------------------------

    browser_processes = [
        "chrome.exe",
        "msedge.exe",
        "firefox.exe",
        "brave.exe",
    ]

    if process_name in browser_processes:
        return "unknown_browser"


    # --------------------------------------------------------
    # OTHER APPLICATIONS
    # --------------------------------------------------------

    return process_name if process_name else "unknown"


# ============================================================
# PUBLIC CATEGORY FUNCTION
# ============================================================

def get_category(info):
    return categorize_target(info)


# ============================================================
# RECORD ONE EVENT
# ============================================================

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

    return stats[today]


# ============================================================
# GET TODAY'S STATISTICS
# ============================================================

def get_today_stats():

    stats = load_stats()

    today = str(date.today())

    return stats.get(today, {})


# ============================================================
# TOTAL EVENTS TODAY
# ============================================================

def get_total_events_today():

    today_stats = get_today_stats()

    return sum(today_stats.values())