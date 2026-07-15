import time


class TimerEngine:

    def __init__(self, reminder_delay=10):
        self.reminder_delay = reminder_delay
        self.start_time = None
        self.current_target = None

    def update(self, target):

        if self.current_target != target:
            self.current_target = target
            self.start_time = time.time()
            return False

        elapsed = time.time() - self.start_time

        if elapsed >= self.reminder_delay:
            self.start_time = time.time()
            return True

        return False

    def reset(self):
        self.start_time = None
        self.current_target = None