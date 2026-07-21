def generate_weekly_report(stats):
    total_distractions = 0
    category_totals = {}

    for day in stats:
        for category, count in stats[day].items():
            total_distractions += count

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += count

    if category_totals:
        worst = max(category_totals, key=category_totals.get)
    else:
        worst = None

    return {"total": total_distractions, "worst": worst, "categories": category_totals}
