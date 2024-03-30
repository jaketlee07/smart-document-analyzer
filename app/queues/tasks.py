# Contents of queues/tasks.py
import threading
from queue import Queue
from time import sleep

def process_pdf_function(pdf_path):
    print(f"Starting PDF processing for: {pdf_path}")
    sleep(2)
    print(f"PDF processing completed for: {pdf_path}")
    return True

def perform_nlp_analysis(text):
    print(f"Starting NLP analysis for text: {text[:30]}...")
    sleep(2)
    print("NLP analysis completed.")
    return True

task_queue = Queue()

def task_processor():
    while True:
        task, args = task_queue.get()
        try:
            task(*args)
        finally:
            task_queue.task_done()

threading.Thread(target=task_processor, daemon=True).start()
