import time

from collector.process_event_detector import ProcessEventDetector
from collector.process_collector import collect_processes
from collector.system_collector import collect_system
from collector.ebpf_process_collector import EbpfProcessCollector

from detection.rule_engine import RuleEngine

from storage.json_writer import write_snapshot
from storage.event_writer import write_process_event
from storage.alert_writer import write_alert

from config import COLLECTION_INTERVAL


def main():
    print("Linux Black Box started")

    detector = ProcessEventDetector()
    ebpf_collector = EbpfProcessCollector()
    rule_engine = RuleEngine()

    print("Starting eBPF process collector...")
    ebpf_collector.start()

    try:
        while True:
            # --------------------------------
            # 1. COLLECT
            # --------------------------------

            system = collect_system()
            processes = collect_processes()

            # --------------------------------
            # 2. PROCESS LIFECYCLE
            # --------------------------------

            started, exited = detector.detect(processes)

            for process in started:
                print(
                    f"[PROCESS_STARTED] "
                    f"PID={process.pid} "
                    f"PPID={process.ppid} "
                    f"NAME={process.name} "
                    f"COMMAND={process.command}"
                )

                write_process_event(
                    "PROCESS_STARTED",
                    process,
                )

            for process in exited:
                print(
                    f"[PROCESS_EXITED] "
                    f"PID={process.pid} "
                    f"NAME={process.name}"
                )

                write_process_event(
                    "PROCESS_EXITED",
                    process,
                )

            # --------------------------------
            # 3. SAVE TELEMETRY
            # --------------------------------

            write_snapshot(
                system,
                processes,
            )

            # --------------------------------
            # 4. DETECTION ENGINE
            # --------------------------------

            alerts = rule_engine.evaluate(
                system,
                processes,
            )

            for alert in alerts:
                print(
                    f"[ALERT] "
                    f"TYPE={alert.type} "
                    f"SEVERITY={alert.severity} "
                    f"MESSAGE={alert.message}"
                )

                write_alert(alert)

            # --------------------------------
            # 5. SUMMARY
            # --------------------------------

            print(
                f"CPU={system.cpu_percent}% | "
                f"RAM={system.memory_percent}% | "
                f"Processes={len(processes)} | "
                f"Alerts={len(alerts)}"
            )

            time.sleep(
                COLLECTION_INTERVAL
            )

    except KeyboardInterrupt:
        print(
            "\nStopping Linux Black Box..."
        )

    finally:
        ebpf_collector.stop()

        print(
            "Linux Black Box stopped"
        )


if __name__ == "__main__":
    main()
