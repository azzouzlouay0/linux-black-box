import time

from collector.process_event_detector import ProcessEventDetector
from collector.process_collector import collect_processes
from collector.system_collector import collect_system

from storage.json_writer import write_snapshot
from storage.event_writer import write_process_event

from config import COLLECTION_INTERVAL


def main():
    print("Linux Black Box started")

    detector = ProcessEventDetector()

    try:
        while True:
            # Collect current system information
            system = collect_system()
            processes = collect_processes()

            # Detect started and exited processes
            started, exited = detector.detect(processes)

            # New processes
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
                    process
                )

            # Exited processes
            for process in exited:
                print(
                    f"[PROCESS_EXITED] "
                    f"PID={process.pid} "
                    f"NAME={process.name}"
                )

                write_process_event(
                    "PROCESS_EXITED",
                    process
                )

            # Save full system snapshot
            write_snapshot(system, processes)

            print(
                f"CPU={system.cpu_percent}% | "
                f"RAM={system.memory_percent}% | "
                f"Processes={len(processes)}"
            )

            time.sleep(COLLECTION_INTERVAL)

    except KeyboardInterrupt:
        print("\nLinux Black Box stopped")


if __name__ == "__main__":
    main()
