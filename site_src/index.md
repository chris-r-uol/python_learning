---
title: Start here
---

# Python for Transport & Civil Engineering

Five weeks. You start by running someone else's script and end by building a
transport atlas of a place you choose, assembled from national open data with
an AI assistant, and checked by you.

**Keep this page open beside your editor.** It is a reference, not a
textbook: everything here is the same text as the files in the repository, so
you can read a task on one side of the screen and do it on the other.

!!! tip "Two things worth knowing before you start"

    **Nothing here is graded.** No submissions, no presentations, nobody
    reviewing your work. Nothing is collected from you at any point.

    **The answers are published too.** Worked solutions to weeks 1 and 2 live
    in `instructor/solutions/`. Use them the way you would use the answers in
    the back of a textbook — after a real attempt.

## Before week 1

Set up your machine, then run the check and read what it tells you.

<div class="grid cards" markdown>

-   :material-microsoft-windows: **Windows**

    ---

    The PATH checkbox is the one that matters.

    [Setup guide](setup/windows.md)

-   :material-apple: **macOS**

    ---

    Do not use the Python that came with your Mac.

    [Setup guide](setup/macos.md)

-   :material-github: **No installation at all**

    ---

    A Codespace runs in your browser. Nothing to install, nothing your
    laptop can block.

    [Codespaces guide](setup/codespaces.md)

-   :material-lock-outline: **Managed or restricted laptop**

    ---

    No admin rights, or a network that blocks downloads.

    [Options in order](setup/locked-down-laptop.md)

</div>

Then, in the course folder:

```bash
python check_setup.py
```

## If something does not work

It will, at some point, and that is not a sign you have gone wrong. Working
out *why* something is broken is the actual subject of this course; the
setup is simply the first place you get to practise it.

When something fails, in this order:

1. **Read the message**, properly and to the end. It usually says what is
   wrong, and often says what to do about it.
2. **Check the "If this fails" notes** in your setup guide. The failures
   almost everyone hits are listed there with their fixes.
3. **Paste the exact error into an AI assistant** and ask what it means.
   Installation problems are the most thoroughly documented problems in
   computing. From week 3 you will be doing a far more demanding version of
   this.
4. **Search the exact error text.** Somebody has had it before you.
5. **Half an hour gone? Stop, and use [Codespaces](setup/codespaces.md).**
   Nothing to install, nothing your laptop can block, and no part of the
   course is lost. Choosing it is good judgement, not defeat.
6. **Still stuck when the session starts?** Bring it with you. Studio time,
   with an instructor and a TA in the room, is exactly what that time is
   for.

## The five weeks

Weeks 1 to 3 are about **doing the work**: reading code, writing it, and
learning to tell whether it is right. Weeks 4 and 5 are one project, and that
project is mostly about **finding data and knowing what is wrong with it**.

<div class="grid cards" markdown>

-   **Week 1 — Getting Python working**

    ---

    What a program is, where files live, how to read an error message. Then
    two tasks: a parameter sweep, and six broken scripts to fix.

    [Week 1](week1_setup/README.md)

-   **Week 2 — Actually programming**

    ---

    Variables, types, `if`, loops, functions, NumPy, and your first figure —
    each introduced at the moment it becomes necessary. Twelve drills.

    [Week 2](week2_programming/README.md)

-   **Week 3 — AI acceleration**

    ---

    You have been promoted: you now specify the work and sign it off. Built
    around a demonstration of an assistant being confidently, silently wrong.

    [Week 3](week3_ai/README.md)

-   **Weeks 4 and 5 — Your Patch**

    ---

    Seven chapters of real national data about a British town you choose.
    Too big to hand-write, which is the point.

    [The project](project/index.md)

</div>

## The three rules

They apply from week 1 to the end, and they are the whole course in three
lines.

1. **A figure with an unlabelled axis is not finished.** Axis labels with
   units, and a title a stranger could read.
2. **Code that works but that you cannot explain is not finished either.**
   From week 3 you will be asked how you know your answer is right — by
   yourself, of yourself.
3. **Getting stuck is the work, not a failure at it.** When it happens, read
   the error message. It is the most helpful thing on your screen.
