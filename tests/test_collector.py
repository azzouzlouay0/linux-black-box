from collector.process_collector import collect_processes
from collector.system_collector import collect_system


def test_process_collector_returns_data():
    processes = collect_processes()
    assert len(processes) > 0


def test_system_collector():
    system = collect_system()

    assert system.cpu_percent >= 0
    assert system.memory_total > 0
