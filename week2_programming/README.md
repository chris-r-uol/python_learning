# Week 2 — Actually programming

**By the end of this week you can:** use variables and lists, write a loop
with a conditional inside it, package repeated work into a function, do
arithmetic on a NumPy array, and produce a labelled figure.

The session has three parts. First the ideas — there are six, and they are
the whole vocabulary of basic programming. Then we build a real analysis
together, live, using each idea at the moment it becomes necessary. Then you
do the tasks, in class, with the instructor and the TA circulating.

Everything this week serves one question: *what does an average day look like
at this traffic count site, and when is the peak?* That is not a toy
question. It is the shape of most analysis you will ever do: take a file of
records, keep the ones that matter, summarise them, and show the result.

---

## Part 1 — The ideas

### 1. Store — variables and types

A variable is a name with a value attached. `count = 1703` stores the number
1703 under the name `count`; from then on, writing `count` means that value.

Every value has a **type**, and the two you meet constantly are text (called
a *string*) and numbers. This distinction matters more than it first appears,
because data files arrive as text. When you read `"1703"` from a CSV file,
you have four characters, not a number — and text behaves like text:

```python
"9" > "1000"      # True  - text compares alphabetically, character by character
9 > 1000          # False - numbers compare as numbers
```

The function `int()` converts text to a whole number: `int("1703")` is
`1703`. Forgetting this conversion is one of the most common mistakes in data
work, and Python will not always warn you — sometimes it just sorts your
data alphabetically and lets you draw the wrong conclusion.

### 2. Decide — `if`

Programs make decisions with `if`: a condition, and an indented block that
runs only when the condition is true.

```python
if count > 900:
    print("busy hour")
```

Conditions use comparisons — `>`, `<`, `>=`, `<=`, `==` (equal), `!=` (not
equal). Two things deserve care. First, `==` compares, while `=` assigns;
confusing them is a classic error. Second, boundaries: `count > 900` and
`count >= 900` differ only for the value 900 exactly, and deciding which you
mean is part of specifying an analysis, not a detail. One of today's drills
is built entirely on this point.

### 3. Repeat — lists and loops

A list holds many values in order: `counts = [52, 22, 24, 29]`. Positions
are numbered **starting from zero**, so `counts[0]` is 52 and `counts[3]` is
29. Asking for `counts[4]` raises the `IndexError` you met last week.

A `for` loop does something once for each item:

```python
total = 0
for count in counts:
    total = total + count
```

The pattern in those three lines is called an **accumulator**: start with an
empty total, add each item as it passes. It looks humble. It is the single
most useful pattern in data processing — counting, summing, collecting
matches into a new list — and most of what libraries like NumPy do for you
is this pattern, performed at speed.

### 4. Package — functions

When the same block of code appears twice, the temptation is to copy it and
edit one word. This is how many real bugs are born: the copies drift apart,
someone fixes one and not the other, and the analysis quietly disagrees with
itself.

A **function** removes the temptation. You name the block, state what inputs
it needs, and state what it hands back:

```python
def hourly_average(direction):
    ...
    return result
```

`def` names the function and its inputs; `return` is what comes back.
Afterwards, `hourly_average("northbound")` and `hourly_average("southbound")`
run the same tested code on different inputs. One block, one place to fix,
no drift.

### 5. NumPy — arithmetic on many values at once

NumPy is a library for numerical work. Its central object, the **array**, is
a sequence like a list, with one large difference: arithmetic applies to the
whole array at once.

```python
counts = np.array([900, 1800, 2700])
counts / 1800          # array([0.5, 1.0, 1.5])
```

A comparison applies to the whole array too, producing an array of `True`
and `False` called a **mask** — which can then select rows:

```python
mask = directions == "northbound"
counts[mask]           # only the northbound counts
```

Nothing new is happening here. The loop you wrote in idea 3 is still
running — inside the library, in a faster language. That is why we write the
loop by hand first: so that NumPy is a convenience you understand, not a
mystery you depend on.

### 6. The figure

The output of an analysis is usually a figure, and matplotlib is the
standard tool. The mechanics are a handful of calls — plot the values, label
the axes, set a title, save the file — and you will see all of them in the
demonstration.

The standard is the part that matters, and it starts now: **a figure with an
unlabelled axis is not finished.** Every figure you produce from today needs
axis labels with units, and a title that a reader could understand without
you in the room. A figure is not decoration for an argument. On most days,
the figure *is* the argument.

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

Twelve short exercises in `drills/drills.py`, one per idea, in rising order
of difficulty. Fill in each function where it says TODO, then run the file —
it marks itself and tells you which functions pass.

```
cd week2_programming/drills
python drills.py
```

Aim to finish the nine unstarred drills; the three marked with a star are
harder and entirely optional. You are not expected to know any of this from
memory: look things up, reread Part 1, reread the worked example, ask the
person next to you, ask the TA. The one approach that teaches you nothing is
copying a finished answer — the struggle in the middle is what the practice
is for.

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
