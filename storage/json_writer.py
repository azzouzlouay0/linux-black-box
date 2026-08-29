import json
from datetime import datetime, timezone


OUTPUT_FILE = "telemetry.jsonl"


def write_snapshot(system, processes):
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": system.to_dict(),
        "processes": [p.to_dict() for p in processes],
    }

    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(snapshot) + "\n")
