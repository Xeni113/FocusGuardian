import json


def load_rules():
    with open("config/rules.json", "r") as file:
        return json.load(file)