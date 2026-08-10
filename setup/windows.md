# Setup — Windows

This guide takes you from a bare Windows machine to a working course setup. It
takes most people 30 to 45 minutes. Follow the steps in order, and do not skip
the checks — each one confirms that the step before it worked.

If a step fails, do not spend your evening fighting it. Copy the error message,
note which step you were on, and submit that instead of the check output. We
will fix it with you before the first session.

> Screenshots for each step are marked **[screenshot]**. If your screen does not
> match the description, stop and ask rather than guessing.

---

## 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download
   the latest Python for Windows. Any version from 3.11 upwards is fine.
2. Run the installer.
3. **On the first screen, tick the box that says "Add python.exe to PATH".**
   [screenshot] This single checkbox prevents the most common failure in the
   whole course. If you clicked past it, run the installer again — it will let
   you repair the installation.
4. Click "Install Now" and wait for it to finish.

**Check it worked.** Open a *new* terminal (press the Windows key, type
`terminal`, press Enter) and run:

```
python --version
```

You should see something like `Python 3.12.4`.

**If this fails:**

- *"'python' is not recognized"* — the PATH box was not ticked. Run the
  installer again, choose "Modify", and tick "Add Python to environment
  variables". Then open a **new** terminal window; old windows do not see the
  change.
- *The Microsoft Store opens instead* — Windows has intercepted the command.
  Search the Start menu for "Manage app execution aliases" and switch **off**
  the two entries for `python.exe` and `python3.exe`. Then open a new terminal
  and try again.

## 2. Do not use the Microsoft Store version of Python

If you already installed Python from the Microsoft Store, uninstall it and
install from python.org as described above. The Store version keeps its files
in unusual places and causes confusing failures later. The course's check
script detects it and will tell you if you have it.

## 3. Install VS Code

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
   and run the installer. The default options are fine.
2. Open VS Code. On the left-hand edge, click the Extensions icon (four
   squares). [screenshot]
3. Search for **Python**, and install the extension published by Microsoft.

## 4. Get the course folder

Download the course folder from the link you were given, and unzip it somewhere
sensible — for example `Documents\python_learning`. Avoid OneDrive-synced
folders if you can; syncing sometimes locks files while Python is using them.

## 5. Open a terminal in the course folder

Two ways; use whichever you prefer:

- In File Explorer, open the course folder, right-click on empty space, and
  choose **Open in Terminal**.
- In VS Code, open the folder (File → Open Folder), then open the built-in
  terminal (Terminal → New Terminal).

**Check it worked.** Run `dir` and confirm you can see `check_setup.py` in the
listing. If you cannot, you are in the wrong folder — this is worth fixing now,
because "wrong folder" is the most common cause of errors in week 1.

## 6. Create and activate a virtual environment

A virtual environment is a private copy of Python for this course, so that the
packages we install cannot interfere with anything else on your machine. You
create it once, and activate it each time you work.

Create it (this takes a minute):

```
python -m venv .venv
```

Activate it:

```
.venv\Scripts\activate
```

**Check it worked.** Your prompt should now start with `(.venv)`.

**If this fails:**

- *"running scripts is disabled on this system"* — PowerShell is blocking the
  activation script. Run this once, answer `Y`, then try activating again:

  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

  If your machine will not allow that either, use the Command Prompt instead of
  PowerShell (in the terminal's dropdown menu choose "Command Prompt") and run
  `.venv\Scripts\activate.bat`.

Remember: **every time** you open a new terminal to work on the course, run the
activate command again. If the `(.venv)` prefix is missing, you are not in the
environment.

## 7. Install the course packages

With the environment active:

```
pip install -r requirements.txt
```

This downloads the libraries the course uses. It can take a few minutes.

**If this fails** with an error mentioning SSL, certificates, or a proxy, you
are probably on a managed or corporate network — see
[`locked-down-laptop.md`](locked-down-laptop.md), and tell us.

## 8. Run the setup check

Still in the course folder, with the environment active:

```
python check_setup.py
```

Copy everything it prints and submit it. If it reports problems, submit that
output — it is designed to tell us exactly what to fix, and that is just as
useful as a pass.

## 9. Install Git (needed from week 4)

Git is the tool the project weeks use to share code within your group. You do
not need it in weeks 1 to 3, but installing it now saves time later.

1. Download Git from [git-scm.com](https://git-scm.com/download/win) and run
   the installer. The default options are fine.
2. Open a new terminal and introduce yourself to it (use your real name and
   email; they are attached to your work):

```
git config --global user.name "Your Name"
```

```
git config --global user.email "you@example.com"
```

The handful of commands you will actually use — `clone`, `status`, `add`,
`commit`, `push`, `pull` — are covered in the project brief when you need them.

---

**You are done.** Keep this guide; the activate command in step 6 is the one
line people forget.
