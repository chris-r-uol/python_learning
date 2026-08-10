# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, move to a folder in a
terminal, explain what a virtual environment is for, change a value in a script
and see the effect, and read an error message.

## Before the session

Complete the setup guide for your machine (see `setup/`), run `check_setup.py`
from the top of this repository, and submit what it prints. If it fails,
submit the error text — that is just as useful to us.

## In the session

`first_script.py` reads two days of hourly traffic counts and lists the busy
hours. Together we will run it, change it, and break it on purpose.

With your virtual environment active:

```
cd week1_setup
python first_script.py
```

## Homework (about 2 hours)

**1. The traceback safari.** There are six broken scripts in `exercises/`. For
each one: run it, read the error, find the line, and fix it.

```
cd week1_setup/exercises
python check.py
```

`check.py` tells you which scripts are fixed. It does not tell you how to fix
them — that is the exercise. The six errors are six different kinds, and you
will meet every one of them again.

**2. The parameter sweep.** Run `first_script.py` five times, with
`BUSY_THRESHOLD` set to 500, 700, 900, 1100, and 1300. Record the number of
busy hours for each threshold in a small table. Then write two sentences
describing the pattern you see.

## The one thing to take away

When something breaks, read the **last line** of the error message first — it
says what went wrong. Then find the line number — it says where. That is most
of debugging, and after this week you have it.
