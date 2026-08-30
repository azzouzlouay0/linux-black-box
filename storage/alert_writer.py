import json

from config import ALERTS_FILE


def write_alert(alert):
    with open(ALERTS_FILE, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(alert.to_dict()) + "\n"
        )
