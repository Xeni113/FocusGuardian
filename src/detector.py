import win32gui
import win32process
import psutil
from datetime import datetime


def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        process = psutil.Process(pid)

        process_name = process.name()
        window_title = win32gui.GetWindowText(hwnd)

        current_time = datetime.now().strftime("%H:%M:%S")

        return {
            "time": current_time,
            "process_name": process_name,
            "pid": pid,
            "window_title": window_title
        }

    except Exception:
        return None