# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, move to a folder in a
terminal, say what a virtual environment is for, change a value in a script
and see the effect, and read an error message.

The session has three parts. First the ideas. Then a script we work through
together. Then the tasks, which you do in class.

This page contains all three parts. Use it to review, or to catch up if you
missed the session.

**Before the session:** follow the setup guide for your machine in `setup/`.
Then run `check_setup.py` and read what it prints. If it reports a problem,
it also names the fix.

---

## Part 1 — The ideas

### 1. A program is a text file

A Python program is a plain text file. You could open it in Notepad and read
every character. VS Code adds colour and other helpers, but the file it
saves contains only the text you typed.

The file does nothing by itself. To run it, you give it to a program called
the **interpreter**. That is what Python is. When you type
`python first_script.py`, you are saying: run the program called `python`,
and give it my file.

The interpreter reads your file from the top. It carries out each line in
order. It stops at the end, or at the first line it cannot carry out.

Here is a complete program:

```python
speed_kph = 48
length_m = 1200
seconds = length_m / (speed_kph * 1000 / 3600)
print(seconds)
```

Read it the way Python does:

- Line 1 stores the value 48 under the name `speed_kph`.
- Line 2 stores 1200 under `length_m`.
- Line 3 converts the speed to metres per second, divides, and stores the
  result under `seconds`.
- Line 4 displays `seconds` on screen.

The last line matters. A program only shows what you tell it to show.
Without `print`, Python calculates `seconds` and then stops. Nothing
appears. If your program runs and shows nothing, this is often the reason.

A spreadsheet updates itself. Change one cell and every formula recalculates
at once. A program does not do this. It runs once, top to bottom, then
stops. If you change the file, nothing happens until you run it again.

So the working method is three steps: **edit, run, look**. Change one thing.
Run it. Look at what changed.

One more rule. A name must be given a value **above** the line that uses it.
Python does not read ahead. If line 3 uses `speed_kph` and no line above
defines it, the program stops at line 3.

### 2. The terminal, and where you are

The terminal is a window where you type commands instead of clicking.

You type one command and press Enter. The computer carries it out, prints
any response, and waits for the next one.

Three commands cover this course:

| Command | What it does |
|---|---|
| `cd foldername` | Move into a folder |
| `ls` (macOS) / `dir` (Windows) | List what is in this folder |
| `python script.py` | Run a script |

The idea behind them is the **working directory**. Your terminal is always
in exactly one folder. Every command works from that folder. `ls` lists
*this* folder. `cd data` moves into a folder called `data` *inside this
one*.

It is like having one folder open in File Explorer or Finder. The difference
is that nothing on screen shows you where you are, so you check with `ls` or
`dir`.

Files have a **path**, which is the file's address. There are two kinds:

- An **absolute path** starts from the top of the disk:
  `C:\Users\you\python_learning\week1_setup\data\site_counts_small.csv`
- A **relative path** starts from where you are:
  `data/site_counts_small.csv`. This means "the folder `data`, here, and the
  file inside it".

Scripts use relative paths, so the project still works when it is copied to
another machine. But a relative path only works if you are in the right
folder when you run the script.

This explains the most common error of week 1. A script says
`open("data/site_counts_small.csv")` and you get `FileNotFoundError`. The
file exists. You are in the wrong folder. Python looked for a `data` folder
inside your current folder and did not find one.

To fix it: read the path in the error, run `ls` or `dir` to see where you
are, `cd` to the right folder, and run the script again.

Now look again at the command you will type most: `python first_script.py`.
The first word is the program to run. The second is the file you give it.

### 3. Virtual environments

When your code says `import numpy`, it asks to use a **library**. A library
is code written by someone else. NumPy does not come with Python. It must be
**installed** first, which means downloaded and saved into your Python's
folders. The tool that installs it is called `pip`. You used it in the setup
guide: `pip install -r requirements.txt` installs everything in that list.

Here is the problem it creates. Suppose everything installs into the one
Python on your machine. This year, project A needs version 1 of a library.
Next year, project B needs version 2, so you upgrade. Project A now breaks,
and you find out months later.

A **virtual environment** solves this. Each project gets its own private
Python. It is a folder, called `.venv`, inside the project. It holds a copy
of the interpreter and its own libraries.

**Activation** tells your terminal: while this window is open, `python`
means the one in this project's `.venv`. Nothing outside the window changes.

Two things follow:

- Activation applies to one terminal window. A new window needs the command
  again. Check for `(.venv)` in your prompt before you run anything.
- An environment is disposable. If one breaks, delete the `.venv` folder and
  build it again: create, activate, install. Your code and data are outside
  it, so you lose nothing.

### 4. What the code is saying

You are about to read a real script, then fix six broken ones. This section
covers what you need to recognise. It is about **reading** code. Week 2
covers writing it.

#### Data and types

**Data** means the values a program works with: a count, a name, a date.

Every value has a **type**. Two types matter now:

- **Numbers**: `1703`, `8`, `0.5`. You can do arithmetic on them.
- **Text**: `"northbound"`, `"1703"`. Text is called a *string*. You can
  always spot it by the quotation marks.

The quotation marks are the only difference here:

```python
count = 1703      # a number
count = "1703"    # text
```

This matters because **a file always gives you text**. A CSV file is a text
file. When a script reads `1703` from one, it gets four characters, not a
number. Text behaves differently:

```python
1703 + 1        # 1704     numbers add
"1703" + "1"    # "17031"  text joins together
```

So a script must convert text before it calculates. `int()` turns text into
a whole number. `int("1703")` gives `1703`. You will see `int(...)` in
almost every script this term.

Python does not guess. If you compare text with a number, it stops and says
`TypeError`.

#### Lists, counting from zero

A **list** holds several values in order. It is written in square brackets:

```python
parts = ["2026-03-02", "8", "northbound", "1703"]
```

You reach an item by its position. **Positions start at zero:**

```python
parts[0]     # "2026-03-02"   the first item
parts[2]     # "northbound"   the third item
parts[3]     # "1703"         the fourth item
```

A list of four items has positions 0 to 3. Asking for `parts[4]` gives
`IndexError`.

Counting from zero feels wrong at first. The number means how far the item
is from the start. The first item is zero steps from the start.

#### `if` — doing something only sometimes

```python
if count > 900:
    print("busy hour")
```

This means: if the condition is true, run the indented lines below it.

The parts are the word `if`, a condition, a colon, then indented lines.

Conditions use `>`, `<`, `>=`, `<=`, `==` (equal to) and `!=` (not equal
to). Equality uses **two** equals signs, because one equals sign already
means "store this value".

The indentation is not decoration. It tells Python which lines are inside
the `if`. Lines that are indented run only when the condition is true. The
first line back at the left margin runs either way. Wrong indentation gives
`IndentationError`.

`if` can have a partner, `else`. Its lines run when the condition is false:

```python
if len(counts) == 0:
    print("no data")
else:
    print(sum(counts) / len(counts))
```

Checking for an empty list before dividing avoids `ZeroDivisionError`.

#### `for` and `while` — doing something many times

A **`for` loop** runs the same lines once for each item:

```python
for line in data_lines:
    print(line)
```

This means: take each item in `data_lines`, one at a time, call it `line`,
and run the indented lines. The name `line` is chosen by whoever wrote the
loop. Indentation decides what is inside the loop.

A **`while` loop** repeats while a condition stays true:

```python
countdown = 3
while countdown > 0:
    print(countdown)
    countdown = countdown - 1
```

`for` means "for each of these things". `while` means "keep going until this
stops being true".

Use `for` when you know what you are working through: a file, a list, the
hours of a day. That is almost always the case in data work, and almost
every loop in this course is a `for` loop.

`while` has one danger. If the condition never becomes false, the program
runs forever. Press **Ctrl-C** to stop it.

#### Putting values inside text

Programs often print a number inside a sentence. You cannot add text and
numbers together:

```python
print("Total: " + total)      # TypeError
```

Use an **f-string** instead. Put `f` before the quotation mark. Anything
inside `{curly braces}` is worked out and placed in the text:

```python
total = 32083
print(f"Total: {total}")              # Total: 32083
print(f"Half is {total / 2}")         # Half is 16041.5
```

The `f` means "formatted". You will see f-strings in every script here.

After a colon you can control the layout:

```python
print(f"{count:>8}")      # pad to 8 characters, right-aligned
print(f"{speed:.1f}")     # one decimal place
print(f"{hour:02d}")      # pad to two digits, so 8 becomes 08
```

Recognise these when you see them. Look them up when you need one.

> Older code uses `"Total: {}".format(total)` instead. It does the same job.
> One file here still uses it: `check_setup.py`. F-strings do not work on
> very old versions of Python, and that file must run on them.

#### Together

Those ideas make up most of the script you are about to read: a `for` loop
over the lines of a file, `int()` to convert text to numbers, `parts[...]`
to take values out of a list, and `if` to decide what counts as busy.

### 5. How to read an error message

When a program fails, Python prints a **traceback**. It looks alarming. It
is the most useful thing on your screen.

```
Traceback (most recent call last):
  File "first_script.py", line 61, in <module>
    count = int(parts[9])
IndexError: list index out of range
```

Read it in this order:

1. **The last line.** It gives the kind of error (`IndexError`) and a
   description (`list index out of range`).
2. **The line above it.** It gives the file and the **line number** where
   the program stopped, and prints that line.

Now you know what went wrong and where. Go to that line and look at it.

Two more things help.

**An error stops the program at that line.** Everything above it ran.
Nothing below it ran. If your script printed three lines and then failed,
those three lines are evidence.

**Some errors happen before the program starts.** Python reads the whole
file first to check it is well formed. `SyntaxError` and `IndentationError`
happen at this stage. The program never started, so it printed nothing.

Six kinds of error cover almost everything this term:

| Error | Meaning | Idea behind it |
|---|---|---|
| `NameError` | A name that was never defined. Often a spelling mistake | Names |
| `TypeError` | Two types that do not fit. Usually text where a number was needed | Data types |
| `IndexError` | You asked a list for a position it does not have | Lists, counting from zero |
| `FileNotFoundError` | The file is not where the program looked. Usually the wrong folder | Paths |
| `IndentationError` | Lines do not line up. The program never started | Indented blocks |
| `ZeroDivisionError` | Something divided by zero. Often an empty input | `if` and the empty case |

You do not need to memorise this table. Read the last line of the traceback
first, every time.

---

## Part 2 — The script: `first_script.py`

We work through this together. It reads two days of hourly traffic counts
and lists the busy hours.

With your virtual environment active:

```
cd week1_setup
python first_script.py
```

The steps:

1. **Read the script from top to bottom before running it.** Every line has
   a comment. Predict what it will print.
2. **Run it.** Compare the output with your prediction.
3. **Change `BUSY_THRESHOLD` to 500.** Run it again.
4. **Change `DIRECTION` to `"southbound"`.** Does the busiest hour move?
5. **Break it three ways.** The suggestions are at the bottom of the script.
   Read each traceback: last line first, then the line number. Put the code
   back afterwards.

Breaking a program on purpose, where nothing matters, is the fastest way to
get used to error messages.

---

## Part 3 — The tasks

You do these in class. Try something for ten minutes, then ask. The
instructor and the TA are there for this.

Finish anything unfinished before next week.

### Task 1 — The parameter sweep

Run `first_script.py` five times. Set `BUSY_THRESHOLD` to 500, 700, 900,
1100 and 1300.

Record the number of busy hours for each threshold in a small table. Use
paper or a spreadsheet. Then write two sentences describing the pattern.

Nothing can break here. You are changing one number in a script that already
works.

### Task 2 — The traceback safari

There are six broken scripts in `exercises/`. Each one contains one of the
six error kinds from the table above.

For each script: run it, read the error, find the line, fix it.

```
cd week1_setup/exercises
python check.py
```

`check.py` tells you which scripts are fixed. It does not tell you how to
fix them.

This task is harder than task 1. Expect to be stuck at least once. Three
things help:

- the error table above, which names the idea behind each error
- section 4, which explains those ideas
- `first_script.py`, which is a working example of all of them

The fixed versions are in `instructor/solutions/week1/`. Nothing is graded,
so nobody loses marks by reading them. Use them to check your work after you
have tried, or when you are stuck. If you read them first, you get no
practice.

---

## The main point of this week

When something breaks, read the **last line** of the error first. It says
what went wrong. Then find the line number. It says where.
