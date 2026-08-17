# SAP Auto Print

Windows automation for SAP GUI printing using **Python + pywinauto**.

The script detects the SAP `Print:` dialog, clicks **Print**, and handles the PDF-related Windows error dialog only when it actually appears.

> **Important:** The automation uses Windows UI controls instead of mouse coordinates, making it more reliable when the mouse is moved elsewhere.

---

## ✨ Features

- Detects SAP `Print:` window
- Clicks **Print** only once per print dialog
- Detects the PDF/application error dialog
- Presses **Enter / OK** only when the expected error is detected
- Waits for the current operation before continuing
- Works without relying on mouse position
- Designed for repeated SAP invoice printing

---

## 🖥️ Requirements

- Windows 10/11 64-bit
- SAP GUI for Windows
- Python **3.12.x 64-bit**
- Internet connection for initial package installation

---

## 📁 Project Structure

```text
SAP_AutoPrint/
├── README.md
├── requirements.txt
├── sap_window_test.py
├── sap_auto_print.py
└── logs/
```

---

## 🚀 Setup on a New PC

### 1. Install Python

Install **Python 3.12.x 64-bit** from:

https://www.python.org/downloads/windows/

During installation, enable:

```text
Add python.exe to PATH
```

Check:

```bat
python --version
```

Expected:

```text
Python 3.12.x
```

Check 64-bit:

```bat
python -c "import platform; print(platform.architecture())"
```

---

### 2. Clone the Repository

```bat
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SAP_AutoPrint
```

Or simply download the repository and open Command Prompt inside the project folder.

---

### 3. Create Virtual Environment

```bat
python -m venv .venv
```

Activate it:

```bat
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

in the Command Prompt.

---

### 4. Install Dependencies

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify:

```bat
python -c "from pywinauto import Desktop; print('pywinauto OK')"
```

Expected:

```text
pywinauto OK
```

---

## 🔍 Test SAP Window Detection

Before running the automation, test the SAP controls.

Start SAP and make the:

```text
Print:
```

window visible.

Then run:

```bat
python sap_window_test.py
```

The diagnostic script should show:

- SAP Print window
- Window title
- Window class
- Print button
- Control class
- Control handle

---

## ⚠️ Test the Error Window

Trigger the PDF error and leave the error dialog open.

Run:

```bat
python sap_window_test.py
```

The script should detect the Windows error dialog and display its controls.

The expected error contains:

```text
This file does not have an app associated with it
```

The final automation should verify this error before pressing **Enter**.

---

## ▶️ Run Automation

After the diagnostic test is successful:

```bat
python sap_auto_print.py
```

Expected workflow:

```text
SAP Print appears
       ↓
Detect Print
       ↓
Click Print once
       ↓
Wait
       ↓
Error?
   ┌───┴───┐
   │       │
  YES      NO
   │       │
   ↓       ↓
Press OK  Continue
   │       │
   └───┬───┘
       ↓
Wait for next Print
```

---

## 🛡️ Reliability Rules

The production script must:

- **Never** blindly press Enter
- **Never** repeatedly click Print
- **Never** depend on screen coordinates
- Verify the error dialog before pressing Enter
- Wait for the current print operation to finish
- Test with a small number of invoices before a large batch

---

## 🧪 Recommended Testing

Test in this order:

| Test | Invoices |
|---|---:|
| Initial test | 1 |
| Small test | 2–5 |
| Medium test | 10–20 |
| Production | Full batch |

Do not start with the full batch on a new PC.

---

## 🔧 Troubleshooting

### `python` is not recognized

Reinstall Python and enable:

```text
Add python.exe to PATH
```

Then open a new Command Prompt.

### `pywinauto` import error

Run:

```bat
python -m pip install --upgrade pywinauto
```

Then:

```bat
python -c "from pywinauto import Desktop; print('pywinauto OK')"
```

### pywin32 DLL error

Only troubleshoot this if `pywinauto` itself fails.

Try:

```bat
python -m pip uninstall pywin32 -y
python -m pip install --upgrade --force-reinstall pywin32
```

If a DLL error remains, install the Microsoft Visual C++ Redistributable:

https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

Then restart Windows and test again.

> Do not repeat the original PC's pywin32 troubleshooting unless the new PC actually has the same problem.

---

## 🔐 SAP Permissions

Python and SAP should normally run at the same Windows privilege level.

If the script cannot see SAP windows:

1. Check whether SAP is running as Administrator.
2. Check whether Python is running as Administrator.
3. Make their privilege levels consistent.
4. Run `sap_window_test.py` again.

---

## 🧰 Useful Commands

Check Python:

```bat
python --version
```

Check architecture:

```bat
python -c "import platform; print(platform.architecture())"
```

Check pywinauto:

```bat
python -c "import pywinauto; print(pywinauto.__version__)"
```

Check pywin32:

```bat
python -m pip show pywin32
```

Check installed packages:

```bat
python -m pip list
```

---

## 📌 Current SAP Window Information

Known from the working PC:

```text
Process: saplogon.exe
Print window: Print:
Class: #32770
```

Window Spy previously identified:

```text
Print button: Button3
Error dialog class: #32770
OK button: Button1
```

These identifiers should be **verified with `sap_window_test.py` on each new PC** instead of blindly assuming they are unchanged.

---

## 🆘 Emergency Stop

If the automation behaves unexpectedly, stop it with:

```text
Ctrl + C
```

in the Command Prompt running the script.

---

## 📝 Deployment Checklist

Before using the automation on a new PC:

- [ ] SAP GUI installed
- [ ] SAP login works
- [ ] Python 3.12 64-bit installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `pywinauto OK` test passes
- [ ] SAP Print window detected
- [ ] Print button verified
- [ ] Error dialog detected
- [ ] Error message verified
- [ ] One-invoice test successful
- [ ] Small batch test successful

---

## 🎯 Goal

The setup should be:

```text
New PC
  ↓
Install Python
  ↓
Clone repository
  ↓
Create .venv
  ↓
Install requirements
  ↓
Run diagnostic
  ↓
Verify SAP controls
  ↓
Run automation
```

This avoids repeating the installation/debugging process from the original PC.
