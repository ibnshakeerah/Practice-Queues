import time
import queue
import threading

task_queue = queue.Queue()

def dummy_task(name, seconds):
    print(f"Task {name} started: sleeping for {seconds} seconds...")
    time.sleep(seconds)
    print(f"Task {name} completed after {seconds} seconds.")

# Add tasks to the queue with varying sleep durations (1, 2, or 3 seconds)
for i in range(10):
    task_queue.put((f"Task-{i + 1}", i % 3 + 1))

def worker(sem):
    while True:
        try:
            name, seconds = task_queue.get(timeout=1)
            with sem:
                dummy_task(name, seconds)
            task_queue.task_done()
        except queue.Empty:
            break

def run_tasks(concurrent_limit=3):
    threads = []
    sem = threading.Semaphore(concurrent_limit)
    for _ in range(5):  # create 5 worker threads
        thread = threading.Thread(target=worker, args=(sem,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print("All tasks completed.")

if __name__ == "__main__":
    run_tasks()


