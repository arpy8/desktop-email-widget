import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class Watcher(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.python_executable = sys.executable
        self.run_script()

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"[INFO] {self.script} changed, restarting...")
            self.restart_script()

    def run_script(self):
        print(f"[INFO] Running: {self.python_executable} {self.script}")
        self.process = subprocess.Popen([self.python_executable, self.script])

    def restart_script(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.run_script()

if __name__ == "__main__":
    script_to_watch = "main.py"
    if not Path(script_to_watch).exists():
        print(f"[ERROR] Script {script_to_watch} not found.")
        sys.exit(1)

    event_handler = Watcher(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print(f"[INFO] Watching for changes in {script_to_watch}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()