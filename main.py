import tkinter as tk
from ui import PrintizaardUI
import sys
from logger import Logger

logger = Logger()

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.write(f"FATAL ERROR: {exc_value}")

sys.excepthook = handle_exception
root = tk.Tk()
app = PrintizaardUI(root)
root.mainloop()