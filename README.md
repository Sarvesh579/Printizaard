# 🖨️ Printizaard

Printizaard is a **portable, zero-install bulk printing assistant** designed for real print-shop and college lab workflows. Another personal project to solve my daily needs.

It automates the most common manual printing process (as per my need):

➡ Print odd pages  
➡ Flip pages  
➡ Print even pages  
➡ Move to next file  

All with a single **Next / Enter** action.
No repeated print dialog. No setup. Just plug in your pendrive and print.

---

## ✨ Features

- 📄 Automatic PDF detection from current folder
- 📝 Word (`.doc` / `.docx`) → auto converted to PDF
- 🔁 Odd / Even page workflow automation
- ⌨️ Press **Enter** for next step (super fast operation)
- 🖨️ Printer selection with status
- 💾 Remembers last used printer **per PC**
- ⚠️ Proper error handling (printer offline, not responding, etc.)
- 🎯 Designed for print shops / college labs
- 📦 Single portable EXE — no installation required

---

## 🧠 How It Works

1. Place `Printizaard.exe` in the folder that contains your print files
2. Run the EXE
3. Select the correct printer (first time only on each PC)
4. Follow the on-screen steps:

```
ODD → print
Flip pages (Pay attention to the order of pages you put back in)
EVEN → print
Next file
```

---

## 📥 Download

You can directly download the ready-to-use portable EXE from:

```
dist/Printizaard.exe
````

---

## 🛠️ Run From Source (Development)

Clone the repository:

```bash
git clone https://github.com/Sarvesh579/Printizaard.git
cd Printizaard
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

## 📦 Build the EXE Yourself
Bash
```bash
`  pyinstaller --noconfirm --onefile --windowed --name Printizaard \
  --hidden-import=win32com \
  --hidden-import=win32com.client \
  --hidden-import=pythoncom \
  --hidden-import=pywintypes \
  main.py`
```
or Powershell
```powershell
pyinstaller --noconfirm --onefile --windowed --name Printizaard --hidden-import=win32com --hidden-import=win32com.client --hidden-import=pythoncom --hidden-import=pywintypes main.py
```

Output:

```

dist/Printizaard.exe

```

---

## 💻 Requirements on Target PC

Printizaard is portable, but the system should have:

* ✅ Windows
* ✅ Microsoft Edge (used for silent PDF printing)
* ✅ Microsoft Word *(only if printing Word files)*

No Python installation required.

---

## 📁 Typical Pendrive Usage

```

Pendrive/
│── Printizaard.exe
│── file1.pdf
│── file2.docx
│── notes.pdf

```

---

## ⚠️ Notes

* Virtual printers (Microsoft Print to PDF, OneNote, etc.) are blocked intentionally.
* Word files are converted to PDF inside a temporary folder.
* Printer preference is saved **per computer**, not globally.

---

## 🚀 Why Printizaard?

This tool was built for real high-volume print environments where:

* Speed matters
* Repetitive dialogs waste time
* Multiple PCs with different printers are used
* Installation is not allowed

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Made with ☕ to eliminate the pain of manual bulk printing.

````

---

# ✅ Replace this line before committing

```md
git clone https://github.com/<your-username>/Printizaard.git
````

with your actual repo URL.

---

# ⭐ Optional additions (tell me if you want)

We can add:

* screenshots section
* demo GIF
* version badge
* “How odd/even logic works” diagram