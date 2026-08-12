# Week 2 — Actually programming

**By the end of this week you can:** use variables and lists, write a loop
with a conditional inside it, package repeated work into a function, do
arithmetic on a NumPy array, and produce a labelled figure.

The session has three parts. First the ideas — there are six, and together
they are the working vocabulary of basic programming. Then we build a real
analysis together, live, using each idea at the moment it becomes necessary.
Then you do the tasks, in class, with the instructor and the TA circulating.

Everything this week serves one question: *what does an average day look like
at this traffic count site, and when is the peak?* That is not a toy
question. It is the shape of most analysis you will ever do: take a file of
records, keep the ones that matter, summarise them, and show the result.

---

## Part 1 — The ideas

### 1. Store — variables and types

A variable is a name with a value attached. The line

```python
count = 1703
```

is an instruction with a definite order of events: first the right-hand side
is worked out, then the result is stored under the name on the left. From
that moment, writing `count` anywhere below means *the value currently
stored under that name*.

Be careful with the `=` sign, because it does not mean what it means in
mathematics. In mathematics, `x = x + 1` is a contradiction. In Python,

```python
count = count + 1
```

is routine, and reads as an instruction, right side first: *take the value
currently stored under `count`, add one, and store the result back under
`count`.* The `=` is an action — "make this name refer to this value" — not
a statement of fact. If you hold on to that one reframing, a surprising
amount of code that looks strange becomes readable.

You choose the names. Python's rules are loose — letters, digits, and
underscores, not starting with a digit — but the real constraint is the
human reader. `northbound_total` costs a few more keystrokes than `nt` and
repays them every time anyone, including you in three weeks, has to work
out what the code does.

Every value also has a **type**, and the two you will handle constantly are
numbers and text (text values are called *strings*). The same-looking value
behaves completely differently depending on its type:

```python
1703 + 1        # 1704        - numbers add
"1703" + "1"    # "17031"     - strings join end to end
9 > 1000        # False       - numbers compare by size
"9" > "1000"    # True        - strings compare alphabetically, character by character
```

That last line deserves a second look. Text is ordered like words in a
dictionary: `"9"` comes after `"1000"` because the character `9` comes after
the character `1`, and nothing further is checked. Data that is secretly
text therefore *sorts* wrongly and *compares* wrongly — while looking
perfectly normal when printed.

This matters because **files hand you text**. A CSV file is a plain text
file — open one in a text editor once and see — so every value you read from
it, however numeric it looks, arrives as a string. Converting is your job,
and it is deliberate: `int("1703")` gives the whole number 1703;
`float("3.1")` gives the decimal 3.1.

If you are used to Excel, you have been protected from this — and
occasionally betrayed by the protection. Excel guesses types silently, and
its guesses are famous enough that geneticists renamed human genes because
Excel kept reading them as dates. Python makes the opposite bargain: it
never guesses, and if you compare text with a number it stops with a
`TypeError`. Loud and immediate beats silent and wrong, every time you are
the one signing the analysis.

### 2. Decide — `if`

Programs make decisions with `if`. The anatomy has three parts: the keyword
and a condition, a colon, and an indented block:

```python
if count > 900:
    print("busy hour")
    busy_hours = busy_hours + 1
```

The indentation is not decoration. It is how Python knows which lines belong
to the decision: every indented line is inside it, and the first line that
returns to the left margin is outside it, running whether the condition was
true or not. This is why week 1's `IndentationError` exists — the layout
*is* the structure.

The condition is an expression that works out to one of exactly two values,
`True` or `False`. You build conditions with the comparison operators: `>`,
`<`, `>=`, `<=`, `==` (equal to), and `!=` (not equal to). Note the doubled
`==`: as we saw above, a single `=` stores a value, so Python uses `==` to
ask whether two things are equal. Writing one where you meant the other is
a rite of passage; you will do it once and then rarely again.

An `if` can be given a partner, `else`, whose block runs when the condition
is false — and a chain of further conditions with `elif` ("else if"), which
you will use in the drills:

```python
if ratio < 0.7:
    band = "free flow"
elif ratio < 0.9:
    band = "busy"
else:
    band = "at capacity or worse"
```

One habit to build from the first day: treat **boundaries** as decisions
you make, not accidents that happen. Is a volume-to-capacity ratio of
exactly 0.9 "busy" or "at capacity"? The code will happily implement either;
`ratio < 0.9` puts 0.9 in the upper band, `ratio <= 0.9` puts it in the
lower. Which is *correct* is not a programming question at all — it is a
specification question, the kind you already answer in engineering
standards — and the analyst's job is to choose deliberately and be able to
say which they chose. One of today's drills is built entirely on this
point.

### 3. Repeat — lists and loops

A list holds many values in order:

```python
counts = [52, 22, 24, 29]
```

Positions are numbered **starting from zero**: `counts[0]` is 52,
`counts[1]` is 22, and `counts[3]` is 29 — the last item, at position
*length minus one*. Asking for `counts[4]` raises the `IndexError` you met
last week. Zero-based counting feels wrong for about a week; the way to hold
it is that the index measures *how far from the start* an item is, and the
first item is zero steps away. `len(counts)` gives the length, 4.

**Taking a run of items — slicing.** Square brackets with a colon inside
give you a section of a list rather than one item:

```python
counts[1:3]     # [22, 24]  - from position 1, up to but NOT including 3
counts[1:]      # [22, 24, 29]  - from position 1 to the end
counts[:2]      # [52, 22]  - from the start up to position 2
```

The rule that catches everybody once: the first number is included and the
second is not. So `counts[1:3]` gives you two items, not three, and if you
want positions 7 to 9 *inclusive* you must write `counts[7:10]`. This is the
notation behind `lines[1:]` in last week's script — "everything except the
header row" — and one of today's drills is built on it.

**Making a list of repeated values.** Multiplying a list repeats it, which
is the usual way to start a set of counters at zero:

```python
[0] * 24        # a list of twenty-four zeros
```

A `for` loop runs a block once for each item:

```python
total = 0
for count in counts:
    total = total + count
```

Read the middle line as: *for each value in `counts`, one at a time, store
it under the name `count` and run the indented block.* The name `count` is
yours to choose; it is created by the loop and refilled on every pass.

Do not skim those three lines, because they contain the most important
pattern in data processing: the **accumulator**. Start with an empty total;
fold each item in as it passes. Watch it run, pass by pass:

| pass | `count` | `total` after the line runs |
|---|---|---|
| 1 | 52 | 52 |
| 2 | 22 | 74 |
| 3 | 24 | 98 |
| 4 | 29 | 127 |

Tracing a loop by hand like this — a column for each variable, a row for
each pass — is not a beginner's crutch. It is a professional debugging
technique, and when a loop misbehaves, three hand-traced passes will find
the problem faster than an hour of staring.

The same shape, with an `if` inside, produces the second great pattern:
**build a new list of the items that qualify**. Start with an empty list,
append each item that passes the test. Counting matches, summing matches,
collecting matches — all of them are this one pattern wearing different
clothes, and you will write all three in the drills.

#### The second way to write a loop: over positions

Everything above loops over *items*. There is a second form, which loops
over *positions*, and you need it because the worked example uses it
throughout — and because some jobs are impossible without it.

`range` produces a run of whole numbers:

```python
range(24)          # 0, 1, 2, ... 23   - twenty-four numbers, starting at 0
range(7, 10)       # 7, 8, 9           - starts at 7, stops before 10
range(0, 24, 2)    # 0, 2, 4, ... 22   - every second number
```

Note that `range(24)` stops *before* 24, exactly as slicing does. That is
not a coincidence: Python is consistent about "up to, but not including",
and once you expect it everywhere it stops surprising you.

Put a `range` in a `for` loop and the loop variable holds a position rather
than a value:

```python
for hour_of_day in range(24):        # hour_of_day is 0, then 1, then 2 ...
    print(hour_of_day)
```

These two loops do exactly the same thing:

```python
for count in counts:                 # over items
    total = total + count

for index in range(len(counts)):     # over positions
    total = total + counts[index]
```

The second is longer, so why would anyone write it? Because the position is
sometimes the thing you actually need:

- **When the position is the answer.** "Which hour was busiest?" is asking
  for a position, not a value.
- **When you must walk two lists together.** If `hours[i]` and `counts[i]`
  describe the same row of the file, then one index reaches into both. The
  worked example does this constantly, because it reads the CSV into four
  parallel lists.
- **When you are not walking a list at all.** `for hour_of_day in range(24)`
  loops over the twenty-four hours of a day, whether or not any list of that
  length exists.

`range(len(counts))` reads awkwardly at first. Take it in two steps:
`len(counts)` is 4, so `range(len(counts))` is `range(4)`, which is 0, 1, 2,
3 — every valid position in the list, and never one past the end. Written
that way it stays correct even when the list changes length, which is why it
is preferred over typing the number.

**Use the item form when you can and the position form when you must.** If
you only need each value, `for count in counts` is clearer and harder to get
wrong.

#### Rows that hold several values at once

Data often arrives as pairs or rows rather than single numbers — a list
where every item is itself a small group of values:

```python
rows = [(8, 100), (8, 50), (17, 90)]     # (hour, count) pairs
```

Those round brackets make a **tuple**, which for our purposes behaves like a
list you do not intend to change: `rows[0]` is the pair `(8, 100)`, and
`rows[0][0]` is `8`. You can therefore reach the parts by position, exactly
as with a list:

```python
for row in rows:
    hour = row[0]
    count = row[1]
```

Python also lets you name the parts in the `for` line itself, which does the
same thing more readably:

```python
for hour, count in rows:
    ...
```

This is called **unpacking**, and you have already seen it: last week's
`first_script.py` ends with `for date, hour, count in busy_hours:`, taking
apart three-value rows in exactly this way. Either form is fine; use
whichever you find clearer.

For the spreadsheet-minded: a list is a column, and a loop is what "fill
this formula down the column" has been doing for you all along. Python makes
the repetition visible and puts it under your control — which is exactly
what you need the week the operation becomes too awkward to express in a
cell formula.

### 4. Package — functions

Here is how real analyses go wrong. You write ten good lines that compute an
hourly average for the northbound direction. You need the same for
southbound — so you copy the block and edit one word. The file now contains
two near-identical copies. Weeks later you find a subtle bug and fix it — in
one copy. From that day the two directions are computed by *different
rules*, the file looks perfectly healthy, and nothing will ever warn you.

A **function** is the cure: give the block a name, state what varies, and
keep exactly one copy.

```python
def hourly_average(direction):
    ...
    return result
```

The anatomy: `def` introduces the function; `hourly_average` is its name;
`direction` is a **parameter** — a placeholder name for the value that will
vary; the indented body is the work; and `return` says what the function
hands back. Defining a function runs nothing. It is *called* later, by
name, with an actual value for each parameter:

```python
northbound = hourly_average("northbound")
southbound = hourly_average("southbound")
```

Follow the flow in the first call: the value `"northbound"` flows in and
becomes `direction` for this one run; the body computes; `return result`
sends the answer back; and the call itself — the whole expression
`hourly_average("northbound")` — *becomes* that returned value, which is
then stored under `northbound`. Same tested code, both directions, one place
to fix anything.

**When there is no answer: `None`.** Sometimes a function is asked for
something that does not exist — the average of an empty list, the busiest
hour of a file with no rows. Returning `0` would be a lie, because zero is a
real average and "there was nothing to average" is not the same statement.
Python has a value for exactly this: `None`, meaning *no value at all*.

```python
def average(values):
    if len(values) == 0:
        return None
    ...
```

`None` is a value like any other, so it can be returned and stored — but it
is not zero and not empty text, and arithmetic on it fails immediately with
a `TypeError`. That is a feature: it stops a missing answer from quietly
being treated as a real one, which is the exact failure you will watch
happen in week 3. You test for it with `is None`:

```python
if average(counts) is None:
    print("no data")
```

Deciding what your function does when there is nothing to work on is part of
writing it, not an afterthought — and one of today's drills is built on
precisely that decision.

Two clarifications that save beginners real confusion. First, `return` is
not `print`. A printed value appears on the screen and is gone — you cannot
add it, compare it, or plot it. A returned value comes back into the program
where it can be stored and used. Print is for humans; return is for the rest
of the code. Second, names created inside a function — the parameters and
anything defined in the body — exist only while that call runs, and vanish
afterwards. Functions are sealed rooms: values pass in through the
parameters and out through `return`, and this is precisely what makes one
function testable on its own, without worrying about the rest of the file.

### 5. NumPy — arithmetic on many values at once

NumPy is a **library**: code written by others, installed into your
environment during setup, and brought into a script with

```python
import numpy as np
```

— which loads it and gives it the short nickname `np`, the universal
convention.

Its central object is the **array**. An array is like a list with one
restriction and one superpower. The restriction: every element has the same
type. The superpower: arithmetic applies to *the whole array at once*:

```python
counts = np.array([900, 1800, 2700])
counts / 1800          # array([0.5, 1.0, 1.5])
```

One line, no loop — you say *what* should happen to every element, and NumPy
handles the *each*. Comparisons work the same way, and produce an array of
`True`/`False` values called a **mask**:

```python
directions == "northbound"   # array([True, False, True, ...])
```

A mask can then be used to select: `counts[mask]` keeps exactly the elements
in the `True` positions. Filtering a dataset — the `if` inside the loop you
wrote in idea 3 — becomes two short lines: build the mask, apply it. Masks
can be combined with `&` (and) and `|` (or), with parentheses around each
comparison; you will see that in the demonstration.

Understand what has *not* happened here: nothing new. When you write
`counts.mean()`, an accumulator loop runs — the same start-at-zero,
fold-each-item-in loop you wrote by hand — inside the library, in a faster
language. NumPy is a convenience and an accelerant, not a different kind of
thing. We make you write the loop first precisely so that the one-line
version is something you can *explain*, and being able to explain your tools
is about to become the theme of this course.

### 6. The figure

The usual output of an analysis is a figure, and the standard tool is
matplotlib. Its mental model has two objects: the **figure** (the page) and
the **axes** (the plotting area on that page — an awkward name, but
universal). You get both from one call, then each further call adds or sets
one element, and nothing appears anywhere until you save:

```python
figure, axes = plt.subplots()
axes.plot(hours, flows)            # the data, as a line
axes.set_xlabel("Hour of day")
axes.set_ylabel("Average flow (vehicles per hour)")
axes.set_title("Average hourly flow, site A34/012, 2-15 March 2026")
figure.savefig("profile.png")
```

Six calls, one finished figure, written to a file you can put in a report.
Everything else matplotlib offers — colours, legends, annotations, grids —
is more calls of the same shape, added one at a time.

What makes a figure *finished* is a checklist, and it is short: both axes
labelled, **with units**; a title that states the finding, or at least the
full context — site, place, period; a legend whenever more than one series
is plotted; and the file saved at a size where the text is readable.

The reason for the rule is worth spelling out, because the rule is the one
thing from this week that applies to every figure you will ever make. A
figure does not stay in your notebook. It gets pasted into a slide deck,
cropped into a report, forwarded in an email — and it arrives without you,
without your caption, and without the surrounding text. A reader one year
from now will decide something based on what the figure alone says. An
unlabelled axis makes that figure unusable at best; at worst, it makes it
confidently misread. On most days, the figure *is* the analysis, and it
travels alone. Label it accordingly.

---

## Part 2 — Demonstration: `worked_example.py`

We build this together, live, in six stages. Each stage uses the idea above
at the moment it is needed. With your virtual environment active:

```
cd week2_programming
python worked_example.py
```

| Stage | What happens | Idea used |
|---|---|---|
| 1 | Read the CSV into four lists | Store |
| 2 | Keep only the chosen direction | Decide |
| 3 | Average each hour of the day, the long way | Repeat |
| 4 | Turn the block into a function; run it for both directions | Package |
| 5 | The same calculation again in NumPy; check the answers agree | NumPy |
| 6 | The figure: labelled, titled, saved to a file | The figure |

Two moments in the file are worth noticing. At the end of stage 4 there is an
`assert` line that checks stage 4 against stage 3 — the same answer computed
two ways, compared automatically. That habit, in one line, is the entire idea
behind week 3. And stage 5 prints a standard deviation at the peak hour that
is surprisingly large. It is not a mistake. Task 2 will show you what it was
telling us.

---

## Part 3 — The tasks

You do these in class, under supervision. Try for ten minutes, then ask —
the instructor and the TA are there to be used. Anything unfinished at the
end of the session, finish before next week.

### Task 1 — The drills

Twelve short exercises, one per idea, in rising order of difficulty. They
work exactly like last week's traceback safari: **one file each**, in
`drills/`, from `drill_01.py` to `drill_12.py`, with a `check.py` that marks
them.

Open a drill file. It contains one function with a `TODO` where its body
should be, and a docstring saying what the function must do, what it should
return for a couple of example inputs, and which idea from Part 1 it comes
from. Fill in the body, save, and run the marker:

```
cd week2_programming/drills
python check.py
```

`check.py` reports each drill as `PASS`, `TODO` (it runs but the answer is
not right yet), `ERROR` (it raised something), or `BROKEN` (the file will
not even start — usually an indentation problem). It does not tell you how
to fix anything; that is the exercise.

The drills are independent of one another, so work on one file at a time and
ignore the rest. There is no need to finish drill 3 before starting drill 4.

Aim to finish the nine unstarred drills; the three marked with a star are
harder and entirely optional. You are not expected to know any of this from
memory: look things up, reread Part 1, reread the worked example, ask the
person next to you, ask the TA. The one approach that teaches you nothing is
copying a finished answer — the struggle in the middle is what the practice
is for.

Complete solutions exist in `instructor/solutions/week2/`, openly and on
purpose: nothing is graded, so they can only help you or cheat you, and
which one is your choice. The good use is checking your working version
against another way of doing it, or getting unstuck after a genuine attempt.
The self-defeating use is reading one before you have tried.

### Task 2 — Reproduce the figure

The file `drills/target_figure.png` shows weekday and weekend demand
profiles, drawn from the same dataset as the worked example. Write a script
that produces a matching plot.

This task is more difficult than it first appears, for one specific reason:
the data file has a date column, but no day-of-the-week column, and you will
need to know which dates are weekends. Python's standard library can tell
you. Look up the `datetime` module, and in particular what
`date(2026, 3, 2).weekday()` returns. Finding and reading that piece of
documentation is part of the task — it is a small version of something you
will do constantly from week 3 onwards.

When your figure matches, you will also have answered the question stage 5
left open: what that large standard deviation at the peak was telling us.

---

## The rule that starts now

**A figure with an unlabelled axis is not finished.** From here to the end of
the course, every plot you produce needs axis labels with units, and a title
that a reader could understand without you in the room.
