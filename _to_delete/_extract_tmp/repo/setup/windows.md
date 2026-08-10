# Setup — Windows

> **STUB.** To be written. Must cover, in this order:

1. Install Python from python.org — **tick "Add python.exe to PATH"** on the first
   installer screen. Screenshot required; this single checkbox causes most week 1
   failures.
2. Do *not* install Python from the Microsoft Store. `check_setup.py` detects and
   rejects it.
3. Install VS Code. Install the Python extension.
4. Open a terminal in the course folder (right-click → Open in Terminal, or VS Code's
   integrated terminal).
5. Create and activate a virtual environment:
   `python -m venv .venv` then `.venv\Scripts\activate`
   — including what to do about the PowerShell execution-policy error, which will hit
   some students.
6. `pip install -r requirements.txt`
7. `python check_setup.py`

Every step gets a screenshot and an "if this fails" line.
