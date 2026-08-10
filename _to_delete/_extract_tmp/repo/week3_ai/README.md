# Week 3 — AI acceleration

**By the end of this week you can:** specify a task precisely enough to get
correct code, verify it against a case you can check by hand, and work in small
verify-as-you-go steps.

You have been promoted. You are no longer the person writing every line — you
are the person who specifies the work and signs it off. Both of those jobs
require you to read code, which is what the last two weeks bought you.

## In the session

We start with `failure_demo/`. A reasonable-sounding prompt, a professional-
looking answer, and a 21% error nobody would catch by looking.

```
cd week3_ai/failure_demo
python lazy_analysis.py
python correct_analysis.py
```

Then: how to specify, how to verify, and how to work in a loop.

## The one thing to keep

[`verification_checklist.md`](verification_checklist.md). Print it. Use it for
the rest of the course and afterwards.

## Homework (~2h)

[`homework.md`](homework.md) — build a journey time tool with AI assistance.

You submit the code, the prompts, **and evidence it is correct**. The evidence
is 60% of the mark. A partial tool with thorough verification scores higher than
a complete one with none.

That is deliberate. Nobody after this course will check your work for you.

## What you are allowed to use

Anything. Including pandas, which you have not been taught. Working out how to
safely use a library nobody taught you *is* this week's skill.
