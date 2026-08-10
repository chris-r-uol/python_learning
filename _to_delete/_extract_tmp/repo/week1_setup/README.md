# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, navigate to a folder in a
terminal, say what a virtual environment is for, change a value in a script and
see the effect, and read a traceback.

## Before the session

Do the setup guide for your machine (see `setup/`), then run `check_setup.py`
from the top of this repo and submit what it prints. If it fails, submit the
error text — that is just as useful.

## In the session

`first_script.py` — reads two days of hourly counts and lists the busy hours.
We run it, change it, and break it on purpose.

```
cd week1_setup
python first_script.py
```

## Homework (~2h)

**1. Traceback safari.** Six broken scripts in `exercises/`. For each one: run it,
read the error, find the line, fix it.

```
cd week1_setup/exercises
python check.py
```

`check.py` tells you which are fixed. It does not tell you how to fix them. The
six errors are six different kinds, and you will meet all of them again.

**2. Parameter sweep.** Run `first_script.py` with `BUSY_THRESHOLD` set to 500,
700, 900, 1100 and 1300. Record the number of busy hours in a table. Write two
sentences on the pattern.

## The one thing to take away

When something breaks, read the **last line** of the error first — it says what
went wrong. Then the line number — it says where. That is most of debugging, and
you now have it.
