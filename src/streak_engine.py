from src.focus_score_engine import calculate_focus_score

STREAK_THRESHOLD = 70


def calculate_streak(stats):
    dates = sorted(stats.keys())

    streak = 0

    for day in reversed(dates):
        score = calculate_focus_score(stats[day])

        if score >= STREAK_THRESHOLD:
            streak += 1
        else:
            break

    return streak
