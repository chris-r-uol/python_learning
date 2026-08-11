# Setup — work laptop with no admin rights

This guide is for managed or corporate machines: laptops where installers ask
for an administrator password you do not have, where the app store is
controlled by your IT department, or where the network blocks some downloads.

One rule before you start: **give this thirty minutes, then stop.** If none
of the local options works within half an hour, switch to
[`codespaces.md`](codespaces.md) and tell us which step failed. A Codespace
needs nothing but a browser and a free GitHub account, so a locked-down
laptop cannot block it — and it gives you a real terminal and a real virtual
environment, so no part of the course is lost. It is a full, supported way
to take this course, not a lesser one.

In fact, if your machine is heavily restricted, you may prefer to go
straight to Codespaces and skip the rest of this page. What we do not want
is you losing an evening to a fight with your IT department that we could
have had for you.

If you would still rather install locally, try the options in this order.

## Option 1 — your organisation's software centre

Many managed machines have a self-service software catalogue (often called
"Software Center", "Company Portal", or similar). Python and VS Code are common
entries because developers ask for them constantly.

1. Open the software centre and search for **Python** (3.11 or newer) and
   **Visual Studio Code**.
2. If both are there, install them, then follow the ordinary
   [`windows.md`](windows.md) guide from step 4 onwards.

## Option 2 — per-user installation (no admin needed)

Both Python and VS Code can install into your own user account without
administrator rights, and on many managed machines this is allowed.

1. Download Python from [python.org/downloads](https://www.python.org/downloads/).
   Run the installer, tick **"Add python.exe to PATH"**, and choose
   **"Install Now"** — do *not* choose "Customize" and "Install for all users",
   which is the option that needs admin rights.
2. Download the VS Code **User Installer** from
   [code.visualstudio.com](https://code.visualstudio.com/) — the standard
   download for Windows is already the user version, and it does not require
   admin rights.
3. If both install, continue with the ordinary [`windows.md`](windows.md)
   guide from step 4.

**If pip fails** in step 7 of that guide with errors mentioning SSL,
certificates, a proxy, or a connection timeout, your network is intercepting
downloads. This is normally the end of the road for a local setup — note the
exact error, switch to Colab, and send us the error text. There are
workarounds, but they need details of your network that we will have to look
at together.

## Option 3 — portable Python

If installers are blocked entirely, [WinPython](https://winpython.github.io/)
is a complete Python that runs from a folder without being installed. Download
it, unzip it somewhere you can write to (your user folder, or a USB drive),
and use the **WinPython Command Prompt** inside the folder as your terminal.
It includes the scientific libraries the course needs.

This works, but it is the fiddliest option, and version mismatches are more
likely. If you use it, say so when you submit your setup check.

## Option 4 — GitHub Codespaces

[`codespaces.md`](codespaces.md). Nothing to install; a browser and a free
GitHub account are the whole requirement. This is the best of the
no-installation routes, because you still get a terminal, files, and a
virtual environment, so every command in the course works as written.

## Option 5 — Colab

[`colab-fallback.md`](colab-fallback.md). Use this if a GitHub account is not
possible for you. Everything in the course can be done there, and the guide
covers the differences.

---

Whichever option you end up on, **tell us during the pre-work period**, not on
the morning of the first session. A student we know about is a five-minute
conversation; a surprise is half a session.
