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

def sequential_worker():
    while True:
        try:
            seconds = sequential_queue.get(timeout=1)  
            dummy_task(seconds) 
            sequential_queue.task_done()  
        except queue.Empty:
            continue  

concurrent_limit = 3  
sem = threading.Semaphore(concurrent_limit)  

def worker(seconds):
    with sem:
        dummy_task(seconds)

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

@app.route("/add_sequential_task", methods=["POST"])
def add_sequential_task():
    
    data = request.json  
    seconds = data.get("seconds")  

    if seconds is None or not isinstance(seconds, int) or seconds <= 0:
        return jsonify({"error": "Invalid input"}), 400  

    sequential_queue.put(seconds)  
    return jsonify({"message": f"Sequential task added: {seconds} seconds."})

@app.route("/add_concurrent_task", methods=["POST"])
def add_concurrent_task():
    
    data = request.json  
    seconds = data.get("seconds")  

    if seconds is None or not isinstance(seconds, int) or seconds <= 0:
        return jsonify({"error": "Invalid input"}), 400  

    concurrent_queue.put(seconds)  
    return jsonify({"message": f"Concurrent task added: {seconds} seconds."})

if __name__ == "__main__":
    background_workers()
    print("Starting flask app...")
    app.run()