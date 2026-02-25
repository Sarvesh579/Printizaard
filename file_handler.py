import os
from PyPDF2 import PdfReader
import win32com.client


class FileHandler:

    def __init__(self):

        self.folder = os.getcwd()
        self.temp_folder = os.path.join(self.folder, "Printizaard_temp")

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        self.files = self.prepare_files()

        self.index = 0
        self.mode = "ODD"

    def prepare_files(self):

        files = []

        word = None

        for f in os.listdir(self.folder):

            if f.lower().endswith(".pdf"):
                files.append(f)

            elif f.lower().endswith((".doc", ".docx")):

                # open Word only once (faster & safer)
                if word is None:
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False

                pdf_name = self.convert_word_to_pdf(word, f)

                if pdf_name:
                    files.append(pdf_name)

        if word:
            word.Quit()

        files.sort()
        return files

    def convert_word_to_pdf(self, word, word_file):

        try:

            doc = word.Documents.Open(os.path.join(self.folder, word_file))

            pdf_name = os.path.splitext(word_file)[0] + ".pdf"
            pdf_path = os.path.join(self.temp_folder, pdf_name)

            doc.SaveAs(pdf_path, FileFormat=17)
            doc.Close()

            return os.path.join("Printizaard_temp", pdf_name)

        except Exception as e:
            print("Word conversion failed:", e)
            return None

    def get_print_info(self):

        if self.index >= len(self.files):
            return None

        file = self.files[self.index]
        total = len(PdfReader(os.path.join(self.folder, file)).pages)

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