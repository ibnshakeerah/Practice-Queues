import time  
import threading  
import queue  
from flask import Flask, jsonify, request  

def dummy_task(seconds):
    print(f"Task started: sleeping for {seconds} seconds…")
    time.sleep(seconds)
    print(f"Task completed after {seconds} seconds.")

sequential_queue = queue.Queue()  
concurrent_queue = queue.Queue()  

# worker function for sequential tasks 
def sequential_worker():
    while True:
        try:
            seconds = sequential_queue.get(timeout=1)  
            dummy_task(seconds) 
            sequential_queue.task_done()  
        except queue.Empty:
            continue  

# The number of concurrent tasks allowed
concurrent_limit = 3  
sem = threading.Semaphore(concurrent_limit)  

# Worker function for concurrent tasks
def worker(seconds):
    with sem:
        dummy_task(seconds)

# concurrent worker function on a separate thread 
def concurrent_worker():
    while True:
        try:
            seconds = concurrent_queue.get(timeout=1)  
            thread = threading.Thread(target=worker, args=(seconds,))  
            thread.start()  
            concurrent_queue.task_done()  
        except queue.Empty:
            continue  

def background_workers():
    # Start background threads for both sequential and concurrent workers
    sequential_thread = threading.Thread(target=sequential_worker, daemon=True)
    sequential_thread.start()
    concurrent_thread = threading.Thread(target=concurrent_worker, daemon=True)
    concurrent_thread.start()

app = Flask(__name__)  

# Endpoint to add tasks to the sequential queue
@app.route("/add_sequential_task", methods=["POST"])
def add_sequential_task():
    data = request.json  
    seconds = data.get("seconds")  

    if seconds is None:
        return jsonify({"error": "Invalid input"}), 400  

    # Add the task to the sequential queue
    print(f"Adding sequential task: {seconds} seconds.")
    sequential_queue.put(seconds)  
    return jsonify({"message": f"Sequential task added: {seconds} seconds."})

# Endpoint to add tasks to the concurrent queue
@app.route("/add_concurrent_task", methods=["POST"])
def add_concurrent_task():
    
    data = request.json  
    seconds = data.get("seconds")  

    if seconds is None:
        return jsonify({"error": "Invalid input"}), 400  
    
    # Add the task to the concurrent queue
    print(f"Adding concurrent task: {seconds} seconds.")
    concurrent_queue.put(seconds)  
    return jsonify({"message" : f"Concurrent task added: {seconds} seconds."})

# Home route
@app.route("/", methods=["GET"])
def index():
    return "<h1>Welcome to the Task Queue App!</h1>"

if __name__ == "__main__":
    background_workers()
    print("Starting flask app...")
    app.run()