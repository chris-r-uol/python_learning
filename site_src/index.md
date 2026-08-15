---
title: Start here
---

# Python for Transport & Civil Engineering

Five weeks. You start by running someone else's script. You finish by
building a transport atlas of a place you choose, using national open data
and an AI assistant.

Keep this page open beside your editor. It has the same text as the files in
the repository, so you can read a task on one side of the screen and do it
on the other.

!!! note "Two things before you start"

    **Nothing here is graded.** No submissions, no presentations, nobody
    reviewing your work. Nothing is collected at any point.

    **The answers are published.** Worked solutions to weeks 1 and 2 are in
    `instructor/solutions/`. Use them to check your work after you have
    tried a task.

## Before week 1

Set up your machine. This takes about 45 minutes.

<div class="grid cards" markdown>

-   :material-microsoft-windows: **Windows**

    ---

    Tick "Add python.exe to PATH" on the first installer screen.

    [Setup guide](setup/windows.md)

-   :material-apple: **macOS**

    ---

    Do not use the Python that came with your Mac.

    [Setup guide](setup/macos.md)

-   :material-github: **No installation**

    ---

    A Codespace runs in your browser. Nothing to install.

    [Codespaces guide](setup/codespaces.md)

-   :material-lock-outline: **Restricted laptop**

    ---

    No admin rights, or a network that blocks downloads.

    [Options in order](setup/locked-down-laptop.md)

</div>

Then, in the course folder:

```bash
python check_setup.py
```

Read what it prints. If it reports a problem, it also names the fix.

## If something does not work

Try these in order.

1. **Read the message to the end.** It usually names the problem.
2. **Read the "If this fails" notes** in your setup guide. Common problems
   are listed there with their fixes.
3. **Paste the exact error into an AI assistant.** Ask what it means.
   Installation errors are well documented.
4. **Search for the exact error text.**
5. **After 30 minutes, stop. Use [Codespaces](setup/codespaces.md).** It
   needs no installation. You lose nothing from the course.
6. **Still stuck at the session?** Bring it. The instructor and TA are
   there.

## The five weeks

Weeks 1 to 3 teach you to read code, write it, and check whether it is
right. Weeks 4 and 5 are one project, mostly about finding data and knowing
what is wrong with it.

<div class="grid cards" markdown>

-   **Week 1 — Getting Python working**

    ---

    What a program is, where files live, how to read an error message. Then
    two tasks: a parameter sweep and six broken scripts.

    [Week 1](week1_setup/README.md)

-   **Week 2 — Actually programming**

    ---

    Variables, types, `if`, loops, functions, NumPy, and your first figure.
    Then twelve drills.

    [Week 2](week2_programming/README.md)

-   **Week 3 — AI acceleration**

    ---

    Your job becomes describing the work and checking the result. Built
    around a demonstration of an assistant being wrong.

    [Week 3](week3_ai/README.md)

-   **Weeks 4 and 5 — Your Patch**

    ---

    Seven chapters of national data about a British town you choose.

    [The project](project/index.md)

-   **A worked example**

    ---

    The same project, built for Leeds by an AI assistant. Its plan, its
    figures, and the four things it got wrong.

    [The worked atlas](atlas/index.md)

</div>

## Three rules

1. **A figure with an unlabelled axis is not finished.** Label both axes.
   Give units. Write a title a stranger can understand.
2. **Code you cannot explain is not finished.** From week 3 you check
   whether your answers are right.
3. **Getting stuck is normal.** Read the error message first.
