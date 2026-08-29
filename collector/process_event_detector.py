class ProcessEventDetector:
    def __init__(self):
        self.previous = {}
        self.initialized = False

    def detect(self, processes):
        current = {process.pid: process for process in processes}

        # First scan: establish baseline
        if not self.initialized:
            self.previous = current
            self.initialized = True
            return [], []

        # New processes
        started_pids = current.keys() - self.previous.keys()

        # Exited processes
        exited_pids = self.previous.keys() - current.keys()

        started = [
            current[pid]
            for pid in started_pids
        ]

        exited = [
            self.previous[pid]
            for pid in exited_pids
        ]

        self.previous = current

        return started, exited
