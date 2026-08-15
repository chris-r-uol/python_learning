# Setup — GitHub Codespaces

A Codespace is a computer that GitHub runs for you. Everything for this
course is already installed on it. You work in your web browser.

There is nothing to install and nothing for your laptop to block.

Use this if installing Python on your own machine did not work. You get a
real terminal, real files and a real virtual environment, so every command
in the course works as written.

You need a free GitHub account. That is all.

---

## 1. Start your Codespace

1. Open the course repository on GitHub.
2. Click the green **Code** button.
3. Choose the **Codespaces** tab.
4. Click **Create codespace on main**.

The first start takes two to four minutes. It is building your environment
and installing the packages. Later starts take seconds.

You will then see VS Code in your browser, with the course files on the
left.

## 2. Check it worked

Open a terminal: **Terminal** menu → **New Terminal**.

Your prompt starts with `(.venv)`. The virtual environment is already
created and active.

Run the setup check:

```
python check_setup.py
```

It should report `Running on: GitHub Codespaces` and `ALL CHECKS PASSED`.

**If it says "no virtual environment is active"**, there are two causes:

1. The setup step was still running when your terminal opened. Close the
   terminal, open a new one, and run the check again. This is the usual
   cause.
2. Your Codespace was created before the course configuration was added.
   Press **F1**, type `Rebuild Container`, and choose **Codespaces: Rebuild
   Container**. Your files are kept.

## 3. Working in your Codespace

Every command in the course works as written:

```
cd week1_setup
python first_script.py
```

- **Edit a file:** click it in the sidebar. It opens in the editor and saves
  automatically.
- **Your work is saved.** Close the browser tab and return tomorrow.
  Everything is where you left it.
- **See a figure:** when a script saves a `.png`, it appears in the sidebar.
  Click it.
- **Run the week 5 web app:** run `streamlit run app.py`. The Codespace
  offers a link to open it in a browser tab.

## 4. Stopping it, and your free hours

Every free GitHub account gets Codespaces hours each month. At the time of
writing that is 120 core-hours. This course uses 2 cores, so you get about
60 hours per month. The course needs far less.

The GitHub Student Developer Pack gives you more. Your usage is shown at
github.com/settings/billing.

Two habits keep you inside the limit:

- **Stop your Codespace when you finish.** Go to github.com/codespaces and
  choose **Stop codespace**. A stopped Codespace uses no hours and keeps
  your files.
- It stops itself after 30 minutes of inactivity.

## 5. Getting your work out

A Codespace is already a Git repository. The commands from the project brief
work in its terminal: `git status`, `git add .`, `git commit`.

One thing to know about `git push`. Your Codespace was started from the
course repository, which you cannot write to. The first time you push,
GitHub offers to create a **fork**, which is your own copy. Accept it. Your
saved versions then go to your copy.

To keep files on your own machine, right-click a file or folder in the
sidebar and choose **Download**.

---

## Before you choose this route

- **You need an internet connection.** The Codespace runs on GitHub's
  computers.
- **It is a Linux machine.** Use `ls`, not `dir`.
- **A Codespace is deleted after 30 days of no use.** Push your work to Git.
- **From mainland China**, GitHub can be slow. If you will work from China
  during the course, install locally instead. See
  [`chinese-services.md`](chinese-services.md).
