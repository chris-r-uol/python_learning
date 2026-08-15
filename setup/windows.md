# Setup — Windows

This guide sets up your machine for the course. It takes about 45 minutes.
Follow the steps in order. Do not skip the checks.

If a step fails, read the error, then read the "If this fails" notes under
that step. If you are still stuck after 30 minutes, use
[Codespaces](codespaces.md) instead. It needs no installation.

> Steps marked **[screenshot]** have a picture in the session slides. If
> your screen does not match the description, stop and ask.

---

## 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/). Download
   the latest Python for Windows. Any version from 3.11 upwards works.
2. Run the installer.
3. **On the first screen, tick "Add python.exe to PATH".** [screenshot] This
   checkbox causes most week 1 problems. If you missed it, run the installer
   again and choose "Modify".
4. Click "Install Now". Wait for it to finish.

**Check it worked.** Open a *new* terminal. Press the Windows key, type
`terminal`, press Enter. Then run:

```
python --version
```

You should see something like `Python 3.12.4`.

**If this fails:**

- *"'python' is not recognized"* — the PATH box was not ticked. Run the
  installer again, choose "Modify", and tick "Add Python to environment
  variables". Then open a **new** terminal. Old terminal windows do not see
  the change.
- *The Microsoft Store opens* — Windows has taken over the command. Open the
  Start menu, search for "Manage app execution aliases", and switch **off**
  `python.exe` and `python3.exe`. Open a new terminal and try again.

## 2. Do not use the Microsoft Store Python

If you installed Python from the Microsoft Store, uninstall it. Install from
python.org instead, as above. The Store version stores files in unusual
places and causes problems later. The setup check detects it.

## 3. Install VS Code

1. Download VS Code from
   [code.visualstudio.com](https://code.visualstudio.com/). Run the
   installer. The default options are correct.
2. Open VS Code. Click the Extensions icon on the left edge. It looks like
   four squares. [screenshot]
3. Search for **Python**. Install the extension published by Microsoft.

## 4. Get the course folder

Download the course folder and unzip it. Put it somewhere simple, such as
`Documents\python_learning`.

Avoid OneDrive folders. OneDrive sometimes locks files while Python is using
them.

## 5. Open a terminal in the course folder

Use either method:

- In File Explorer, open the course folder. Right-click empty space. Choose
  **Open in Terminal**.
- In VS Code, choose File → Open Folder, then Terminal → New Terminal.

**Check it worked.** Run:

```
dir
```

You should see `check_setup.py` in the list. If you do not, you are in the
wrong folder. Fix this now. The wrong folder causes most errors in week 1.

## 6. Create and activate a virtual environment

A virtual environment is a private copy of Python for this course. Packages
you install cannot affect anything else on your machine.

Create it once:

```
python -m venv .venv
```

Activate it:

```
.venv\Scripts\activate
```

**Check it worked.** Your prompt now starts with `(.venv)`.

**If this fails:**

- *"running scripts is disabled on this system"* — PowerShell is blocking
  the script. Run this once and answer `Y`:

  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

  Then activate again. If your machine blocks that too, open Command Prompt
  instead of PowerShell. Use the dropdown in the terminal panel. Then run
  `.venv\Scripts\activate.bat`.

**Activate the environment every time you open a new terminal.** If you do
not see `(.venv)`, it is not active.

## 7. Install the course packages

With the environment active:

```
pip install -r requirements.txt
```

This takes a few minutes.

**If this fails** with an error about SSL, certificates or a proxy, your
network is blocking the download. Use [Codespaces](codespaces.md) instead.
It runs on GitHub's machines, so your network cannot block it.

## 8. Run the setup check

In the course folder, with the environment active:

```
python check_setup.py
```

Read the result. If it reports a problem, it also names the fix.

## 9. Install Git

Git saves versions of your work. You can return to any saved version. You
need it from week 4. Installing it now saves time.

1. Download Git from [git-scm.com](https://git-scm.com/download/win). Run
   the installer. The default options are correct.
2. Open a new terminal. Set your name and email. Git attaches them to your
   saved versions.

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

**Setup is complete.** Keep this guide. The activate command in step 6 is
the one people forget.
