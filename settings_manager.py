import json
import os

SETTINGS_FILE = "settings.json"

class SettingsManager:

    def __init__(self):
        self.pc_name = os.environ.get("COMPUTERNAME")
        self.data = self.load()

    def load(self):
        if not os.path.exists(SETTINGS_FILE):
            return {}

        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_last_printer(self):
        return self.data.get(self.pc_name)

    def set_last_printer(self, printer_name):
        self.data[self.pc_name] = printer_name
        self.save()