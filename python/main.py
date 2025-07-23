import time
from collections import deque

task_queue = deque()

def dummy_task(seconds):
    print(f"Task started: sleeping for {seconds} seconds…")
    time.sleep(seconds)
    print(f"Task completed after {seconds} seconds.")

# Function to process tasks in the queue
def process_tasks():
    while task_queue:
        task = task_queue.popleft()
        dummy_task(task)

try:
    while True:
        duration = input("Enter seconds or 'exit': ")
        if duration.lower() == 'exit':
            print("Exiting...")
            break
        try:
            seconds = int(duration)
            task_queue.append(seconds)
            print(f"Task added: {seconds} seconds.")
            process_tasks()
        except ValueError:
            print("please enter a valid number or 'exit'.")
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Goodbye!")