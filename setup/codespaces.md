# Setup — GitHub Codespaces (no installation at all)

If installing Python on your own machine has not worked, use this. A
**Codespace** is a computer that GitHub runs for you, with everything for
this course already installed. You work in it through your web browser.
There is nothing to install, nothing to configure, and nothing that your
laptop's restrictions can block.

This is the recommended route for anyone still stuck after trying their
operating system's guide. It is not a lesser version of the course: unlike
some browser-based options, a Codespace gives you a **real terminal, real
files, and a real virtual environment**, so every command in every week of
this course works exactly as written.

You need a free GitHub account. That is the only requirement.

---

## 1. Start your Codespace

1. Go to the course repository on GitHub.
2. Click the green **Code** button.
3. Choose the **Codespaces** tab.
4. Click **Create codespace on main**.

The first launch takes two to four minutes, because it is building your
environment and installing the course packages. Later launches take seconds.

When it finishes you are looking at VS Code, in your browser, with the
course files in the sidebar — the same editor described in the other setup
guides.

## 2. Check it worked

Open a terminal inside it: the **Terminal** menu → **New Terminal**.

Your prompt should begin with `(.venv)`. That is the virtual environment,
already created and already activated for you.

Now run the setup check:

```
python check_setup.py
```

Copy everything it prints and send it to us, exactly as students on laptops do.
It should report `Running on: GitHub Codespaces` and `ALL CHECKS PASSED`.

**If it says "no virtual environment is active":** the check itself will
tell you which of the two causes applies, but in short —

1. The setup step was still finishing when your terminal opened. Close the
   terminal, open a new one, and run the check again. This is the usual
   explanation and it costs you ten seconds.
2. Your Codespace was created before the course configuration existed in
   the repository. Existing Codespaces do not pick up a new configuration
   on their own. Press **F1**, type `Rebuild Container`, and choose
   **Codespaces: Rebuild Container**. Your files are kept. Alternatively,
   delete the Codespace at github.com/codespaces and create a fresh one.

Note that "READY, WITH NOTES" is a pass — see the verdict table in the main
README. On Codespaces, though, you should be able to reach a clean
`ALL CHECKS PASSED`, so it is worth resolving the note rather than
ignoring it.

## 3. Working in your Codespace

Everything in the course guides works unchanged:

```
cd week1_setup
python first_script.py
```

- **Editing files:** click a file in the sidebar; it opens in the editor and
  saves automatically.
- **Your work is saved.** A Codespace keeps your files between sessions, in
  the same way a laptop does. Close the browser tab and come back tomorrow;
  everything is where you left it.
- **Figures:** when a script saves a `.png`, it appears in the sidebar.
  Click it to view.
- **The week 5 web app:** if you build the optional Streamlit atlas, run
  `streamlit run app.py` and the Codespace offers you a link to open it in
  a browser tab. This works with no extra setup.

## 4. Stopping it, and the free allowance

GitHub gives every free account a monthly allowance of Codespaces time. At
the time of writing that is **120 core-hours per month**, and this course's
Codespace uses 2 cores — so roughly **60 hours a month**, which is
comfortably more than this course needs. (If you are signed up for the
GitHub Student Developer Pack, you get considerably more. Your current usage
is shown at github.com/settings/billing.)

Two habits keep you well inside it:

- **Stop your Codespace when you finish working.** From the repository's
  Codespaces tab, or by closing the browser tab and using **Stop codespace**
  from github.com/codespaces. A stopped Codespace uses no hours and keeps
  all your files.
- It also stops itself after 30 minutes of inactivity, so a forgotten tab
  will not quietly consume your allowance.

## 5. Getting your work out

A Codespace is already a Git repository, so the snapshot habit from the
project brief — `git status`, `git add .`, `git commit` — works in its
terminal with no setup at all, and it is worth using from week 4 onwards.

One thing to know about `git push`: your Codespace was launched from the
*course* repository, which is not yours to push to. The first time you
push, GitHub notices this and offers to create a **fork** — a copy of the
repository under your own account. Accept, and from then on your snapshots
go to your own copy.

If you would rather keep a copy on your own machine instead, right-click
any file or folder in the sidebar and choose **Download**.

---

## What to know before you choose this route

- **You need an internet connection to work.** The Codespace runs on
  GitHub's computers, not yours.
- **It is a Linux machine**, so use the macOS/Linux commands where a guide
  offers a choice: `ls`, not `dir`.
- **A Codespace is deleted after 30 days of not being used.** Push your work
  to Git, which you would be doing anyway.
- **From mainland China**, GitHub can be slow or intermittent. If you expect
  to work from China during the course, a local installation is the more
  resilient choice — see [`chinese-services.md`](chinese-services.md).

If any of this does not behave as described, tell us during setup week. A
Codespace is the one environment where we can see exactly what you see,
which makes helping you straightforward.
