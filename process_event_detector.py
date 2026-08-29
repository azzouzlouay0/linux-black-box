class ProcessEventDetector:
    def __init__(self):
        self.previous = {}

    def detect(self, processes):
        current = {p.pid: p for p in processes}

        started = [
            current[pid]
            for pid in current.keys() - self.previous.keys()
        ]

        exited = [
            self.previous[pid]
            for pid in self.previous.keys() - current.keys()
        ]

        self.previous = current

        return started, exited
