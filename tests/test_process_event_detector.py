from collector.models import ProcessInfo
from collector.process_event_detector import ProcessEventDetector


def make_process(pid, ppid=1, name="test"):
    return ProcessInfo(
        pid=pid,
        ppid=ppid,
        username="lou",
        name=name,
        command=name,
        status="running",
        cpu_percent=0.0,
        memory_percent=0.0,
        create_time=0.0,
    )


def test_first_scan_creates_baseline_only():
    detector = ProcessEventDetector()

    processes = [
        make_process(100),
        make_process(200),
    ]

    started, exited = detector.detect(processes)

    assert started == []
    assert exited == []


def test_detect_new_process():
    detector = ProcessEventDetector()

    detector.detect([
        make_process(100),
    ])

    started, exited = detector.detect([
        make_process(100),
        make_process(200),
    ])

    assert len(started) == 1
    assert started[0].pid == 200
    assert exited == []


def test_detect_exited_process():
    detector = ProcessEventDetector()

    detector.detect([
        make_process(100),
        make_process(200),
    ])

    started, exited = detector.detect([
        make_process(100),
    ])

    assert started == []
    assert len(exited) == 1
    assert exited[0].pid == 200
