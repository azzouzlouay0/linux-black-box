COLLECTION_INTERVAL = 5

TELEMETRY_FILE = "telemetry.jsonl"
EVENTS_FILE = "events.jsonl"
ALERTS_FILE = "alerts.jsonl"

CPU_HIGH_THRESHOLD = 90.0
MEMORY_HIGH_THRESHOLD = 90.0

# Alert only after several consecutive high measurements
SUSTAINED_SAMPLES = 3

# Detect a sudden increase in number of processes
PROCESS_GROWTH_THRESHOLD = 20
