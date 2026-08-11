# Fallback — Google Colab

> **Consider Codespaces first.** [`codespaces.md`](codespaces.md) also
> requires no installation, and it keeps the terminal, the files, and the
> virtual environment — so nothing from week 1 is lost and every command in
> the course works exactly as written. Use this Colab guide if a GitHub
> account is not possible for you, or if you already know Colab and prefer
> it.

If a local setup did not work out, you will use Google Colab: a free service
that runs Python in your web browser, on Google's computers. Nothing needs to
be installed on your machine.

Two things to say clearly at the start:

- **You are not behind and you are not getting a lesser course.** Everything
  the course asks for can be done in Colab, and some professional data work
  happens there by choice.
- There are a few real differences from a local setup, listed at the end.
  Read them once so they do not surprise you.

You need a Google account. If you do not have one or cannot use one, tell us
and we will sort something out — and note that Colab does not work from
mainland China, so if you expect to spend part of the course there, the
local setup is the resilient choice (see
[`chinese-services.md`](chinese-services.md)).

## 1. Open Colab

Go to [colab.research.google.com](https://colab.research.google.com) and sign
in. Choose **New notebook**.

A notebook is a page of cells. You type a command into a cell and press
Shift-Enter to run it. Commands that would go into a terminal on a local
machine work here too — you put an exclamation mark in front of them, so
`python check_setup.py` becomes `!python check_setup.py`.

## 2. Put the course files somewhere permanent

Colab forgets its local files when a session ends, so the course folder should
live in your Google Drive, which persists.

1. Upload the course folder (unzipped) to your Google Drive, at the top level,
   keeping the folder name `python_learning`.
2. In your notebook, connect Drive by running this in a cell:

   ```
   from google.colab import drive
   drive.mount('/content/drive')
   ```

   A dialog asks for permission; allow it.
3. Move into the course folder:

   ```
   %cd /content/drive/MyDrive/python_learning
   ```

**Check it worked.** Run `!ls` and confirm you can see `check_setup.py`.

## 3. Run the setup check

```
!python check_setup.py
```

Copy everything it prints and submit it, exactly as local students do.

One expected difference: the check will report that no virtual environment is
active. On Colab that is normal — Colab manages the environment for you — and
the message says so. Everything else should pass, because Colab already has
the libraries the course uses.

## 4. Working in Colab through the course

- **Running a course script.** Move to the right folder with `%cd`, then run
  the script with `!python`, for example:

  ```
  %cd /content/drive/MyDrive/python_learning/week1_setup
  !python first_script.py
  ```

- **Editing a course file.** Open the file browser with the folder icon on the
  left edge, find the file under `drive/MyDrive/python_learning`, and
  double-click it. It opens in an editor pane; changes save automatically.
- **Saving your own work.** Keep your files inside the course folder on Drive,
  and they will be there next session.

## What is different, honestly

| Local setup | Colab |
|---|---|
| A terminal | Notebook cells with `!` in front of commands |
| Files on your disk | Files on Google Drive |
| A virtual environment you manage | An environment Google manages |
| Sessions last as long as you like | Sessions time out after idle periods; you reconnect and run the mount cell again |

Because of this, the parts of week 1 about terminals, folders, and virtual
environments will partly not apply to you. That material matters — it is what
makes you employable on machines that are not Colab — so we will run a short
separate catch-up with you rather than leaving the gap. Remind us if we do not
offer it.

## Getting your project out at the end

Your project group will keep its work in a shared repository from week 4. From
Colab, the simple route is: download your files (right-click a file in the
file browser → Download), and add them to the group repository from any
machine with Git — or use Colab's built-in **File → Save a copy in GitHub**
for notebooks. We will help with this in the project weeks; nothing about it
needs solving now.
