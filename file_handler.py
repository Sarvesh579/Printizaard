import os
from PyPDF2 import PdfReader

class FileHandler:
    def __init__(self):
        self.folder = os.getcwd()
        self.files = self.get_pdf_files()
        self.index = 0
        self.mode = "ODD"

    def get_pdf_files(self):
        pdfs = [f for f in os.listdir(self.folder) if f.lower().endswith(".pdf")]
        pdfs.sort()
        return pdfs

    def has_files(self):
        return self.index < len(self.files)

    def current_file(self):
        if not self.has_files():
            return None
        return self.files[self.index]

    def get_page_count(self, file):
        reader = PdfReader(os.path.join(self.folder, file))
        return len(reader.pages)

    def get_print_info(self):
        if not self.has_files():
            return None

        file = self.current_file()
        total = self.get_page_count(file)

        if self.mode == "ODD":
            pages = (total + 1) // 2
        else:
            pages = total // 2

        return {
            "file": file,
            "total": total,
            "mode": self.mode,
            "count": pages
        }

    def next_step(self):
        if self.mode == "ODD":
            self.mode = "EVEN"
        else:
            self.mode = "ODD"
            self.index += 1