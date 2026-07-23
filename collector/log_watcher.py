import chardet
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogWatcherHandler(FileSystemEventHandler):
    def __init__(self, log_file, callback):
        self.log_file = os.path.abspath(log_file)
        self.callback = callback
        self._last_position = 0
        self._encoding = self._detect_encoding()
    def _detect_encoding(self):
        try:
            with open(self.log_file, 'rb') as f:
                raw = f.read(10000) 
                result = chardet.detect(raw)
                return result['encoding'] or 'utf-8'
        except:
            return 'utf-8'
    def on_modified(self, event):
        if event.src_path == self.log_file:
            self._read_new_lines()
    def _read_new_lines(self):
        with open(self.log_file, 'r', encoding=self._encoding, errors='replace') as f:
            f.seek(self._last_position)
            new_content = f.read()
            if new_content:
                lines = new_content.splitlines()
                for line in lines:
                    if line.strip():
                        self.callback(line)
                self._last_position = f.tell()

class LogWatcher:
    def __init__(self, log_file, callback):
        self.log_file = os.path.abspath(log_file)
        self.handler = LogWatcherHandler(self.log_file, callback)
        self.observer = Observer()

    def start(self):
        log_dir = os.path.dirname(os.path.abspath(self.log_file))
        self.observer.schedule(self.handler, path=log_dir, recursive=False)
        self.observer.start()
        print(f"开始监听日志文件: {self.log_file}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print("停止日志监听")