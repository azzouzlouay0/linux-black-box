import json
from datetime import datetime, timezone

from config import EVENTS_FILE


def write_process_event(event_type, process):
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "pid": process.pid,
        "ppid": process.ppid,
        "username": process.username,
        "name": process.name,
        "command": process.command,
    }

    with open(EVENTS_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")
