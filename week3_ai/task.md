# Week 3 task — build something, then prove it works

**Done in class, under supervision. About 2 hours of work. Anything
unfinished at the end of the session, finish before week 4 — the project
weeks assume this way of working.**

You are going to build a small tool with AI assistance. Building the tool is
the easy part. The real exercise is showing that it is correct — nothing here
is graded, and that is precisely why the proof matters: the only reason to
verify is the only reason that will exist after this course, which is that
nobody else is going to.

The instructor and the TA are circulating, and this task is designed to make
you need them at least once. Try for ten minutes, then ask — and note that
"how do I check this?" is a better question to bring than "why is this
broken?", though both are welcome.

---

## The task

Create a file `journey_time.py` in this folder (`week3_ai/`). The data it
works on is the project's arrival records, at `project/data/arrivals.csv`
relative to the top of the repository.

Given a *from* stop, a *to* stop, and a time band (for example 08:00 to
09:00), your tool should:

1. Find the journey time between those two stops for every trip that departs
   within the band.
2. Report the mean, the median, and the 90th percentile.
3. State how many trips it used — and how many it dropped, and why.

Requirement 3 is not decoration. It is the requirement.

You may use pandas. You have not been taught pandas; that is deliberate. Ask
the assistant for help, and apply the checklist to everything it gives you.

---

## What you produce

Three files. Keep all three — together they are the template for every piece
of AI-assisted work you do in the project weeks, and afterwards.

### 1. `journey_time.py`

The tool.

### 2. `prompts.md`

Every prompt you used, in order, including the ones that did not work. If you
rewrote a prompt, include both versions and say what you changed and why.

The point is not elegant prompts. The point is knowing, afterwards, which
ones worked and being able to say why — that record is how the skill
compounds instead of resetting every session.

### 3. `verification.md`

**This is the part that matters.** It has three sections.

**a. A hand-worked case.**
Choose one pair of stops and one specific trip. Work out the journey time
yourself, from the raw CSV, with a calculator or a spreadsheet. Show the two
timestamps you used and the arithmetic. Then show your tool's answer for the
same trip, and state whether the two agree.

If they do not agree, that is a finding, not a failure. Write down what you
found and what you did about it.

**b. The awkward cases.**
For each case below, establish what your tool does, and state whether that
behaviour is correct. Be careful: some of these cases occur in the data, and
some may not. If you check and find that a case does not occur, say so — that
check is itself verification — and then test your tool against a small input
you construct yourself, so you still know how it would behave.

- A trip that has no record at one of the two stops
- A journey time that comes out negative
- A trip that crosses midnight
- A stop that appears under two different names
- Rows that appear twice

You will not have anticipated all of these. Finding out which ones your tool
handles, and which ones break it, *is the exercise*. A tool that handles
three of the five, with the other two documented honestly, is worth more
than one that claims to handle all five without evidence — here and
everywhere after this course.

**c. One sentence per function.**
For every function in your file, write one sentence saying what it does. If
you cannot write that sentence, you do not yet own that code — ask the
assistant what the function does, and keep asking until you can explain it.

---

## Where the value is

Nothing here is graded, so be honest about which part of this task is worth
your two hours. It is not the tool — the assistant writes most of the tool.
It is the verification: the evidence file is the part you could not have
produced three weeks ago, and the part that makes the tool trustworthy
rather than merely plausible.

The reason it matters: in the project weeks, and afterwards in your work,
nobody will check your numbers for you. The only thing standing between a
wrong number and a decision made on it is whether you looked.

---

## Two habits to avoid from the start

**Keeping code you cannot explain.** In week 4 the instructor will ask you,
conversationally and in person, what your code does — not to test you, but
because saying it out loud is how you find out whether you own it.

**Writing "I tested it and it worked."** That is not evidence. Evidence
contains numbers.
