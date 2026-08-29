import psutil
from collector.models import ProcessInfo


def collect_processes():
    processes = []

    for process in psutil.process_iter([
        "pid",
        "ppid",
        "username",
        "name",
        "cmdline",
        "status",
        "cpu_percent",
        "memory_percent",
        "create_time",
    ]):
        try:
            info = process.info

            processes.append(
                ProcessInfo(
                    pid=info["pid"],
                    ppid=info["ppid"],
                    username=info["username"] or "unknown",
                    name=info["name"] or "",
                    command=" ".join(info["cmdline"] or []),
                    status=info["status"] or "",
                    cpu_percent=info["cpu_percent"] or 0.0,
                    memory_percent=info["memory_percent"] or 0.0,
                    create_time=info["create_time"] or 0.0,
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes
