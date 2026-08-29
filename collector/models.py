from dataclasses import dataclass, asdict


@dataclass
class ProcessInfo:
    pid: int
    ppid: int
    username: str
    name: str
    command: str
    status: str
    cpu_percent: float
    memory_percent: float
    create_time: float

    def to_dict(self):
        return asdict(self)


@dataclass
class SystemInfo:
    cpu_percent: float
    memory_total: int
    memory_used: int
    memory_available: int
    memory_percent: float
    swap_total: int
    swap_used: int
    swap_percent: float
    disk_read_bytes: int
    disk_write_bytes: int

    def to_dict(self):
        return asdict(self)
