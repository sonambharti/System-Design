"""
# Job Schedular

Key Concept: Schedule jobs to run at a specific time.
Use Case: Cron jobs, background tasks.

"""

import threading
import time

class JobScheduler:
    def __init__(self):
        self.jobs = []

    def schedule(self, delay, func, *args):
        """Schedules a function to run after 'delay' seconds."""
        job_thread = threading.Thread(target=self._run_job, args=(delay, func, args))
        self.jobs.append(job_thread)
        job_thread.start()

    def _run_job(self, delay, func, args):
        """Waits and then executes the function."""
        time.sleep(delay)
        func(*args)

# Usage
def print_message(msg):
    print("Executing:", msg)

scheduler = JobScheduler()
scheduler.schedule(2, print_message, "Hello, Sonam!")  # Runs after 2 sec
