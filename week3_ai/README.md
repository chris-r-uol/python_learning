# Week 3 — AI acceleration

**By the end of this week you can:** describe a task precisely enough that an
AI assistant produces correct code, check that code against a case you can
work out by hand, and build things in small steps that you verify as you go.

You have been promoted. You are no longer the person who writes every line —
you are the person who specifies the work and signs it off. Both of those jobs
require you to read code with understanding, and that is what the last two
weeks gave you.

## In the session

We begin with `failure_demo/`: a reasonable-sounding request, a
professional-looking answer, and an error of about 21% that nothing on the
screen would warn you about.

```
cd week3_ai/failure_demo
python lazy_analysis.py
python correct_analysis.py
```

After that: how to specify a task, how to verify the result, and how to work
with an assistant in a loop.

## The one thing to keep

[`verification_checklist.md`](verification_checklist.md). Print it and keep it
next to you. You will use it for the rest of the course, and it is written to
be useful long after the course ends.

## Homework (about 2 hours)

[`homework.md`](homework.md) — build a journey time tool with AI assistance.

You submit three things: the code, the prompts you used, and **evidence that
the code is correct**. The evidence carries 60% of the mark. A partial tool
with thorough verification scores higher than a complete tool with none.

That weighting is deliberate. After this course, nobody will check your work
for you.

## What you are allowed to use

Anything — including pandas, a library you have not been taught. Working out
how to use an unfamiliar library safely, with the assistant's help and your
own checks, is precisely this week's skill.
