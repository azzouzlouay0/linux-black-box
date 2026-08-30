from datetime import datetime, timezone
from uuid import uuid4

from config import (
    CPU_HIGH_THRESHOLD,
    MEMORY_HIGH_THRESHOLD,
    PROCESS_GROWTH_THRESHOLD,
    SUSTAINED_SAMPLES,
)

from detection.models import Alert


class RuleEngine:
    def __init__(self):
        self.cpu_high_count = 0
        self.memory_high_count = 0

        self.cpu_alert_active = False
        self.memory_alert_active = False

        self.previous_process_count = None

        self.reported_zombies = set()

    def evaluate(self, system, processes):
        alerts = []

        alerts.extend(self._check_cpu(system))
        alerts.extend(self._check_memory(system))
        alerts.extend(self._check_zombies(processes))
        alerts.extend(self._check_process_growth(processes))

        return alerts

    def _create_alert(
        self,
        alert_type,
        severity,
        message,
        evidence,
    ):
        return Alert(
            alert_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            type=alert_type,
            severity=severity,
            message=message,
            evidence=evidence,
        )

    def _check_cpu(self, system):
        alerts = []

        if system.cpu_percent >= CPU_HIGH_THRESHOLD:
            self.cpu_high_count += 1
        else:
            self.cpu_high_count = 0
            self.cpu_alert_active = False

        if (
            self.cpu_high_count >= SUSTAINED_SAMPLES
            and not self.cpu_alert_active
        ):
            severity = (
                "CRITICAL"
                if system.cpu_percent >= 97
                else "HIGH"
            )

            alerts.append(
                self._create_alert(
                    alert_type="HIGH_CPU",
                    severity=severity,
                    message="CPU usage remained above the configured threshold.",
                    evidence={
                        "cpu_percent": system.cpu_percent,
                        "threshold": CPU_HIGH_THRESHOLD,
                        "consecutive_samples": self.cpu_high_count,
                    },
                )
            )

            self.cpu_alert_active = True

        return alerts

    def _check_memory(self, system):
        alerts = []

        if system.memory_percent >= MEMORY_HIGH_THRESHOLD:
            self.memory_high_count += 1
        else:
            self.memory_high_count = 0
            self.memory_alert_active = False

        if (
            self.memory_high_count >= SUSTAINED_SAMPLES
            and not self.memory_alert_active
        ):
            severity = (
                "CRITICAL"
                if system.memory_percent >= 95
                else "HIGH"
            )

            alerts.append(
                self._create_alert(
                    alert_type="HIGH_MEMORY",
                    severity=severity,
                    message="Memory usage remained above the configured threshold.",
                    evidence={
                        "memory_percent": system.memory_percent,
                        "threshold": MEMORY_HIGH_THRESHOLD,
                        "consecutive_samples": self.memory_high_count,
                    },
                )
            )

            self.memory_alert_active = True

        return alerts

    def _check_zombies(self, processes):
        alerts = []

        current_zombies = set()

        for process in processes:
            if process.status.lower() != "zombie":
                continue

            process_key = (
                process.pid,
                process.create_time,
            )

            current_zombies.add(process_key)

            if process_key in self.reported_zombies:
                continue

            alerts.append(
                self._create_alert(
                    alert_type="ZOMBIE_PROCESS",
                    severity="MEDIUM",
                    message="A zombie process was detected.",
                    evidence={
                        "pid": process.pid,
                        "ppid": process.ppid,
                        "name": process.name,
                        "username": process.username,
                    },
                )
            )

        self.reported_zombies = current_zombies

        return alerts

    def _check_process_growth(self, processes):
        alerts = []

        current_count = len(processes)

        if self.previous_process_count is None:
            self.previous_process_count = current_count
            return alerts

        growth = current_count - self.previous_process_count

        if growth >= PROCESS_GROWTH_THRESHOLD:
            alerts.append(
                self._create_alert(
                    alert_type="RAPID_PROCESS_CREATION",
                    severity="HIGH",
                    message="The number of running processes increased rapidly.",
                    evidence={
                        "previous_process_count": self.previous_process_count,
                        "current_process_count": current_count,
                        "increase": growth,
                        "threshold": PROCESS_GROWTH_THRESHOLD,
                    },
                )
            )

        self.previous_process_count = current_count

        return alerts
