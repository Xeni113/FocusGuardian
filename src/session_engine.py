import time


class SessionEngine:
    def __init__(self):
        self.current_target = None
        self.start_time = None

    def start_session(self, target):
        """Start a new tracked session."""

        if target is None:
            return

        self.current_target = target
        self.start_time = time.time()

    def end_session(self):
        """Finish the current session and return its data."""

        if self.current_target is None or self.start_time is None:
            return None

        duration = max(0, int(time.time() - self.start_time))

        result = {
            "target": self.current_target,
            "duration": duration,
        }

        # Completely reset state
        self.current_target = None
        self.start_time = None

        return result

    def switch_target(self, target):
        """
        Change the currently tracked target.

        Cases:
        None -> YouTube       : start YouTube
        YouTube -> YouTube    : continue existing session
        YouTube -> Gemini     : finish YouTube, start Gemini
        YouTube -> None       : finish YouTube
        None -> None          : do nothing
        """

        # Nothing changed
        if target == self.current_target:
            return None

        # Finish whatever was previously active
        old_session = self.end_session()

        # Start the new target only if it is trackable
        if target is not None:
            self.start_session(target)

        return old_session

    def get_current_session(self):
        """Return information about the active session."""

        if self.current_target is None or self.start_time is None:
            return None

        return {
            "target": self.current_target,
            "duration": max(0, int(time.time() - self.start_time)),
        }

    def is_active(self):
        return self.current_target is not None
