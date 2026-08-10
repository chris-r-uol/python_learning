# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, move to a folder in a
terminal, explain what a virtual environment is for, change a value in a
script and see the effect, and read an error message.

The session has three parts. First we cover four ideas — everything else this
week depends on them. Then we work through a real script together. Then you
do the tasks, in class, with the instructor and the TA circulating. This
document covers all three parts in full, so you can also use it to review, or
to catch up if you missed the session.

**Before the session:** complete the setup guide for your machine (see
`setup/`), run `check_setup.py` from the top of this repository, and submit
what it prints. If it fails, submit the error text instead — that is just as
useful to us.

---

## Part 1 — The ideas

### 1. A program is a text file

A Python program is a plain text file. That is the whole of it. You could
open one in Notepad and read every character. VS Code, the editor you
installed, is a text editor with conveniences added — colouring, underlining
of likely mistakes, a built-in terminal — but the file it saves contains
nothing except the text you typed.

The file does nothing on its own. To make it do something, you hand it to a
second program called the **interpreter** — that is what Python actually is.
When you type `python first_script.py`, you are saying: *run the program
called `python`, and give it my file to work through.* The interpreter reads
your file from the top, carries out each line in turn, and stops when it
reaches the end — or when it hits a line it cannot carry out.

Here is a complete four-line program:

```python
speed_kph = 48
length_m = 1200
seconds = length_m / (speed_kph * 1000 / 3600)
print(seconds)
```

Walk through it the way the interpreter does. Line 1: store the value 48
under the name `speed_kph`. Line 2: store 1200 under `length_m`. Line 3:
convert the speed to metres per second, divide the length by it, and store
the result under `seconds`. Line 4: display the value of `seconds` on the
screen.

That last line matters more than it looks. A program only shows you what you
ask it to show. Without `print`, the interpreter would still compute
`seconds` — correctly — and then finish in silence. When one of your
programs runs and appears to do nothing, this is usually why: it worked, and
nobody asked it to report.

If you are used to spreadsheets, notice one deep difference. A spreadsheet
is *alive*: change one cell, and everything that depends on it recalculates
instantly. A program is not alive. It runs once, from top to bottom, and
finishes. If you change the file, nothing happens until you run it again.
This is why the working method for the whole course is a loop of three
steps — **edit → run → look** — and why "did you re-run it after the
change?" is a serious debugging question, not a joke. Programmers with
twenty years of experience still work in this loop; they have simply become
fast at it.

One consequence of top-to-bottom reading: a name must be given its value
*above* the place it is used. The interpreter does not read ahead. If line 3
mentions `speed_kph` and nothing above line 3 has defined it, the program
stops there with an error, regardless of what line 10 says.

### 2. The terminal, and where you are standing

The terminal is a window where you type commands instead of clicking. It
looks old-fashioned. It has survived because text has two properties that
clicking does not: a command can be *written down exactly* — in a guide like
this one, in your notes, in a report someone else must reproduce — and a
command can be *repeated exactly*. Every piece of professional data work
leans on both.

The mechanics are plain. The terminal shows a *prompt*, which means "type
here". You type one command and press Enter. The computer carries it out,
prints any response, and shows the prompt again. Three commands cover this
course:

| Command | What it does |
|---|---|
| `cd foldername` | Move into a folder ("change directory") |
| `ls` (macOS) / `dir` (Windows) | List what is in the current folder |
| `python script.py` | Run a script with Python |

The idea underneath them is the **working directory**. At every moment, your
terminal is "standing" in exactly one folder — most terminals print its name
as part of the prompt — and every command is interpreted from that position.
`ls` lists *this* folder. `cd data` moves into a folder called `data` *inside
this one*. It is the same idea as having one folder open in File Explorer or
Finder, except that nothing on the screen reminds you visually, so you must
hold the position in your head — or ask, with `ls` or `dir`, which is what
experienced people actually do.

Files are found by their **path** — the file's address. An *absolute* path
gives the address from the very top of the disk:
`C:\Users\you\python_learning\week1_setup\data\site_counts_small.csv`. A
*relative* path gives it from where you are standing:
`data/site_counts_small.csv`, meaning "the folder `data`, right here, and
the file inside it". Scripts almost always use relative paths, because the
project may be copied to another machine where the absolute address would be
wrong — but a relative path only works if you are standing in the right
place when you run the script.

That single fact explains the most common error of week 1. When a script
says `open("data/site_counts_small.csv")` and you see `FileNotFoundError`,
the file almost always exists. The problem is your position: Python looked
for a `data` folder inside the folder your terminal was standing in, did not
find one, and reported the full path it tried. Read that path, run `ls` or
`dir` to see where you actually are, `cd` to the right place, and run the
script again.

Finally, take apart the command you will type most: `python first_script.py`.
The first word names the program to run — the Python interpreter. The second
is handed to that program as its input — the path to your file, relative to
where you stand. Two words, both of them now meaningful.

### 3. Virtual environments

When your code says `import numpy`, it is asking to use a **library** — a
collection of code written by someone else and published for reuse. NumPy
does not come with Python; before your machine can import it, it must be
*installed*, which means downloaded from a public archive and saved into
your Python's folders. The installing tool is called `pip`, and you used it
in the setup guide: `pip install -r requirements.txt` means "install
everything named in this list".

Now the problem. Suppose everything you install lands in the one Python on
your machine. This term, project A needs version 1 of some library. Next
year, project B needs version 2, so you upgrade — and project A quietly
breaks, and you find out months later, when you reopen it the night before
you need it. One shared Python means every project can damage every other.
This is not a rare misfortune; it is the natural fate of any machine used
for real work over several years.

A **virtual environment** removes the problem by giving each project its own
private Python. Concretely, it is nothing more than a folder — ours is
called `.venv`, sitting inside the project — containing a copy of the
interpreter and its own separately installed libraries. **Activation**, the
step you do each session, tells your current terminal window: *while this
window is open, when I say `python`, use the one in this project's `.venv`.*
Nothing outside the window, and nothing outside the project, is affected.

Two practical consequences. First, activation is per terminal window: a new
window knows nothing about it, which is why the `(.venv)` marker in your
prompt is worth glancing at before you run anything. Second, an environment
is cheap and disposable. If one ever breaks or confuses you, delete the
`.venv` folder and rebuild it — create, activate, install, three commands
from the setup guide, two minutes. Nothing of value lives inside it; your
code and data live outside. You never need to be afraid of it.

### 4. How to read an error message

When a program fails, Python prints a report called a **traceback**. It
looks alarming, and most beginners' instinct is to look away and re-read
their code. Resist that. The traceback is the most informative thing on the
screen, and it is written for you — the name means it *traces back* from the
failure to show where the program was when it stopped.

```
Traceback (most recent call last):
  File "first_script.py", line 61, in <module>
    count = int(parts[9])
IndexError: list index out of range
```

Read it in this order. **Last line first**: the kind of error
(`IndexError`) and a plain description (`list index out of range` — you
asked a list for a position it does not have). Then the line above: the file
and the **line number** where execution stopped, with the offending line
printed underneath. What went wrong, and where. With those two facts you can
go to line 61 and look at it with a specific question in mind, instead of
re-reading the whole file with a vague sense of dread.

Two further things sharpen the diagnosis. First, an error stops the program
at that line: everything *above* it ran; nothing *below* it did. If your
script printed three things and then failed, those three prints are
evidence about what was true just before the failure. Second, there are two
moments an error can happen, and they mean different things. Most errors
happen *while the program runs*, at the line reported. But Python reads your
whole file before starting, to check that it is well-formed — and a file
that is not well-formed fails *before any line runs at all*. `SyntaxError`
and `IndentationError` are this second kind: the program never started, so
there is no point looking at what it printed, because it printed nothing.
You will meet exactly this in the tasks.

The kind of error is itself information. Six kinds cover almost everything
you will see this term:

| Error | What it means |
|---|---|
| `NameError` | You used a name that has not been defined — often a spelling mistake |
| `TypeError` | You combined two things whose types do not fit — often text where a number was needed |
| `IndexError` | You asked a list for a position it does not have |
| `FileNotFoundError` | The file is not where the program looked — usually a working-directory problem |
| `IndentationError` | The lines do not line up the way Python requires — the program never started |
| `ZeroDivisionError` | Something divided by zero — often an empty input nobody planned for |

You do not need to memorise the table. You need to know it exists, and to
read the last line of every traceback before doing anything else. One more
thing, said once because it matters: an error message is not an accusation
and not a grade. It is the machine reporting, precisely and without any
opinion of you, the exact place it could not continue. People who progress
fastest in this course are not the ones who make fewer errors; they are the
ones who read them.

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
