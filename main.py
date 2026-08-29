import time

from collector.process_collector import collect_processes
from collector.system_collector import collect_system
from storage.json_writer import write_snapshot


from config import COLLECTION_INTERVAL


def main():
    print("Linux Black Box started")

    try:
        while True:
            system = collect_system()
            processes = collect_processes()

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
