import time


class Timer:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} start")
        self.start_time = time.perf_counter()

    def finish(self):
        elapsed_time = time.perf_counter() - self.start_time
        print(f"{self.name} elapsed time: {(elapsed_time * 1000):.6f} ms")
