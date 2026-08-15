# Setup — Google Colab

> **Try [Codespaces](codespaces.md) first.** It also needs no installation,
> and it keeps the terminal, the files and the virtual environment, so every
> command in the course works as written. Use Colab if you cannot have a
> GitHub account, or if you already know Colab and prefer it.

Colab is a free service that runs Python in your web browser, on Google's
computers. You install nothing.

Everything in this course can be done in Colab. A few things work
differently. They are listed at the end.

You need a Google account. If you cannot have one, use
[Codespaces](codespaces.md), which needs a GitHub account instead.

Colab does not work from mainland China. If you will work from China during
the course, install locally. See
[`chinese-services.md`](chinese-services.md).

## 1. Open Colab

Go to [colab.research.google.com](https://colab.research.google.com) and
sign in. Choose **New notebook**.

A notebook is a page of cells. Type a command into a cell and press
Shift-Enter to run it.

Terminal commands work here too. Put an exclamation mark in front. So
`python check_setup.py` becomes `!python check_setup.py`.

## 2. Put the course files in Google Drive

Colab deletes its own files when a session ends. Google Drive keeps them.

1. Upload the course folder to your Google Drive. Put it at the top level.
   Keep the name `python_learning`.
2. In your notebook, run this in a cell to connect Drive:

   ```
   from google.colab import drive
   drive.mount('/content/drive')
   ```

   A window asks for permission. Allow it.
3. Move into the course folder:

   ```
   %cd /content/drive/MyDrive/python_learning
   ```

**Check it worked.** Run `!ls`. You should see `check_setup.py`.

## 3. Run the setup check

```
!python check_setup.py
```

Read what it prints.

The check will say that no virtual environment is active. On Colab this is
normal. Colab manages the environment for you. Everything else should pass,
because Colab already has the packages this course uses.

## 4. Working in Colab

- **Run a course script.** Move to the folder, then run the script:

  ```
  %cd /content/drive/MyDrive/python_learning/week1_setup
  !python first_script.py
  ```

- **Edit a course file.** Click the folder icon on the left edge. Find the
  file under `drive/MyDrive/python_learning`. Double-click it. It opens in
  an editor and saves automatically.
- **Save your own work.** Keep your files inside the course folder on Drive.

## What is different

| Local setup | Colab |
|---|---|
| A terminal | Notebook cells, with `!` before commands |
| Files on your disk | Files on Google Drive |
| A virtual environment you manage | An environment Google manages |
| Sessions last as long as you like | Sessions stop when idle. Reconnect and run the mount cell again |

Parts of week 1 cover terminals, folders and virtual environments. You
cannot run those commands in Colab. Read those sections anyway. You will
need them on any machine that is not Colab.

## Getting your files out

Your atlas is yours to keep, so take a copy at the end. Right-click a file
or folder in the file browser and choose **Download**. For notebooks you can
also use **File → Save a copy in GitHub**.
