# Week 3 homework — build something, then prove it works

**Time: about 2 hours. Due before week 4.**

You are going to build a small tool with AI assistance. Building the tool is
the easy part. The submission is graded on whether you can show that it is
correct.

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

## What you submit

Three files.

### 1. `journey_time.py`

The tool.

### 2. `prompts.md`

Every prompt you used, in order, including the ones that did not work. If you
rewrote a prompt, include both versions and say what you changed and why.

We are not checking whether your prompts were elegant. We are checking that
you know which ones worked, and can say why.

### 3. `verification.md`

**This is the part that is marked.** It must contain three sections.

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
handles, and which ones break it, *is the exercise*. A tool that handles three
of the five, with the other two documented honestly, scores better than one
that claims to handle all five without evidence.

**c. One sentence per function.**
For every function in your file, write one sentence saying what it does. If
you cannot write that sentence, you do not yet own that code — ask the
assistant what the function does, and keep asking until you can explain it.

---

## Marking

| | Weight |
|---|---|
| Verification evidence — the hand-worked case and the awkward cases | **60%** |
| Prompt record — shows real iteration, not one lucky attempt | 20% |
| The tool itself — runs, and does approximately the right thing | 20% |

Yes, this is deliberate. Working code with no evidence scores 20%. A partial
tool with thorough, honest verification scores 80%.

The reason: in the project, and afterwards in your work, nobody will check
your numbers for you. The only thing standing between a wrong number and a
decision made on it is whether you looked.

---

## Two things that will lose you marks

**Submitting code you cannot explain.** In week 4 we will ask you to explain
it, in person.

**A verification section that says "I tested it and it worked."** That is not
evidence. Evidence contains numbers.
