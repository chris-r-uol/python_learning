# Week 2 — Actually programming

**By the end of this week you can:** use variables and lists, write a loop
with a conditional inside it, put repeated work into a function, do
arithmetic on a NumPy array, and produce a labelled figure.

The session has three parts. First the six ideas. Then we build a real
analysis together. Then the tasks, which you do in class.

Everything this week answers one question: *what does an average day look
like at this traffic count site, and when is the peak?* That is the shape of
most analysis work. Take a file of records, keep the ones you want,
summarise them, show the result.

---

## Part 1 — The ideas

### 1. Store — variables and types

A variable is a name with a value attached:

```python
count = 1703
```

Python works out the right-hand side first, then stores the result under the
name on the left. After that, `count` means that value.

The `=` sign does not mean what it means in mathematics. In mathematics
`x = x + 1` is impossible. In Python this is normal:

```python
count = count + 1
```

Read it right side first: take the value in `count`, add one, store the
result back in `count`. The `=` sign is an instruction, not a statement of
fact.

You choose the names. Python allows letters, digits and underscores, and the
name cannot start with a digit. Choose names a reader can understand.
`northbound_total` is better than `nt`.

Every value has a **type**. The two you meet most are numbers and text. Text
is called a *string*. The same-looking value behaves differently depending
on its type:

```python
1703 + 1        # 1704       numbers add
"1703" + "1"    # "17031"    text joins together
9 > 1000        # False      numbers compare by size
"9" > "1000"    # True       text compares letter by letter
```

The last line surprises people. Text is ordered like a dictionary. `"9"`
comes after `"1000"` because the character `9` comes after the character
`1`. Nothing else is checked. So text that looks like numbers **sorts
wrongly and compares wrongly**, while looking normal when printed.

This matters because **files give you text**. A CSV file is a text file.
Every value you read from one arrives as text, however numeric it looks.
Converting is your job:

- `int("1703")` gives the whole number 1703
- `float("3.1")` gives the decimal 3.1

Excel guesses types for you. Sometimes it guesses wrong, which is why
geneticists renamed some human genes that Excel kept reading as dates.
Python never guesses. If you compare text with a number it stops with
`TypeError`.

### 2. Decide — `if`

```python
if count > 900:
    print("busy hour")
    busy_hours = busy_hours + 1
```

The parts are: the word `if`, a condition, a colon, then indented lines.

The indentation tells Python which lines belong to the `if`. Indented lines
run only when the condition is true. The first line back at the left margin
runs either way.

The condition gives one of two values, `True` or `False`. Build conditions
with `>`, `<`, `>=`, `<=`, `==` (equal to) and `!=` (not equal to).
Equality uses **two** equals signs, because one equals sign stores a value.

`if` can have a partner, `else`, whose lines run when the condition is
false. A chain uses `elif`, short for "else if":

```python
if ratio < 0.7:
    band = "free flow"
elif ratio < 0.9:
    band = "busy"
else:
    band = "at capacity or worse"
```

**Decide your boundaries on purpose.** Is a ratio of exactly 0.9 "busy" or
"at capacity"? `ratio < 0.9` puts 0.9 in the upper band. `ratio <= 0.9` puts
it in the lower one. Python will do either. Choosing is your job, and you
must be able to say which you chose. One drill is built on this.

### 3. Repeat — lists and loops

A list holds several values in order:

```python
counts = [52, 22, 24, 29]
```

**Positions start at zero.** `counts[0]` is 52. `counts[3]` is 29, the last
item. `counts[4]` gives `IndexError`. `len(counts)` gives the length, 4.

The position number means how far the item is from the start. The first item
is zero steps from the start.

**Taking a run of items.** Square brackets with a colon give you a section
of a list:

```python
counts[1:3]     # [22, 24]        from position 1, up to but not including 3
counts[1:]      # [22, 24, 29]    from position 1 to the end
counts[:2]      # [52, 22]        from the start to position 2
```

The first number is included. The second is not. So `counts[1:3]` gives two
items. For positions 7 to 9 including 9, write `counts[7:10]`.

This is what `lines[1:]` means in last week's script: everything except the
first line.

**Making a list of repeated values.** Multiplying a list repeats it:

```python
[0] * 24        # a list of twenty-four zeros
```

**A `for` loop** runs the same lines once for each item:

```python
total = 0
for count in counts:
    total = total + count
```

The middle line means: take each value in `counts`, one at a time, call it
`count`, and run the indented lines. You choose the name `count`.

Those three lines contain the most useful pattern in data work: the
**accumulator**. Start with an empty total. Add each item as it passes.
Follow it one pass at a time:

| pass | `count` | `total` afterwards |
|---|---|---|
| 1 | 52 | 52 |
| 2 | 22 | 74 |
| 3 | 24 | 98 |
| 4 | 29 | 127 |

Tracing a loop like this, with a column per variable and a row per pass, is
a normal way to find a problem. Three hand-traced passes usually beat an
hour of reading.

The same shape with an `if` inside gives the second pattern: **build a new
list of the items that qualify**. Start with an empty list. Add each item
that passes the test.

A list is like a spreadsheet column. A loop is what "fill this formula down
the column" does. Python makes the repetition visible and lets you control
it.

#### The second way to write a loop: over positions

The loops above go over *items*. There is a second form that goes over
*positions*. The worked example uses it throughout.

`range` produces a run of whole numbers:

```python
range(24)          # 0, 1, 2 ... 23      twenty-four numbers, starting at 0
range(7, 10)       # 7, 8, 9             starts at 7, stops before 10
range(0, 24, 2)    # 0, 2, 4 ... 22      every second number
```

`range(24)` stops **before** 24, in the same way that slicing stops before
its second number. Python is consistent about this.

Put a `range` in a `for` loop and the variable holds a position:

```python
for hour_of_day in range(24):        # 0, then 1, then 2 ...
    print(hour_of_day)
```

These two loops do the same thing:

```python
for count in counts:                 # over items
    total = total + count

for index in range(len(counts)):     # over positions
    total = total + counts[index]
```

The second is longer. Use it when you need the position:

- **The position is the answer.** "Which hour was busiest?" asks for a
  position.
- **You must walk two lists together.** If `hours[i]` and `counts[i]`
  describe the same row of a file, one index reaches into both. The worked
  example does this, because it reads the file into four lists.
- **There is no list.** `range(24)` covers the hours of a day whether or not
  a list of that length exists.

`range(len(counts))` looks odd at first. Take it in two steps. `len(counts)`
is 4. So `range(len(counts))` is `range(4)`, which gives 0, 1, 2, 3. Those
are every valid position, and never one past the end. It stays correct if
the list changes length.

**Use the item form when you can. Use the position form when you must.**

#### Rows that hold several values

Data often arrives as pairs or rows:

```python
rows = [(8, 100), (8, 50), (17, 90)]     # (hour, count) pairs
```

Round brackets make a **tuple**. For our purposes it behaves like a list you
do not change. `rows[0]` is the pair `(8, 100)`. `rows[0][0]` is `8`.

You can reach the parts by position:

```python
for row in rows:
    hour = row[0]
    count = row[1]
```

Or name them in the `for` line, which does the same thing:

```python
for hour, count in rows:
    ...
```

This is called **unpacking**. Last week's `first_script.py` ends with
`for date, hour, count in busy_hours:`, which does exactly this. Use
whichever form you find clearer.

### 4. Package — functions

When the same block of code appears twice, people copy it and change one
word. The copies then drift apart. Someone fixes one and not the other. The
two versions give different answers, and nothing warns you.

A **function** gives the block a name, so there is only one copy:

```python
def hourly_average(direction):
    ...
    return result
```

`def` starts the function. `hourly_average` is its name. `direction` is a
**parameter**, a placeholder for the value that changes. The indented lines
are the work. `return` says what comes back.

Defining a function runs nothing. You **call** it later:

```python
northbound = hourly_average("northbound")
southbound = hourly_average("southbound")
```

Follow the first call. The value `"northbound"` goes in and becomes
`direction` for this run. The lines run. `return result` sends the answer
back. The call itself becomes that answer, which is then stored in
`northbound`.

**When there is no answer: `None`.** Sometimes a function is asked for
something that does not exist, such as the average of an empty list.
Returning `0` would be wrong, because zero is a real average. Python has a
value for "no value at all": `None`.

```python
def average(values):
    if len(values) == 0:
        return None
    ...
```

`None` is not zero and not empty text. Arithmetic on it fails at once with
`TypeError`, so a missing answer cannot be mistaken for a real one. Test for
it with `is None`:

```python
if average(counts) is None:
    print("no data")
```

Decide what your function does with no data. One drill is built on this.

Two more points.

**`return` is not `print`.** A printed value appears on screen and is gone.
You cannot add it, compare it or plot it. A returned value comes back into
the program, where you can store and use it. Print is for people. Return is
for the rest of your code.

**Names inside a function exist only while it runs.** The parameters and
anything defined in the body disappear afterwards. Values go in through the
parameters and come out through `return`.

### 5. NumPy — arithmetic on many values at once

NumPy is a **library**. It was installed during setup. Bring it into a
script with:

```python
import numpy as np
```

`np` is the usual short name for it.

Its main object is the **array**. An array is like a list, with one
restriction and one advantage. The restriction: every item has the same
type. The advantage: arithmetic applies to the whole array at once.

```python
counts = np.array([900, 1800, 2700])
counts / 1800          # array([0.5, 1.0, 1.5])
```

One line, no loop. You say what should happen to every item.

Comparisons work the same way. They give an array of `True` and `False`
values, called a **mask**:

```python
directions == "northbound"   # array([True, False, True, ...])
```

A mask selects items. `counts[mask]` keeps the items in the `True`
positions. So filtering becomes two lines: build the mask, apply it.
Combine masks with `&` (and) and `|` (or), with brackets around each
comparison.

Nothing new is happening. When you write `counts.mean()`, a loop runs inside
the library, in a faster language. You write the loop by hand first so you
can explain the one-line version.

### 6. The figure

Most analysis ends in a figure. The standard tool is matplotlib.

It has two objects: the **figure**, which is the page, and the **axes**,
which is the plotting area. You get both from one call. Each later call adds
or sets one thing. Nothing appears until you save:

```python
figure, axes = plt.subplots()
axes.plot(hours, flows)            # the data
axes.set_xlabel("Hour of day")
axes.set_ylabel("Average flow (vehicles per hour)")
axes.set_title("Average hourly flow, site A34/012, 2-15 March 2026")
figure.savefig("profile.png")
```

Six calls, one finished figure, saved to a file you can put in a report.
Everything else matplotlib offers is more calls of the same shape.

A finished figure has:

- both axes labelled, **with units**
- a title giving the place and the period
- a legend when there is more than one line
- a size where the text is readable

**A figure with an unlabelled axis is not finished.** A figure gets pasted
into slides, cropped into reports and sent in emails. It arrives without you
and without your explanation. A reader a year from now decides something
from the figure alone.

---

## Part 2 — The worked example

We build `worked_example.py` together, in six stages. Each stage uses one
idea above.

With your virtual environment active:

```
cd week2_programming
python worked_example.py
```

| Stage | What it does | Idea |
|---|---|---|
| 1 | Read the CSV into four lists | Store |
| 2 | Keep only one direction | Decide |
| 3 | Average each hour of the day, the long way | Repeat |
| 4 | Turn the block into a function, then run it for both directions | Package |
| 5 | Do the same calculation in NumPy and check the answers match | NumPy |
| 6 | Draw the figure, label it, save it | The figure |

Two things in the file are worth noticing.

At the end of stage 4 there is an `assert` line. It checks stage 4 against
stage 3: the same answer, calculated two ways, compared automatically.

Stage 5 prints a standard deviation at the peak hour that is larger than you
might expect. It is not a mistake. Task 2 shows the reason.

---

## Part 3 — The tasks

You do these in class. Try something for ten minutes, then ask. The
instructor and the TA are there for this.

Finish anything unfinished before next week.

### Task 1 — The drills

Twelve short exercises, one per idea, getting harder as they go. They work
like last week's traceback safari: **one file each**, from `drill_01.py` to
`drill_12.py`, with a `check.py` that marks them.

Open a drill file. It contains one function with a `TODO` where the body
should be. The docstring says what the function must do, gives example
inputs and outputs, and names the idea from Part 1.

Fill in the body, save, and run:

```
cd week2_programming/drills
python check.py
```

`check.py` reports each drill as:

- `PASS` — correct
- `TODO` — it runs, but the answer is not right yet
- `ERROR` — it raised an error
- `BROKEN` — the file does not start, usually because of indentation

It does not tell you how to fix anything.

The drills do not depend on each other. Work on one file at a time. If one
is fighting you, move to the next and come back.

Aim to finish the nine unstarred drills. The three marked with a star are
harder and optional.

You are not expected to know any of this from memory. Look things up. Reread
Part 1. Reread the worked example. Ask the person next to you. Ask the TA.

The answers are in `instructor/solutions/week2/`. Nothing is graded, so
nobody loses marks by reading them. Use them to check your work after you
have tried a drill, or when you are stuck. If you read one first, you get no
practice.

### Task 2 — Reproduce the figure

`drills/target_figure.png` shows weekday and weekend demand profiles, from
the same dataset as the worked example. Write a script that produces a
matching plot.

This is harder than it looks, for one reason. The data file has a date
column but no day-of-the-week column, and you need to know which dates are
weekends.

Python's standard library can tell you. Look up the `datetime` module. Find
out what `date(2026, 3, 2).weekday()` returns.

When your figure matches, you will also have the answer to the question
stage 5 raised.

---

## The rule that starts now

**A figure with an unlabelled axis is not finished.** Every plot from now on
needs axis labels with units, and a title a reader can understand without
you.
