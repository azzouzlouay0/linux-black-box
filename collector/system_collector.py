import psutil
from collector.models import SystemInfo


def collect_system():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_io_counters()

    return SystemInfo(
        cpu_percent=psutil.cpu_percent(interval=1),
        memory_total=memory.total,
        memory_used=memory.used,
        memory_available=memory.available,
        memory_percent=memory.percent,
        swap_total=swap.total,
        swap_used=swap.used,
        swap_percent=swap.percent,
        disk_read_bytes=disk.read_bytes if disk else 0,
        disk_write_bytes=disk.write_bytes if disk else 0,
    )
