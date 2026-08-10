"""
Traceback safari - the marker.

    python check.py

This runs each exercise and tells you whether it is fixed. It does not tell
you how to fix anything - that is the exercise. Read the traceback: the last
line says what went wrong, and the line above it says where.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED = {
    "exercise_1.py": ("ANSWER: 32083", "NameError"),
    "exercise_2.py": ("ANSWER: 1855", "TypeError"),
    "exercise_3.py": ("ANSWER: 48", "IndexError"),
    "exercise_4.py": ("ANSWER: 96", "FileNotFoundError"),
    "exercise_5.py": ("ANSWER: 20", "IndentationError"),
    "exercise_6.py": ("ANSWER: no eastbound data", "ZeroDivisionError"),
}


def run(filename):
    result = subprocess.run(
        [sys.executable, filename],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    print("=" * 64)
    print("TRACEBACK SAFARI")
    print("=" * 64)

    passed = 0
    for filename in sorted(EXPECTED):
        expected_output, expected_error = EXPECTED[filename]
        code, stdout, stderr = run(filename)

        if code == 0 and stdout == expected_output:
            print("  PASS   {0:<16} {1}".format(filename, stdout))
            passed += 1
        elif code == 0:
            print("  WRONG  {0:<16} it runs, but the answer is not right".format(filename))
            print("         got:      {0}".format(stdout or "(nothing printed)"))
            print("         expected: {0}".format(expected_output))
        else:
            last_line = stderr.splitlines()[-1] if stderr else "(no error text)"
            still_original = expected_error in stderr
            label = "STILL BROKEN" if still_original else "NEW ERROR"
            print("  FAIL   {0:<16} {1}".format(filename, label))
            print("         {0}".format(last_line))
        print()

    print("=" * 64)
    print("{0} of {1} fixed.".format(passed, len(EXPECTED)))
    if passed == len(EXPECTED):
        print("All six fixed. You can now read a traceback, and that is most")
        print("of debugging.")
    else:
        print("Keep going. Work on one file at a time, and always read the")
        print("last line of the error first.")
    print("=" * 64)


if __name__ == "__main__":
    main()
