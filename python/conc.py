import time 
from concurrent.futures import ThreadPoolExecutor

def dummy_task(name, seconds):
    print(f"Task {name} started: sleeping for {seconds} seconds...")
    time.sleep(seconds)
    print(f"Task {name} completed after {seconds} seconds.")

def run_tasks(concurrent_limit=3):
    with ThreadPoolExecutor(max_workers=concurrent_limit) as executor:
        futures = []
        for i in range(10):
            name = f"Task-{i + 1}"
            seconds = i % 3 + 1
            futures.append(executor.submit(dummy_task, name, seconds))

            for future in futures:
                future.result()
                print("All tasks completed.")

if __name__ == "__main__":
    run_tasks()