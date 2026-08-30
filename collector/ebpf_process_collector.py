import subprocess
import threading
from datetime import datetime, timezone

from storage.event_writer import write_ebpf_event


class EbpfProcessCollector:
    """
    Collects process execution and exit events directly
    from the Linux kernel using bpftrace/eBPF.
    """

    def __init__(self):
        self.process = None
        self.thread = None
        self.running = False

    def start(self):
        program = r'''
tracepoint:syscalls:sys_enter_execve
{
    printf("EXEC|%d|%s\n", pid, str(args->filename));
}

tracepoint:sched:sched_process_exit
{
    printf("EXIT|%d|%s\n", pid, comm);
}
'''

        command = [
            "sudo",
            "bpftrace",
            "-q",
            "-e",
            program,
        ]

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        self.running = True

        self.thread = threading.Thread(
            target=self._read_events,
            daemon=True,
        )

        self.thread.start()

    def _read_events(self):
        if self.process is None or self.process.stdout is None:
            return

        for line in self.process.stdout:
            if not self.running:
                break

            line = line.strip()

            if not line:
                continue

            event = self._parse_event(line)

            if event is None:
                continue

            write_ebpf_event(event)

            if event["type"] == "PROCESS_EXEC":
                print(
                    f"[EBPF_PROCESS_EXEC] "
                    f"PID={event['pid']} "
                    f"EXEC={event['executable']}"
                )

            elif event["type"] == "PROCESS_EXIT":
                print(
                    f"[EBPF_PROCESS_EXIT] "
                    f"PID={event['pid']} "
                    f"NAME={event['name']}"
                )

    @staticmethod
    def _parse_event(line):
        parts = line.split("|", 2)

        if len(parts) != 3:
            return None

        event_kind, pid_text, value = parts

        try:
            pid = int(pid_text)
        except ValueError:
            return None

        timestamp = datetime.now(timezone.utc).isoformat()

        if event_kind == "EXEC":
            return {
                "timestamp": timestamp,
                "type": "PROCESS_EXEC",
                "source": "ebpf",
                "pid": pid,
                "executable": value,
            }

        if event_kind == "EXIT":
            return {
                "timestamp": timestamp,
                "type": "PROCESS_EXIT",
                "source": "ebpf",
                "pid": pid,
                "name": value,
            }

        return None

    def stop(self):
        self.running = False

        if self.process is None:
            return

        if self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self.process = None
