# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, move to a folder in a
terminal, explain what a virtual environment is for, change a value in a
script and see the effect, and read an error message.

The session has three parts. First we cover four ideas — they are short, and
everything else this week depends on them. Then we work through a real script
together. Then you do the tasks, in class, with the instructor and the TA
circulating. This document covers all three parts, so you can also use it to
review, or to catch up if you missed the session.

**Before the session:** complete the setup guide for your machine (see
`setup/`), run `check_setup.py` from the top of this repository, and submit
what it prints. If it fails, submit the error text instead — that is just as
useful to us.

---

## Part 1 — The ideas

### 1. A program is a text file

A Python program is a plain text file containing instructions. When you run
it, a program called the *interpreter* reads your file from the top to the
bottom, one line at a time, and carries out each instruction in order. There
is nothing hidden: everything the program will do is written in the file, in
the order it will happen.

Here is a complete four-line program:

```python
speed_kph = 48
length_m = 1200
seconds = length_m / (speed_kph * 1000 / 3600)
print(seconds)
```

The first two lines store values under names. The third calculates a new
value from them. The fourth prints the result to the screen — without that
line, the program would calculate the answer and then end silently.

The working method for this whole course is a loop with three steps:
**edit → run → look.** Change one thing, run the program, look carefully at
what changed. Programmers with twenty years of experience still work this
way; they have simply become faster at the loop.

### 2. The terminal, and where you are standing

The terminal is a window where you type commands instead of clicking. You
need very little of it — three commands cover this course:

| Command | What it does |
|---|---|
| `cd foldername` | Move into a folder ("change directory") |
| `ls` (macOS) / `dir` (Windows) | List what is in the current folder |
| `python script.py` | Run a script with Python |

The important idea behind these commands is the **working directory**. At any
moment, your terminal is "standing" in exactly one folder, and every command
you type is interpreted from that position. When a script says
`open("data/site_counts_small.csv")`, Python does not search your computer
for that file — it looks for a folder called `data` *inside the folder your
terminal is standing in*, and nowhere else.

This explains the most common error of week 1. If you see
`FileNotFoundError`, the file almost always exists — you are standing in the
wrong folder. Check with `ls` or `dir`, move with `cd`, and run again.

### 3. Virtual environments

Imagine two projects on one machine. Project A needs version 1 of a library;
project B needs version 2. If both projects share one Python, they cannot
both work. This is not a rare situation — it is the normal condition of any
machine used for real work.

A **virtual environment** solves it: a private copy of Python that belongs to
one project, with its own installed libraries that cannot interfere with
anything else. You met the three commands in the setup guide:

1. Create it, once per project: `python -m venv .venv`
2. Activate it, once per terminal session — the command differs by operating
   system; it is in your setup guide.
3. Install into it: `pip install -r requirements.txt`

The one people forget is activation. It applies to the terminal window you
ran it in, and to nothing else. New window, new activation. If your prompt
does not show `(.venv)`, you are not in the environment.

### 4. How to read an error message

When a program fails, Python prints a report called a **traceback**. It looks
alarming. It is actually the most helpful thing on your screen, if you read
it in the right order:

```
Traceback (most recent call last):
  File "first_script.py", line 61, in <module>
    count = int(parts[9])
IndexError: list index out of range
```

Read the **last line first**. It has two parts: the kind of error
(`IndexError`) and a description (`list index out of range`). Then read the
line above it: the file name and the **line number** where the failure
happened, with the failing line printed underneath. What went wrong, and
where. That is most of debugging.

The kind of error is itself information. Six kinds cover almost everything
you will meet this term:

| Error | What it means |
|---|---|
| `NameError` | You used a name that has not been defined — often a spelling mistake |
| `TypeError` | You combined two things whose types do not fit — often text where a number was needed |
| `IndexError` | You asked a list for a position it does not have |
| `FileNotFoundError` | The file is not where the program looked — usually a working-directory problem |
| `IndentationError` | The lines are not lined up the way Python requires |
| `ZeroDivisionError` | Something divided by zero — often an empty input nobody planned for |

You do not need to memorise this table. You need to know it exists, and to
read the last line of every traceback before doing anything else.

---

## Part 2 — Demonstration: `first_script.py`

We do this together. The script reads two days of hourly traffic counts and
reports which hours were busy. With your virtual environment active:

```
cd week1_setup
python first_script.py
```

The sequence, which you can also follow on your own:

1. **Read the script from top to bottom before running it.** Every line has a
   comment. Predict what it will print.
2. **Run it.** Compare what you predicted with what appeared.
3. **Change something.** Set `BUSY_THRESHOLD` to 500 and run again. The
   edit → run → look loop, in its natural habitat.
4. **Change something else.** Set `DIRECTION` to `"southbound"`. Does the
   busiest hour move?
5. **Break it, on purpose, three ways** — the suggestions are at the bottom
   of the script. Each produces a different traceback. Read each one: last
   line first, then the line number. Put the code back afterwards.

Breaking a program deliberately, in a place where nothing matters, is the
fastest way to lose your fear of error messages. That fear is the main thing
standing between a beginner and progress.

---

## Part 3 — The tasks

You do these in class, under supervision. The instructor and the TA are
there to be used: a good rule is to try something yourself for ten minutes,
and then ask. Both halves of the rule matter — the trying and the asking.
Anything unfinished at the end of the session, finish before next week.

### Task 1 — The traceback safari

Six broken scripts are in `exercises/`. Each contains exactly one of the six
error kinds from the table above. For each script: run it, read the error,
find the line, fix it.

```
cd week1_setup/exercises
python check.py
```

`check.py` tells you which scripts are fixed. It does not tell you how to fix
them — that is the exercise. When all six pass, you have met, in miniature,
most of the errors you will see for the rest of the course.

### Task 2 — The parameter sweep

Run `first_script.py` five times, with `BUSY_THRESHOLD` set to 500, 700,
900, 1100, and 1300. Record the number of busy hours for each threshold in a
small table — on paper or in a spreadsheet, either is fine. Then write two
sentences describing the pattern you see.

The point of the task is not the table. It is that changing one number in a
script, re-running it, and observing the result is a complete, legitimate
method of investigation — and after today, it is one you have.

---

## The one thing to take away

When something breaks, read the **last line** of the error message first — it
says what went wrong. Then find the line number — it says where. That is most
of debugging, and after this week you have it.
