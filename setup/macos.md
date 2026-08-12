# Setup — macOS

This guide takes you from a bare Mac to a working course setup. It takes most
people 30 to 45 minutes. Follow the steps in order, and do not skip the
checks — each one confirms that the step before it worked.

If a step fails, do not spend your evening fighting it. Copy the error message,
note which step you were on, and send us that instead of the check output.
We will fix it with you before the first session.

---

## 1. Install Python

Your Mac already has a version of Python on it. **Do not use it.** It belongs
to the operating system, it cannot install packages properly, and Apple can
change it without warning. The course's check script detects it by its location
and will tell you if you are using it by mistake.

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   the latest Python for macOS. Any version from 3.11 upwards is fine.
2. Open the downloaded file and follow the installer. The default options are
   fine.
3. When the installer finishes, it opens a Finder window containing a file
   called **Install Certificates.command**. Double-click it and let it run.
   This step is easy to miss and skipping it causes confusing "certificate
   verify failed" errors when Python downloads anything later.

**Check it worked.** Open Terminal (press Cmd-Space, type `terminal`, press
Enter) and run:

```
python3 --version
```

You should see something like `Python 3.12.4`.

One thing to know from the start: on macOS the command is **`python3`**, not
`python`. Typing `python` on a fresh Mac either fails or finds the wrong
Python. Once your virtual environment is active (step 5), plain `python` is
safe — until then, always type `python3`.

**If this fails:**

- *"command not found: python3"* — the installer did not finish, or you are in
  a terminal window that was open before the install. Close the terminal, open
  a new one, and try again. If it still fails, run the installer again.

## 2. Install VS Code

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/).
2. Open the downloaded file and drag **Visual Studio Code** into your
   **Applications** folder, then open it from there.
3. On the left-hand edge, click the Extensions icon (four squares), search for
   **Python**, and install the extension published by Microsoft.

## 3. Get the course folder

Download the course folder from the link you were given, and unzip it somewhere
sensible — for example a `projects` folder inside your home folder. Avoid
iCloud-synced locations such as Desktop and Documents if your Mac "optimises"
storage; files that are not really on the disk cause puzzling errors.

## 4. Open a terminal in the course folder

Two ways; use whichever you prefer:

- In Finder, right-click the course folder and choose
  **New Terminal at Folder** (if you do not see it, it is in
  System Settings → Keyboard → Keyboard Shortcuts → Services).
- In VS Code, open the folder (File → Open Folder), then open the built-in
  terminal (Terminal → New Terminal).

**Check it worked.** Run `ls` and confirm you can see `check_setup.py` in the
listing. If you cannot, you are in the wrong folder — worth fixing now, because
"wrong folder" is the most common cause of errors in week 1.

Two commands worth knowing: `cd foldername` moves you into a folder, and `ls`
lists what is in the current one. That is most of the terminal knowledge this
course needs.

## 5. Create and activate a virtual environment

A virtual environment is a private copy of Python for this course, so that the
packages we install cannot interfere with anything else on your machine. You
create it once, and activate it each time you work.

Create it (this takes a minute):

```
python3 -m venv .venv
```

Activate it:

```
source .venv/bin/activate
```

**Check it worked.** Your prompt now starts with `(.venv)`, and from here on
plain `python` refers to the right Python.

Remember: **every time** you open a new terminal to work on the course, run the
activate command again. If the `(.venv)` prefix is missing, you are not in the
environment.

## 6. Install the course packages

With the environment active:

```
pip install -r requirements.txt
```

This downloads the libraries the course uses. It can take a few minutes.

**If this fails** with an error mentioning SSL or certificates, go back and run
**Install Certificates.command** from step 1. If it fails with an error
mentioning a proxy, you are probably on a managed network — see
[`locked-down-laptop.md`](locked-down-laptop.md), and tell us.

## 7. Run the setup check

Still in the course folder, with the environment active:

```
python check_setup.py
```

Copy everything it prints and send it to us. If it reports problems, send
that output — it is designed to tell us exactly what to fix, and that is just as
useful as a pass.

## 8. Install Git (needed from week 4)

Git keeps a history of your own work and lets you get back to any version
that worked. You do not need it in weeks 1 to 3, but setting it up now saves
time later.

macOS installs Git the first time you ask for it. Run:

```
git --version
```

If a dialog offers to install the "command line developer tools", accept, and
wait for it to finish. Then introduce yourself to Git (use your real name and
email; they are attached to your work):

```
git config --global user.name "Your Name"
```

```
git config --global user.email "you@example.com"
```

The handful of commands you will actually use — `status`, `add`, `commit`,
`log`, `restore`, and `push` — are taught in the project brief, in the
section "Saving your progress with Git", at the point you need them.

---

**You are done.** Keep this guide; the activate command in step 5 is the one
line people forget.
