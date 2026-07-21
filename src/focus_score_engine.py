DISTRACTION_WEIGHTS = {
    "youtube": 20,
    "reddit": 15,
    "instagram": 25,
    "lyrics": 10,
    "spotify": 5,
    "facebook": 20,
    "twitter": 15,
    "chrome.exe": 5,
    "msedge.exe": 5
}


def calculate_focus_score(day_stats):
    score = 100

    for category, count in day_stats.items():
        penalty = DISTRACTION_WEIGHTS.get(category, 5)
        score -= penalty * count

    if score < 0:
        score = 0

    return score