import json

CONFIG_FILE = "config/rules.json"


def load_config():
    """
    Load monitoring rules from the FocusGuardian configuration file.
    """

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()


def is_monitored(info):
    """
    Determine whether the supplied application/window information
    matches one of the configured monitoring rules.

    Missing process names or window titles are treated as empty
    strings instead of causing the monitoring engine to crash.
    """

    if not isinstance(info, dict):
        return False

    process_name = str(info.get("process_name") or "").lower()

    window_title = str(info.get("window_title") or "").lower()

    processes = config.get("processes", [])
    keywords = config.get("keywords", [])

    # --------------------------------------------------------
    # PROCESS RULES
    # --------------------------------------------------------

    for process in processes:
        if process_name == str(process).lower():
            return True

    # --------------------------------------------------------
    # WINDOW-TITLE KEYWORD RULES
    # --------------------------------------------------------

    for keyword in keywords:
        keyword = str(keyword).lower()

        if keyword and keyword in window_title:
            return True

    return False
