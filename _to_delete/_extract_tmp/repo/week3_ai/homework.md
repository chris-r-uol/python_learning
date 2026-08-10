# Week 3 homework — build something, then prove it works

**Time: about 2 hours. Due before week 4.**

You are going to build a small tool with AI assistance. The tool is the easy
part. The submission is graded on whether you can show it is correct.

---

## The task

Write `journey_time.py`. Given the project's `arrivals.csv`, it should:

1. Take a `from` stop, a `to` stop, and a time band (e.g. `08:00`–`09:00`).
2. Return the journey time between those stops for every trip in that band.
3. Report the mean, the median, and the 90th percentile.
4. Say how many trips it used, and how many it dropped and why.

Requirement 4 is not optional decoration. It is the requirement.

You may use pandas. You have not been taught it. That is deliberate — use the
assistant to help you, and apply the checklist to what it gives you.

---

## What you submit

Three files.

### 1. `journey_time.py`
The tool.

### 2. `prompts.md`
Every prompt you used, in order, including the ones that went wrong. If you
rewrote a prompt, show both versions and say what you changed and why.

We are not checking that your prompts were good. We are checking that you know
which ones worked.

### 3. `verification.md`
**This is what is marked.** It must contain:

**a. A hand-worked case.**
Pick one pair of stops and one specific trip. Work out the journey time
yourself — from the raw CSV, with a calculator or a spreadsheet. Show the two
timestamps you used and the arithmetic. Then show your tool's answer for the
same trip. State whether they match.

If they don't match, that is a finding, not a failure. Write down what you found
and what you did about it.

**b. The edge cases.**
For each of the following, say what your tool does and whether that is the right
behaviour:

- A trip where one of the two stops has no record at all
- A journey time that comes out negative
- A trip that crosses midnight
- The stop that appears under two different names
- Rows that appear twice

You will not have anticipated all of these. Finding out which ones break your
tool *is the exercise*. A tool that handles three of five, with the other two
documented honestly, scores better than one that claims to handle all five
without evidence.

**c. One line per function.**
For every function in your file, one sentence saying what it does. If you cannot
write the sentence, you do not yet own that code — go and ask what it does.

---

## Marking

| | Weight |
|---|---|
| Verification evidence — the hand-worked case and edge cases | **60%** |
| Prompt record — shows a real iteration, not one lucky shot | 20% |
| The tool itself — runs, does roughly the right thing | 20% |

Yes, that is deliberate. Working code with no evidence scores 20%. A partial
tool with thorough, honest verification scores 80%.

The reason: on the project, and afterwards in your job, nobody will check your
work for you. The only thing standing between a wrong number and a decision made
on it is whether you looked.

---

## Two things that will lose you marks

**Submitting code you cannot explain.** We will ask, in week 4, out loud.

**A verification section that says "I tested it and it worked."** That is not
evidence. Evidence has numbers in it.
