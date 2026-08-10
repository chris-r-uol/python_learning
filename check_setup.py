from __future__ import print_function

"""
check_setup.py - Week 1 diagnostic.

Run this and send us everything it prints. If it fails, send us the error text.
Either outcome is useful - you are not expected to fix it yourself.

    python check_setup.py

Written to be parseable by Python 2 as well as Python 3, so that students who
run it with an old interpreter get a clear message instead of a SyntaxError.
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
    """The macOS system Python cannot install packages. Catch it by name."""
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
    """The Windows Store shim is a common source of confusing failures."""
    if platform.system() != "Windows":
        return []
    if "WindowsApps" in sys.executable:
        return [
            "You are using the Windows Store version of Python.",
            "Uninstall it and install Python from python.org, ticking",
            "'Add python.exe to PATH' on the first screen of the installer.",
        ]
    return []


def check_virtual_environment():
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    say("Virtual environment", "active" if in_venv else "NOT active")
    if not in_venv:
        return [
            "No virtual environment is active. If you are on Google Colab this",
            "is expected and you can ignore it. Otherwise, see the activation",
            "step in your setup guide - you will need it from week 2.",
        ]
    return []


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
    cwd = os.getcwd()
    say("Working directory", cwd)
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(cwd) != here:
        return [
            "You are running this from a different folder to the one it lives in.",
            "That is the most common cause of 'file not found' errors.",
            "Try: cd {0}".format(here),
        ]
    return []


def main():
    print(LINE)
    print("PYTHON SETUP CHECK")
    print(LINE)

    say("Operating system", "{0} {1}".format(platform.system(), platform.release()))

    problems = []
    problems += check_python_version()
    problems += check_macos_system_python()
    problems += check_windows_store_python()
    problems += check_virtual_environment()
    problems += check_packages()
    problems += check_working_directory()

    print(LINE)
    if not problems:
        print("ALL CHECKS PASSED.")
        print("Copy everything above and submit it. You are ready for week 1.")
    else:
        print("SOME CHECKS DID NOT PASS.")
        print("")
        for problem in problems:
            print("  " + problem)
        print("")
        print("Copy everything above and submit it. Do not try to fix this alone -")
        print("we will sort it out before the session.")
    print(LINE)


if __name__ == "__main__":
    main()
