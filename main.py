from src.stats_engine import (
    record_distraction,
    get_category,
    get_today_stats,
)
from src.adaptive_engine import calculate_reminder_delay
from src.time_stats_engine import record_time
from src.overlay_engine import show_reminder
from src.detector import get_active_window_info
from src.rule_engine import is_monitored
from src.timer_engine import TimerEngine
from src.session_engine import SessionEngine

import time

# ============================================================
# FOCUSGUARDIAN
# Core Monitoring Engine
# ============================================================

POLL_INTERVAL = 0.5
DEFAULT_REMINDER_DELAY = 60


# Categories that are considered genuine distractions.
#
# Only these categories:
#   1. increase the distraction counter,
#   2. reduce the Focus Score,
#   3. create distraction sessions,
#   4. trigger reminder overlays.
DISTRACTING_CATEGORIES = {
    "youtube",
    "reddit",
    "instagram",
}


# ============================================================
# ENGINE INITIALIZATION
# ============================================================

timer = TimerEngine(reminder_delay=DEFAULT_REMINDER_DELAY)

session = SessionEngine()


# ============================================================
# RUNTIME STATE
# ============================================================

# Used to detect meaningful monitored-target transitions.
previous_target = None
previous_category = None

# Used only for terminal/debug logging of window changes.
previous_pid = None
previous_title = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def build_target(info, category):
    """
    Creates a stable identity for the current monitored target.

    The process name + category combination prevents every
    polling cycle or browser-title change from being counted
    as a completely new distraction.
    """

    return (
        info.get("process_name", "").lower(),
        category,
    )


def calculate_total_distractions(today_stats):
    """
    Calculates the total number of genuine distracting events
    recorded today.

    Unknown, neutral and productive categories are ignored.
    """

    return sum(today_stats.get(category, 0) for category in DISTRACTING_CATEGORIES)


def calculate_focus_score(total_distractions):
    """
    Calculates the current Focus Score.

    Each genuine distraction removes 5 points.

    Minimum score = 0
    Maximum score = 100
    """

    return max(
        100 - total_distractions * 5,
        0,
    )


def print_focus_event(
    info,
    category,
    total_distractions,
    focus_score,
    reminder_delay,
):
    """
    Prints a structured FocusGuardian event.
    """

    print("\n" + "=" * 55)
    print("FOCUSGUARDIAN EVENT")
    print("=" * 55)

    print(f"Application  : " f"{info.get('process_name', 'Unknown')}")

    print(f"Window       : " f"{info.get('window_title', 'Unknown')}")

    print(f"Category     : {category}")
    print(f"Distractions : {total_distractions}")
    print(f"Focus Score  : {focus_score}")
    print(f"Reminder     : {reminder_delay}s")

    print("=" * 55)


def print_window_change(info):
    """
    Prints active-window changes for debugging.

    This does NOT mean that every printed window is considered
    a distraction.
    """

    print("\n" + "-" * 50)

    print(f"Time        : " f"{info.get('time', 'Unknown')}")

    print(f"Application : " f"{info.get('process_name', 'Unknown')}")

    print(f"PID         : " f"{info.get('pid', 'Unknown')}")

    print(f"Window      : " f"{info.get('window_title', 'Unknown')}")

    print("-" * 50)


def save_finished_session(finished_session, final=False):
    """
    Saves a completed distraction session.

    Returns immediately if no session was active.
    """

    if not finished_session:
        return

    record_time(
        finished_session["target"],
        finished_session["duration"],
    )

    if final:

        print(
            "Final session saved:"
            f" {finished_session['target']}"
            f" ({finished_session['duration']} seconds)"
        )

    else:

        print(
            "\nFinished session:"
            f"\nTarget   : {finished_session['target']}"
            f"\nDuration : {finished_session['duration']} seconds"
        )


# ============================================================
# MAIN MONITORING LOOP
# ============================================================

print("\nFocusGuardian Core Engine Started")
print("Monitoring active windows...")
print("Press Ctrl+C to stop.\n")


try:

    while True:

        # ----------------------------------------------------
        # 1. DETECT ACTIVE WINDOW
        # ----------------------------------------------------

        info = get_active_window_info()

        if not info:

            time.sleep(POLL_INTERVAL)
            continue

        # ----------------------------------------------------
        # 2. WINDOW CHANGE LOGGING
        # ----------------------------------------------------

        current_pid = info.get("pid")
        current_title = info.get("window_title")

        if current_pid != previous_pid or current_title != previous_title:

            print_window_change(info)

            previous_pid = current_pid
            previous_title = current_title

        # ----------------------------------------------------
        # 3. CHECK WHETHER TARGET IS MONITORED
        # ----------------------------------------------------

        if not is_monitored(info):

            # The user has left a monitored target.
            #
            # Any currently running distraction session must
            # therefore end immediately.

            finished_session = session.switch_target(None)

            save_finished_session(finished_session)

            # Reset the reminder because the user is no longer
            # on a monitored target.

            timer.reset()

            # Reset transition state so that returning to a
            # distraction later counts as a new transition.

            previous_target = None
            previous_category = None

            time.sleep(POLL_INTERVAL)
            continue

        # ----------------------------------------------------
        # 4. CLASSIFY CURRENT TARGET
        # ----------------------------------------------------

        category = get_category(info)

        current_target = build_target(
            info,
            category,
        )

        # ----------------------------------------------------
        # 5. DETECT TARGET / CATEGORY TRANSITION
        # ----------------------------------------------------

        target_changed = current_target != previous_target

        category_changed = category != previous_category

        if target_changed:

            # ------------------------------------------------
            # 5A. SESSION TRACKING
            # ------------------------------------------------
            #
            # Only genuine distractions receive sessions.
            #
            # Example:
            #
            # youtube -> tracked
            # reddit -> tracked
            # instagram -> tracked
            # unknown_browser -> NOT tracked
            #

            if category in DISTRACTING_CATEGORIES:

                session_target = category

            else:

                session_target = None

            finished_session = session.switch_target(session_target)

            save_finished_session(finished_session)

            # ------------------------------------------------
            # 5B. RECORD NEW DISTRACTION EVENT
            # ------------------------------------------------

            if category_changed and category in DISTRACTING_CATEGORIES:

                today_stats = record_distraction(info)

                print(f"\nRecorded new distraction: " f"{category}")

            else:

                today_stats = get_today_stats()

                if category not in DISTRACTING_CATEGORIES:

                    print(f"\nNon-distracting category ignored: " f"{category}")

                else:

                    print("\nSame category detected - " "event counter NOT increased.")

            # ------------------------------------------------
            # 5C. CALCULATE DISTRACTION COUNT
            # ------------------------------------------------

            total_distractions = calculate_total_distractions(today_stats)

            # ------------------------------------------------
            # 5D. CALCULATE FOCUS SCORE
            # ------------------------------------------------

            focus_score = calculate_focus_score(total_distractions)

            # ------------------------------------------------
            # 5E. ADAPT REMINDER FREQUENCY
            # ------------------------------------------------

            new_delay = calculate_reminder_delay(
                total_distractions,
                focus_score,
            )

            timer.reminder_delay = new_delay

            # ------------------------------------------------
            # 5F. PRINT EVENT
            # ------------------------------------------------

            print_focus_event(
                info,
                category,
                total_distractions,
                focus_score,
                new_delay,
            )

            # ------------------------------------------------
            # 5G. UPDATE TRANSITION STATE
            # ------------------------------------------------

            previous_target = current_target
            previous_category = category

            # Every genuine target transition starts with a
            # fresh reminder countdown.

            timer.reset()

        # ----------------------------------------------------
        # 6. BUILD REMINDER TARGET DESCRIPTION
        # ----------------------------------------------------

        target_description = (
            f"{info.get('process_name', 'Unknown')}:\n"
            f"{info.get('window_title', 'Unknown')}"
        )

        # ----------------------------------------------------
        # 7. REMINDER TIMER
        # ----------------------------------------------------
        #
        # Reminder overlays are allowed ONLY for genuine
        # distracting categories.
        #

        if category in DISTRACTING_CATEGORIES:

            if timer.update(target_description):

                show_reminder(
                    "You have been distracted by:\n\n"
                    f"{target_description}\n\n"
                    "Return to your task."
                )

                # IMPORTANT:
                #
                # Do NOT record another distraction here.
                #
                # The distraction was already recorded when
                # the user entered the distracting category.
                #
                # Otherwise repeated reminders would falsely
                # increase the distraction counter.

                timer.reset()

        else:

            # Unknown/neutral targets must never accumulate
            # time toward a distraction reminder.

            timer.reset()

        # ----------------------------------------------------
        # 8. POLLING DELAY
        # ----------------------------------------------------

        time.sleep(POLL_INTERVAL)


# ============================================================
# SAFE SHUTDOWN
# ============================================================

except KeyboardInterrupt:

    print("\n\nFocusGuardian monitoring stopped.")

    # Save any currently active genuine distraction session
    # before shutting down.

    try:

        finished_session = session.switch_target(None)

        save_finished_session(
            finished_session,
            final=True,
        )

    except Exception as shutdown_error:

        print("Could not save final session:" f" {shutdown_error}")

    print("FocusGuardian Core Engine Closed.")
