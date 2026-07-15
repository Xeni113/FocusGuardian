from src.overlay_engine import show_reminder

import time

from src.detector import get_active_window_info
from src.rule_engine import is_monitored
from src.timer_engine import TimerEngine

previous_pid = None
previous_title = None

timer = TimerEngine()

while True:
    info = get_active_window_info()

    if info:

        # Check if distraction app/site detected
        if is_monitored(info):

            target = (
                f'{info["process_name"]}:'
                f'{info["window_title"]}'
            )

            if timer.update(target):
                show_reminder(
    f"You have been distracted by:\n\n{target}\n\nReturn to your task."
)

        else:
            timer.reset()

        # Print window changes
        if (
            info["pid"] != previous_pid or
            info["window_title"] != previous_title
        ):
            print("\n" + "=" * 50)
            print(f'Time        : {info["time"]}')
            print(f'Application : {info["process_name"]}')
            print(f'PID         : {info["pid"]}')
            print(f'Window      : {info["window_title"]}')
            print("=" * 50)

            previous_pid = info["pid"]
            previous_title = info["window_title"]

    time.sleep(0.5)