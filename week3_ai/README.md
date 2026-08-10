# Week 3 — AI acceleration

**By the end of this week you can:** describe a task precisely enough that an
AI assistant produces correct code, check that code against a case you can
work out by hand, and build things in small steps that you verify as you go.

The session has three parts. First a demonstration — deliberately before any
teaching, for reasons that will be obvious once you have seen it. Then the
ideas. Then one substantial task, done in class under supervision, which uses
everything from the first three weeks at once.

---

## Part 1 — Demonstration: the failure

We begin in `failure_demo/`: a reasonable-sounding request typed into an AI
assistant, a professional-looking answer, and an error of about 21% that
nothing on the screen would warn you about.

```
cd week3_ai/failure_demo
python lazy_analysis.py
python correct_analysis.py
```

If you missed the session, `failure_demo/README.md` records what happened and
why it matters. If you have not seen the session yet, know that the
demonstration lands harder live — the folder will still be there afterwards.

## Part 2 — The ideas

### 1. You have been promoted

From today you are no longer the person who writes every line. You are the
person who **specifies** the work and **signs it off**. Those are the two
jobs of every senior engineer who reviews the work of others — and both of
them require you to read code with understanding, which is what the last two
weeks gave you.

An assistant makes you faster at exactly the rate that you can check its
output. A person who cannot check the output is not faster. They are merely
producing wrong answers sooner, with more confidence.

### 2. Specifying

The demonstration fails because the request leaves everything important
unsaid. A usable specification states four things:

- **The shape of the input.** The columns, their types, and their units.
  "`scheduled_time` and `actual_time` are text in HH:MM:SS format" saves an
  assistant from guessing — and it will guess.
- **The conventions that live outside the file.** What a missing value looks
  like. What a sentinel code means. Which column is authoritative when two
  disagree. The assistant cannot see any of this; only you can.
- **The output you expect.** Its shape, its units, and roughly its size. "A
  journey time between these stops should be tens of minutes, not seconds"
  gives both of you a way to notice nonsense.
- **The awkward cases.** What should happen with a duplicate, a gap, an
  empty result. If you do not decide, the assistant will — silently.

Writing this down feels slow. It is the opposite: every item you leave out
becomes a guess, and every guess is a place the code can be confidently
wrong.

### 3. Verifying

The full method is [`verification_checklist.md`](verification_checklist.md) —
print it and keep it beside you; it is written to remain useful long after
this course. Its heart is four checks, applied to any code you did not write
yourself:

1. **Does it run?**
2. **Does it give the right answer on a case you already know?** Work five
   rows out by hand and compare. This is the check people skip, and it is
   the one that catches real errors.
3. **What does it do with the awkward cases?** Missing values, duplicates,
   zeros, empty inputs, the full file.
4. **Can you explain every line?** A line you cannot explain is a line you
   cannot defend. Asking what a line does is always allowed; skipping it is
   not.

### 4. Working in the loop

Ask for one function. Run it. Check it. Then ask for the next. Keep a copy
of every version that worked.

The failure pattern this avoids: asking for two hundred lines, receiving two
hundred lines, and having no idea which of them is broken. Small steps feel
slower, and are faster — debugging one new function is minutes; debugging
two hundred unfamiliar lines is an afternoon.

### 5. Where this breaks

Honest limits, so none of them surprises you later:

- Assistants state domain assumptions confidently and invisibly — a
  direction convention, a time zone, a headway.
- They drop data silently: a filter that also removes rows you needed, a
  merge that quietly discards non-matches.
- They produce plausible statistics — a mean where a median was needed —
  whose results are wrong by an amount too small to look wrong.
- Code that works on a sample can fail, or mislead, on the full file.

Every one of these is caught by the four checks. None of them is caught by
reading the output and finding it believable — that is exactly the test the
demonstration passed while being wrong.

---

## Part 3 — The task

[`task.md`](task.md) — build a journey time tool, with AI assistance, against
data that has real problems in it. You do it in class, with the instructor
and the TA circulating; it is the first time this course asks you to use an
assistant, a specification, and the checklist together.

You produce three things: the code, the prompts you used, and **evidence that
the code is correct**. Nothing is graded — the evidence matters because it is
the part the assistant cannot do for you, and because the project weeks ask
you to repeat exactly this pattern, at volume, on your own project.

## What you are allowed to use

Anything — including pandas, a library you have not been taught. Working out
how to use an unfamiliar library safely, with the assistant's help and your
own checks, is precisely this week's skill.
