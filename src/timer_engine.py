import time


class TimerEngine:

    def __init__(self):
        self.current_target = None
        self.start_time = None

    def update(self, target):

        # switched to new distraction
        if self.current_target != target:
            self.current_target = target
            self.start_time = time.time()
            return False

        elapsed = time.time() - self.start_time

        if elapsed >= 10:
            self.start_time = time.time()
            return True

        return False

    def reset(self):
        self.current_target = None
        self.start_time = None