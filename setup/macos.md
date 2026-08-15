# Setup — macOS

This guide sets up your machine for the course. It takes about 45 minutes.
Follow the steps in order. Do not skip the checks.

If a step fails, read the error, then read the "If this fails" notes under
that step. If you are still stuck after 30 minutes, use
[Codespaces](codespaces.md) instead. It needs no installation.

---

## 1. Install Python

Your Mac already has Python. **Do not use it.** It belongs to the operating
system. It cannot install packages properly. The setup check detects it and
tells you.

1. Go to [python.org/downloads](https://www.python.org/downloads/). Download
   the latest Python for macOS. Any version from 3.11 upwards works.
2. Open the file and follow the installer. The default options are correct.
3. When it finishes, a Finder window opens. It contains a file called
   **Install Certificates.command**. Double-click it and let it run.

Step 3 is easy to miss. If you skip it, Python cannot download files later
and you get "certificate verify failed" errors.

**Check it worked.** Open Terminal. Press Cmd-Space, type `terminal`, press
Enter. Then run:

```
python3 --version
```

You should see something like `Python 3.12.4`.

On macOS the command is **`python3`**, not `python`. Typing `python` finds
the wrong Python, or nothing. After you activate your virtual environment in
step 5, plain `python` is correct.

**If this fails:**

- *"command not found: python3"* — the installer did not finish, or your
  terminal was open before you installed. Close the terminal, open a new
  one, and try again.

## 2. Install VS Code

1. Download VS Code from
   [code.visualstudio.com](https://code.visualstudio.com/).
2. Open the file. Drag **Visual Studio Code** into your **Applications**
   folder. Open it from there.
3. Click the Extensions icon on the left edge. It looks like four squares.
   Search for **Python**. Install the extension published by Microsoft.

## 3. Get the course folder

Download the course folder and unzip it. Put it somewhere simple, such as a
`projects` folder inside your home folder.

Avoid Desktop and Documents if your Mac uses iCloud storage optimisation.
Files that are not really on the disk cause errors.

## 4. Open a terminal in the course folder

Use either method:

- In Finder, right-click the course folder. Choose **New Terminal at
  Folder**. If you do not see this option, turn it on in System Settings →
  Keyboard → Keyboard Shortcuts → Services.
- In VS Code, choose File → Open Folder, then Terminal → New Terminal.

**Check it worked.** Run:

```
ls
```

You should see `check_setup.py` in the list. If you do not, you are in the
wrong folder. Fix this now. The wrong folder causes most errors in week 1.

Two commands do most of the work: `cd foldername` moves into a folder, and
`ls` lists what is in the current folder.

## 5. Create and activate a virtual environment

A virtual environment is a private copy of Python for this course. Packages
you install cannot affect anything else on your machine.

Create it once:

```
python3 -m venv .venv
```

Activate it:

```
source .venv/bin/activate
```

**Check it worked.** Your prompt now starts with `(.venv)`. From now on,
plain `python` uses the correct Python.

**Activate the environment every time you open a new terminal.** If you do
not see `(.venv)`, it is not active.

## 6. Install the course packages

With the environment active:

```
pip install -r requirements.txt
```

This takes a few minutes.

**If this fails** with an error about SSL or certificates, run **Install
Certificates.command** from step 1. If the error mentions a proxy, your
network is blocking the download. Use [Codespaces](codespaces.md) instead.

## 7. Run the setup check

In the course folder, with the environment active:

```
python check_setup.py
```

Read the result. If it reports a problem, it also names the fix.

## 8. Install Git

Git saves versions of your work. You can return to any saved version. You
need it from week 4. Installing it now saves time.

macOS installs Git when you first ask for it. Run:

```
git --version
```

If a window offers to install the "command line developer tools", accept it
and wait. Then set your name and email. Git attaches them to your saved
versions.

```
git config --global user.name "Your Name"
```

```
git config --global user.email "you@example.com"
```

You will use six commands: `status`, `add`, `commit`, `log`, `restore` and
`push`. The project brief teaches them in the section "Saving your progress
with Git".

---

**Setup is complete.** Keep this guide. The activate command in step 5 is
the one people forget.
