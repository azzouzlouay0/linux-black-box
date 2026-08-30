from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Alert:
    alert_id: str
    timestamp: str
    type: str
    severity: str
    message: str
    evidence: dict[str, Any]

    def to_dict(self):
        return asdict(self)
