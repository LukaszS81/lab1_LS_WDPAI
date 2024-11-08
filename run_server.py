from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os
import signal

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, process):
        super().__init__()
        self.process = process

    def on_modified(self, event):
        # Restartuj serwer przy zmianach w pliku server.py
        if event.src_path.endswith("server.py"):
            print("Zmieniono server.py, restartowanie serwera...")
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
            self.process = subprocess.Popen(["python", "server.py"])

def start_server():
    process = subprocess.Popen(["python", "server.py"])
    event_handler = FileChangeHandler(process)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    process.terminate()

if __name__ == "__main__":
    start_server()
