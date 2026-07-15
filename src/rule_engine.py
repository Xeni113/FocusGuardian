import json


def load_config():
    with open("config/rules.json", "r") as file:
        return json.load(file)


config = load_config()


def is_monitored(info):
    process_name = info["process_name"].lower()
    window_title = info["window_title"].lower()

    # Process rules
    for process in config["processes"]:
        if process_name == process.lower():
            return True

    # Keyword rules
    for keyword in config["keywords"]:
        if keyword.lower() in window_title:
            return True

    return False