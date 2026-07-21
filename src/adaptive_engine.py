def calculate_reminder_delay(distractions, focus_score):
    """
    Returns adaptive reminder delay in seconds.
    """

    # Severe focus loss
    if focus_score < 50:
        return 5

    # Distraction escalation
    if distractions <= 1:
        return 60

    elif distractions <= 2:
        return 45

    elif distractions <= 3:
        return 30

    elif distractions <= 5:
        return 20

    else:
        return 10