import time

from collector.process_event_detector import ProcessEventDetector
from collector.process_collector import collect_processes
from collector.system_collector import collect_system
from storage.json_writer import write_snapshot
from config import COLLECTION_INTERVAL


def main():
    print("Linux Black Box started")

    detector = ProcessEventDetector()

    try:
        while True:
            # Collect current system information
            system = collect_system()
            processes = collect_processes()

            # Detect process start and exit events
            started, exited = detector.detect(processes)

            # Display newly started processes
            for process in started:
                print(
                    f"[PROCESS_STARTED] "
                    f"PID={process.pid} "
                    f"PPID={process.ppid} "
                    f"NAME={process.name} "
                    f"COMMAND={process.command}"
                )

            # Display exited processes
            for process in exited:
                print(
                    f"[PROCESS_EXITED] "
                    f"PID={process.pid} "
                    f"NAME={process.name}"
                )

            # Save telemetry snapshot
            write_snapshot(system, processes)

            # Display system summary
            print(
                f"CPU={system.cpu_percent}% | "
                f"RAM={system.memory_percent}% | "
                f"Processes={len(processes)}"
            )

            # Wait before next collection
            time.sleep(COLLECTION_INTERVAL)

    except KeyboardInterrupt:
        print("\nLinux Black Box stopped")


if __name__ == "__main__":
    main()
