import subprocess
import threading
from datetime import datetime, timezone

from storage.event_writer import write_ebpf_event


class EbpfExecCollector:
    def __init__(self):
        self.process = None
        self.thread = None
        self.running = False

    def start(self):
        command = [
            "sudo",
            "bpftrace",
            "-q",
            "-e",
            (
                'tracepoint:syscalls:sys_enter_execve '
                '{ printf("%d|%s\\n", pid, str(args->filename)); }'
            ),
        ]

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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

            if not line or "|" not in line:
                continue

            try:
                pid_text, executable = line.split("|", 1)
                pid = int(pid_text)

                event = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "type": "PROCESS_EXEC",
                    "source": "ebpf",
                    "pid": pid,
                    "executable": executable,
                }

                write_ebpf_event(event)

                print(
                    f"[EBPF_PROCESS_EXEC] "
                    f"PID={pid} "
                    f"EXEC={executable}"
                )

            except ValueError:
                continue

    def stop(self):
        self.running = False

        if self.process is not None:
            self.process.terminate()
            self.process.wait(timeout=5)
