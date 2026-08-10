# Setup — macOS

> **STUB.** To be written. Must cover, in this order:

1. Install Python 3.11+ from python.org. Explain plainly that the Python already on
   the machine is the system Python, cannot install packages, and must not be used.
   `check_setup.py` detects it by path and says so.
2. Install VS Code. Install the Python extension.
3. `python3`, not `python` — say this early and repeat it.
4. Terminal basics: opening a terminal in a folder, `cd`, `ls`.
5. Virtual environment: `python3 -m venv .venv` then `source .venv/bin/activate`.
6. `pip install -r requirements.txt`
7. `python3 check_setup.py`

Note the Apple Silicon / Rosetta case only if it actually bites — do not pre-load
students with architecture detail they don't need.
