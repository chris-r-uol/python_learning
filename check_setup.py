from __future__ import print_function

"""
check_setup.py - Week 1 setup check.

    python check_setup.py

It reports whether your machine is ready. Nothing is collected. Read what it
prints: each problem comes with its fix.

This file is written so that Python 2 can parse it. A student running an old
interpreter then sees a clear message instead of a SyntaxError.

DO NOT convert this file to f-strings. The rest of the course uses them and
should. But the `f"..."` prefix did not exist before Python 3.6, so on an
older interpreter this file would fail to parse. The student would see a
SyntaxError instead of the message saying their Python is too old. That
message is the point of the file. Keep .format() here.
"""

import os
import platform
import sys

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 11

REQUIRED_PACKAGES = ["numpy", "matplotlib", "pandas", "requests"]

LINE = "-" * 60


def say(label, value):
    print("{0:<22} {1}".format(label + ":", value))


def check_python_version():
    version = sys.version_info
    say("Python version", "{0}.{1}.{2}".format(version[0], version[1], version[2]))
    say("Interpreter path", sys.executable)

    if version[0] < 3:
        return [
            "You are running Python 2. The course needs Python 3.11 or newer.",
            "On macOS/Linux try 'python3 check_setup.py' instead of 'python'.",
        ]
    if (version[0], version[1]) < (REQUIRED_MAJOR, REQUIRED_MINOR):
        return [
            "Python {0}.{1} is too old - the course needs {2}.{3} or newer.".format(
                version[0], version[1], REQUIRED_MAJOR, REQUIRED_MINOR
            )
        ]
    return []


def check_macos_system_python():
    """The macOS system Python cannot install packages. Catch it by path."""
    if platform.system() != "Darwin":
        return []
    path = sys.executable
    if path.startswith("/usr/bin/") or "/System/Library/" in path:
        return [
            "You are using the macOS system Python, which cannot install packages.",
            "Install Python from python.org, then re-run this check.",
        ]
    return []


def check_windows_store_python():
    """The Windows Store version causes confusing failures. Catch it."""
    if platform.system() != "Windows":
        return []
    if "WindowsApps" in sys.executable:
        return [
            "You are using the Windows Store version of Python.",
            "Uninstall it and install Python from python.org, ticking",
            "'Add python.exe to PATH' on the first screen of the installer.",
        ]
    return []


def running_on_colab():
    try:
        import google.colab                      # noqa: F401
        return True
    except ImportError:
        return False


def running_on_codespaces():
    return os.environ.get("CODESPACES", "").lower() == "true"


def describe_environment():
    """Report where this is running."""
    if running_on_colab():
        where = "Google Colab"
    elif running_on_codespaces():
        where = "GitHub Codespaces"
    else:
        where = "your own machine"
    say("Running on", where)
    return where


def check_virtual_environment():
    """Advisory, not blocking. Returns a list of notes."""
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    say("Virtual environment", "active" if in_venv else "NOT active")

    if in_venv:
        return []

    if running_on_colab():
        return [
            "No virtual environment is active. On Colab this is normal.",
            "Colab manages the environment. Nothing to fix.",
        ]

    if running_on_codespaces():
        return [
            "No virtual environment is active. On Codespaces there should",
            "be one. Two likely reasons:",
            "  - the setup step was still running when this terminal opened.",
            "    Close the terminal, open a new one, run this again.",
            "  - your Codespace was created before the course configuration",
            "    was added. Rebuild it: press F1, then choose",
            "    'Codespaces: Rebuild Container'.",
        ]

    return [
        "No virtual environment is active. Python still works, so you can",
        "carry on today. You will need one from week 2 onwards.",
        "The activation command is in your setup guide. Run it in every new",
        "terminal window. This is the step most often forgotten.",
    ]


def check_packages():
    problems = []
    for name in REQUIRED_PACKAGES:
        try:
            module = __import__(name)
            version = getattr(module, "__version__", "unknown version")
            say(name, version)
        except ImportError:
            say(name, "NOT INSTALLED")
            problems.append(
                "'{0}' is not installed. Run: pip install -r requirements.txt".format(name)
            )
    return problems


def check_working_directory():
    """Advisory, not blocking. Returns a list of notes."""
    cwd = os.getcwd()
    say("Working directory", cwd)
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(cwd) != here:
        return [
            "You are running this from a different folder to the one it is",
            "in. Nothing is broken. This is the most common cause of",
            "'file not found' errors later.",
            "Try: cd {0}".format(here),
        ]
    return []


def main():
    print(LINE)
    print("PYTHON SETUP CHECK")
    print(LINE)

    say("Operating system", "{0} {1}".format(platform.system(), platform.release()))
    describe_environment()

    # Blockers stop you working. Notes do not. Some notes are normal,
    # depending on where the check is run.
    blockers = []
    blockers += check_python_version()
    blockers += check_macos_system_python()
    blockers += check_windows_store_python()
    blockers += check_packages()

    notes = []
    notes += check_virtual_environment()
    notes += check_working_directory()

    print(LINE)

    if blockers:
        print("NOT READY YET.")
        print("")
        print("Fix these before week 1. Each line below says what to do:")
        print("")
        for blocker in blockers:
            print("  " + blocker)
    elif notes:
        print("READY, WITH NOTES.")
        print("")
        print("Everything the course needs is installed and working.")
        print("This is a pass. Read the notes below. Some are normal for")
        print("where you are running. Some are worth acting on.")
    else:
        print("ALL CHECKS PASSED.")
        print("")
        print("Everything the course needs is installed and working.")

    if notes:
        print("")
        print("Notes:")
        print("")
        for note in notes:
            print("  " + note)

    if blockers:
        print("")
        print("What to do:")
        print("")
        print("  1. Read the lines above. They name the problem and the fix.")
        print("  2. Read the 'If this fails' notes in your setup guide.")
        print("     Common failures are listed there with their fixes.")
        print("  3. Paste the exact error into an AI assistant. Ask what it")
        print("     means. Setup errors are well documented.")
        print("  4. After 30 minutes, stop. Use GitHub Codespaces instead:")
        print("     see setup/codespaces.md. Nothing to install, and nothing")
        print("     your machine can block.")
    print(LINE)


if __name__ == "__main__":
    main()
