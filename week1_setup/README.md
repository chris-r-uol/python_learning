# Week 1 — Getting Python working

**By the end of this week you can:** run a `.py` file, move to a folder in a
terminal, explain what a virtual environment is for, change a value in a
script and see the effect, and read an error message.

The session has three parts. First we cover five ideas — everything else
this week depends on them. Then we work through a real script together. Then
you do the tasks, in class, with the instructor and the TA circulating. This
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

### 4. What the code is actually saying

You are about to read a real script and then fix six broken ones, so you
need to recognise four things when you see them. This section is about
**reading** code, not writing it — week 2 teaches you to write these from
scratch. For now the goal is that nothing in a script looks like
unexplained punctuation.

#### Data, and the two types that matter today

**Data** is simply the values a program works with: a count of vehicles, the
name of a direction, a date. Every value in Python has a **type**, and today
only two matter.

- **Numbers** — `1703`, `8`, `0.5`. You can do arithmetic on them.
- **Text** — `"northbound"`, `"1703"`. Text is called a *string*, and you
  can always spot it by the quotation marks.

The quotation marks are the whole difference between these two lines:

```python
count = 1703      # a number
count = "1703"    # text that happens to look like a number
```

That difference matters more than it sounds, because **a file always gives
you text.** A CSV file is a plain text file, so when a script reads `1703`
out of one, it receives the four characters `1`, `7`, `0`, `3` — not the
number. Text behaves like text:

```python
1703 + 1        # 1704     - numbers add
"1703" + "1"    # "17031"  - text joins end to end
```

So a script must convert before it calculates. `int()` turns text into a
whole number: `int("1703")` gives `1703`. You will see `int(...)` wrapped
around values in almost every script this term, and now you know why it is
there.

Python will not quietly guess for you. If you compare text with a number it
stops and says `TypeError` — which is the loudest, most helpful thing it
could do, and one of the six errors in the tasks.

#### Lists, and counting from zero

A **list** holds several values in order, written in square brackets:

```python
parts = ["2026-03-02", "8", "northbound", "1703"]
```

You reach an item by its position, and **positions start at zero**:

```python
parts[0]     # "2026-03-02"  - the first item
parts[2]     # "northbound"  - the third item
parts[3]     # "1703"        - the fourth and last
```

Zero-based counting feels wrong for about a week. The way to hold on to it
is that the number measures *how far from the start* an item is, and the
first item is zero steps along. A four-item list therefore has positions 0
to 3 — and asking for `parts[4]` gets you `IndexError`, another of the six.

Lists appear constantly because a file is naturally a list of lines, and a
line is naturally a list of comma-separated values.

#### `if` — doing something only sometimes

```python
if count > 900:
    print("busy hour")
```

Read it as written: *if this condition is true, run the indented lines
underneath.* The parts are the word `if`, a condition, a colon, and then an
indented block.

The comparisons you will see are `>`, `<`, `>=`, `<=`, `==` (equal to) and
`!=` (not equal to). Note that **equality is a double `==`**, because a
single `=` already means "store this value under this name".

The indentation is not decoration — it is how Python knows which lines are
inside the `if` and which are not. Lines indented under it run only when the
condition holds; the first line back at the left margin runs either way.
Getting that spacing wrong is `IndentationError`, and it is the one error
that stops the program *before it starts*.

An `if` may be followed by `else`, whose block runs when the condition is
false:

```python
if len(counts) == 0:
    print("no data")
else:
    print(sum(counts) / len(counts))
```

That pattern — check for the empty case before dividing — is how you avoid
`ZeroDivisionError`, which is the sixth error in the tasks.

#### `for` and `while` — doing something repeatedly

A **`for` loop** runs the same block once for each item in a collection:

```python
for line in data_lines:
    print(line)
```

Read it as: *for each item in `data_lines`, one at a time, call it `line`
and run the indented block.* The name `line` is chosen by whoever wrote the
loop; it is refilled on every pass. As with `if`, indentation decides what
is inside the loop.

A **`while` loop** repeats for as long as a condition stays true:

```python
countdown = 3
while countdown > 0:
    print(countdown)
    countdown = countdown - 1
```

The difference in plain words: `for` means *"for each of these things"*, and
`while` means *"keep going until this stops being true"*. Use `for` when you
know what you are working through — a file, a list, the hours of a day —
which is nearly always in data work, and why almost every loop in this
course is a `for`. `while` earns its place when you cannot know in advance
how many repetitions you need. Its one hazard is worth knowing: if the
condition never becomes false, the program runs forever, and you stop it
with **Ctrl-C**.

#### Printing values inside a sentence

Programs constantly need to report a number inside a line of text. Joining
the pieces by hand is awkward, because text and numbers cannot simply be
added together:

```python
print("Total: " + total)      # TypeError - you cannot add a number to text
```

Python's answer is the **f-string**. Put the letter `f` immediately before
the opening quotation mark, and anything you write inside `{curly braces}`
is worked out and dropped into the text:

```python
total = 32083
print(f"Total: {total}")              # Total: 32083
print(f"Half of it is {total / 2}")   # Half of it is 16041.5
```

The `f` stands for *formatted*. Anything can go inside the braces — a name,
a calculation, a function call — and the result is converted to text for
you. You will see this in every script in this course.

There is a second part you will meet in the scripts, after a colon, which
controls the layout rather than the value:

```python
print(f"{count:>8}")      # pad to 8 characters, right-aligned
print(f"{speed:.1f}")     # show 1 decimal place
print(f"{hour:02d}")      # pad a whole number to 2 digits, so 8 becomes 08
```

Those are worth recognising rather than memorising: they are how a script
lines its output up into readable columns. Look them up when you need one.

> You may also see `"Total: {}".format(total)` in older code, which does the
> same job in an older style. One file in this course still uses it —
> `check_setup.py`, deliberately, because f-strings do not work on very old
> versions of Python and that file has to run on them to tell you so.

#### Putting it together

Those four ideas are almost the whole of the script you are about to read: a
`for` loop over the lines of a file, `int()` converting text to numbers,
`parts[...]` pulling values out of a list, and an `if` deciding what counts
as busy. Four of the six errors in the tasks are simply one of these ideas
going wrong.

### 5. How to read an error message

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
you will see this term, and each one points back at an idea from section 4:

| Error | What it means | Idea behind it |
|---|---|---|
| `NameError` | You used a name that has not been defined — often a spelling mistake | Names |
| `TypeError` | You combined two things whose types do not fit — usually text where a number was needed | Data types |
| `IndexError` | You asked a list for a position it does not have | Lists, counting from zero |
| `FileNotFoundError` | The file is not where the program looked — usually a working-directory problem | Paths and the working directory |
| `IndentationError` | The lines do not line up the way Python requires — the program never started | Indented blocks in `if` and `for` |
| `ZeroDivisionError` | Something divided by zero — often an empty input nobody planned for | `if` and the empty case |

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

Do them in this order: the first is a gentle continuation of the
demonstration, and the second is the harder one.

### Task 1 — The parameter sweep

Run `first_script.py` five times, with `BUSY_THRESHOLD` set to 500, 700,
900, 1100, and 1300. Record the number of busy hours for each threshold in a
small table — on paper or in a spreadsheet, either is fine. Then write two
sentences describing the pattern you see.

Nothing here can break: you are changing one number in a script that already
works, which makes it the safest possible place to practise the
edit → run → look loop until it feels automatic.

The point of the task is not the table. It is that changing one number in a
script, re-running it, and observing the result is a complete, legitimate
method of investigation — and after today, it is one you have.

### Task 2 — The traceback safari

Six broken scripts are in `exercises/`. Each contains exactly one of the six
error kinds from the table above — one per row, in no particular order. For
each script: run it, read the error, find the line, fix it.

```
cd week1_setup/exercises
python check.py
```

`check.py` tells you which scripts are fixed. It does not tell you how to fix
them — that is the exercise.

This is the harder task, and it is meant to be. Expect to be stuck at least
once; that is not a sign you are behind. Three things to lean on when you
are: the error table above, which names the idea behind each error; section
4, which explains those ideas; and `first_script.py`, which is a working
example of every one of them. Then the ten-minute rule — try, then ask.

When all six pass, you have met, in miniature, most of the errors you will
see for the rest of the course.

---

## The one thing to take away

When something breaks, read the **last line** of the error message first — it
says what went wrong. Then find the line number — it says where. That is most
of debugging, and after this week you have it.
