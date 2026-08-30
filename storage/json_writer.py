import json
from datetime import datetime, timezone

from config import TELEMETRY_FILE


def write_snapshot(system, processes):
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": system.to_dict(),
        "processes": [
            process.to_dict()
            for process in processes
        ],
    }

    with open(TELEMETRY_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(snapshot) + "\n")
