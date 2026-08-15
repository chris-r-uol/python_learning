# Setup — work laptop with no admin rights

This guide is for managed machines. Use it if installers ask for an
administrator password you do not have, if your IT department controls the
app store, or if your network blocks downloads.

**Give this 30 minutes. Then stop and use [Codespaces](codespaces.md).**

A Codespace needs only a browser and a free GitHub account, so a locked-down
laptop cannot block it. You get a real terminal and a real virtual
environment. You lose nothing from the course.

If your machine is heavily restricted, go straight to Codespaces and skip
this page.

To install locally, try these options in order.

## Option 1 — your organisation's software centre

Managed machines often have a software catalogue. It may be called "Software
Center", "Company Portal" or something similar. Python and VS Code are
common entries.

1. Open the software centre. Search for **Python** (3.11 or newer) and
   **Visual Studio Code**.
2. If both are there, install them. Then follow [`windows.md`](windows.md)
   from step 4.

## Option 2 — install for your user only

Python and VS Code can install into your own account without administrator
rights. Many managed machines allow this.

1. Download Python from
   [python.org/downloads](https://www.python.org/downloads/). Run the
   installer. Tick **"Add python.exe to PATH"**. Choose **"Install Now"**.
   Do not choose "Customize" and "Install for all users", which needs admin
   rights.
2. Download the VS Code **User Installer** from
   [code.visualstudio.com](https://code.visualstudio.com/). The standard
   Windows download is the user version and needs no admin rights.
3. If both install, follow [`windows.md`](windows.md) from step 4.

**If `pip install` fails** with an error about SSL, certificates, a proxy or
a timeout, your network is intercepting downloads. Use
[Codespaces](codespaces.md). It runs on GitHub's computers, so your network
cannot block it.

## Option 3 — portable Python

If installers are blocked completely, use
[WinPython](https://winpython.github.io/). It is a complete Python that runs
from a folder. Download it, unzip it somewhere you can write to, and use the
**WinPython Command Prompt** inside that folder as your terminal. It
includes the packages this course needs.

This option is the most awkward, and version mismatches are more likely.
Note that you used it, so a later problem has an explanation.

## Option 4 — Codespaces

[`codespaces.md`](codespaces.md). Nothing to install. A browser and a free
GitHub account are all you need.

## Option 5 — Colab

[`colab-fallback.md`](colab-fallback.md). Use this if you cannot have a
GitHub account.

---

Have your setup working **before** the first session. Session time is for
the course, not for installers.
