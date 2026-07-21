import time


class TimerEngine:

    def __init__(self, reminder_delay=10):
        self.reminder_delay = reminder_delay
        self.start_time = None
        self.current_target = None

    def update(self, target):
        """
        Update the reminder timer for the current monitored target.

        Returns True when the reminder delay has elapsed.
        Otherwise returns False.

        Passing None represents the absence of a monitored target
        and resets the timer.
        """

        # ----------------------------------------------------
        # NO ACTIVE MONITORED TARGET
        # ----------------------------------------------------

        if target is None:
            self.reset()
            return False

        # ----------------------------------------------------
        # TARGET CHANGED OR TIMER HAS NOT STARTED
        # ----------------------------------------------------

        if self.current_target != target or self.start_time is None:
            self.current_target = target
            self.start_time = time.time()

            return False

        # ----------------------------------------------------
        # SAME TARGET - CHECK ELAPSED TIME
        # ----------------------------------------------------

        elapsed = time.time() - self.start_time

        if elapsed >= self.reminder_delay:
            self.start_time = time.time()

            return True

        return False

    def reset(self):
        """
        Reset all timer state.
        """

        self.start_time = None
        self.current_target = None
