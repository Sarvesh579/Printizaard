import tkinter as tk
from tkinter import ttk
from file_handler import FileHandler
from printer import PrinterManager
from logger import Logger
import threading
import time
import os
from settings_manager import SettingsManager

class PrintizaardUI:
    def __init__(self, root):
        self.root = root
        self.settings = SettingsManager()
        self.root.title("Printizaard")
        self.root.geometry("520x340")

        self.file_handler = FileHandler()
        self.printer_manager = PrinterManager()
        self.logger = Logger()

        self.printer_map = {}
        self.selected_printer = tk.StringVar()

        self.build_ui()
        self.load_printers()
        self.update_display()

        self.root.bind("<Return>", self.next_action)

    def build_ui(self):
        tk.Label(self.root, text="Printer:", font=("Arial", 11)).pack(pady=5)

        self.printer_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.selected_printer,
            state="readonly",
            width=55
        )
        self.printer_dropdown.pack()

        self.file_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.file_label.pack(pady=15)

        self.total_pages_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.total_pages_label.pack()

        self.mode_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.mode_label.pack(pady=10)

        self.next_button = tk.Button(
            self.root,
            text="PRINT / NEXT",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            width=22,
            command=self.next_action
        )
        self.next_button.pack(pady=15)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack()
        self.set_button_state(True)


    def load_printers(self):
        display_list = []            
        for p in self.printer_manager.printers:
            display = f"{p['name']} → {p['status']}"
            display_list.append(display)
            self.printer_map[display] = p["name"]
            self.logger.write(f"Detected printer: {p['name']} | Status: {p['status']}")

        self.printer_dropdown["values"] = display_list
        last_used = self.settings.get_last_printer()
        default = self.printer_manager.get_default_printer()

        # Try last used for this PC
        if last_used:
            for key, value in self.printer_map.items():
                if value == last_used:
                    self.selected_printer.set(key)
                    return

        # Fallback to system default
        for key, value in self.printer_map.items():
            if value == default:
                self.selected_printer.set(key)
                return

        # Final fallback → first printer in list
        if self.printer_dropdown["values"]:
            self.selected_printer.set(self.printer_dropdown["values"][0])

    def update_display(self):
        info = self.file_handler.get_print_info()
        if not info:
            self.file_label.config(text="✅ ALL FILES COMPLETED")
            self.total_pages_label.config(text="")
            self.mode_label.config(text="")
            self.next_button.config(state="disabled")
            return

        self.file_label.config(text=info["file"])
        self.total_pages_label.config(text=f"Total pages: {info['total']}")
        self.mode_label.config(text = (
            "Print 1 page"
            if info["mode"] == "SINGLE"
            else f"{info['mode']} → Print {info['count']} pages"
        ))

    def is_virtual_printer(self, printer_name):
        blocked = ["PDF", "OneNote", "XPS"]
        return any(word in printer_name for word in blocked)

    def next_action(self, event=None):
        self.logger.write("User pressed PRINT / NEXT")
        info = self.file_handler.get_print_info()
        if not info:
            return

        selected_display = self.selected_printer.get()
        printer = self.printer_map.get(selected_display)
        if not printer:
            self.status_label.config(text="❌ No printer selected")
            return
        self.logger.write(f"Selected printer: {printer}")

        if self.is_virtual_printer(printer):
            self.status_label.config(text="❌ Cannot print to virtual printer")
            return

        file_path = os.path.join(os.getcwd(), info["file"])
        self.set_button_state(False)
        self.status_label.config(text="🖨 Printing...")
        self.logger.write(f"Printing file: {info['file']} | Mode: {info['mode']}")

        threading.Thread(
            target=self.print_job,
            args=(file_path, printer),
            daemon=True
        ).start()

    def print_job(self, file_path, printer):
        try:
            self.printer_manager.print_pdf(file_path, printer, self.logger)
            time.sleep(3)
            self.root.after(0, self.print_success)
            self.logger.write("Print successful, moving to next step")
        except Exception as e:
            self.root.after(0, self.print_error, str(e))

    def print_success(self):
        self.file_handler.next_step()
        self.update_display()
        self.status_label.config(text="✅ Done")
        self.set_button_state(True)
        selected_display = self.selected_printer.get()
        printer = self.printer_map.get(selected_display)
        self.settings.set_last_printer(printer)

    def print_error(self, message):
        self.status_label.config(text=f"❌ {message}")
        self.logger.write(f"ERROR: {message}")
        self.set_button_state(True)

    def set_button_state(self, enabled):
        if enabled:
            self.next_button.config(
                state="normal",
                bg="#4CAF50",
                activebackground="#45a049",
                fg="white"
            )
        else:
            self.next_button.config(
                state="disabled",
                bg="grey",
                fg="white"
            )