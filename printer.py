import win32print
import subprocess
import shutil

class PrinterManager:
    def __init__(self):
        self.printers = self.get_printers()
        self.default_printer = win32print.GetDefaultPrinter()
        self.edge_path = self.find_edge()

    def find_edge(self):
        paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        for p in paths:
            if shutil.which(p) or shutil.os.path.exists(p):
                return p
        return None

    def get_printers(self):
      printer_list = []
      flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
      printers = win32print.EnumPrinters(flags, None, 2)

      for p in printers:
          name = p["pPrinterName"]
          attributes = p["Attributes"]
          work_offline = attributes & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE

          try:
              handle = win32print.OpenPrinter(name)
              win32print.ClosePrinter(handle)
              accessible = True
          except:
              accessible = False

          if work_offline:
              state = "OFFLINE"
          elif not accessible:
              state = "NOT AVAILABLE"
          else:
              state = "READY"

          printer_list.append({
              "name": name,
              "status": state
          })
      return printer_list

    def get_default_printer(self):
        return self.default_printer

    def print_pdf(self, file_path, printer_name):
        if not self.edge_path:
            raise Exception("Microsoft Edge not found")

        try:
            result = subprocess.run(
                [
                    self.edge_path,
                    "--headless",
                    "--disable-gpu",
                    f'--print-to-printer={printer_name}',
                    file_path
                ],
                capture_output=True,
                text=True,
                timeout=10   # ⬅️ KEY FIX
            )

            if result.returncode != 0:
                error = result.stderr.strip() or "Printing failed"
                raise Exception(error)

        except subprocess.TimeoutExpired:
            raise Exception("Printer not responding / not connected")