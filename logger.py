import os
import datetime
import platform

LOG_FILE = "Printizaard_log.txt"


class Logger:

    def __init__(self):
        self.log_path = os.path.join(os.getcwd(), LOG_FILE)
        self.write_header()

    def write(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def write_header(self):
        self.write("========== Printizaard Started ==========")
        self.write(f"PC Name: {os.environ.get('COMPUTERNAME')}")
        self.write(f"User: {os.environ.get('USERNAME')}")
        self.write(f"OS: {platform.system()} {platform.release()}")
        self.write("----------------------------------------")