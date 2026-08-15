# Python for Transport & Civil Engineering

**Website: <https://chris-r-uol.github.io/python_learning/>**

The website has the same text as these files, with a search box. Use it
beside your editor.

Five weeks. You will learn to take a transport dataset, clean it, analyse
it, and produce a figure. You will also learn what to do when your code does
not work.

## Start here

Set up your machine before week 1. This takes about 45 minutes.

1. Follow the guide for your machine:
   - Windows → [`setup/windows.md`](setup/windows.md)
   - macOS → [`setup/macos.md`](setup/macos.md)
   - No installation possible → [`setup/codespaces.md`](setup/codespaces.md)
   - Work laptop, no admin rights → [`setup/locked-down-laptop.md`](setup/locked-down-laptop.md)
   - No GitHub account possible → [`setup/colab-fallback.md`](setup/colab-fallback.md)

   If you use Chinese services such as Baidu, DeepSeek or WeChat sign-in,
   also read [`setup/chinese-services.md`](setup/chinese-services.md).

2. In the course folder, with your virtual environment active, run:

   ```
   python check_setup.py
   ```

3. Read what it prints.

### The three results

| Result | Meaning |
|---|---|
| **ALL CHECKS PASSED** | Nothing to do. |
| **READY, WITH NOTES** | Also a pass. Everything needed works. Read the notes. Some are normal, such as "no virtual environment" on Colab. |
| **NOT READY YET** | Something is missing or wrong. The check names each problem and its fix. |

## If something does not work

Try these in order.

1. **Read the message to the end.** It usually names the problem.
2. **Read the "If this fails" notes** in your setup guide. Common problems
   are listed there with their fixes.
3. **Paste the exact error into an AI assistant.** Ask what it means.
   Installation errors are well documented.
4. **Search for the exact error text.**
5. **After 30 minutes, stop. Use [Codespaces](setup/codespaces.md).** It
   needs no installation. It runs in your browser. You lose nothing from the
   course.
6. **Still stuck at the session?** Bring it. The instructor and TA are
   there.

## What is in this folder

| Folder | Contents |
|---|---|
| `setup/` | Installation guides |
| `week1_setup/` | First scripts and the traceback exercises |
| `week2_programming/` | The worked example and the drills |
| `week3_ai/` | The verification checklist and the AI task |
| `project/` | The transport atlas project and the data catalogue |
| `instructor/` | Teaching notes and the answers to weeks 1 and 2 |
| `docs/` | How the course was designed |

The answers are in `instructor/solutions/`. Nothing is graded, so nobody
loses marks by reading them. Use them to check your work after you have
tried a task, or when you are stuck. If you read them first, you get no
practice.

## Three rules

1. **A figure with an unlabelled axis is not finished.** Label both axes.
   Give units. Write a title a stranger can understand.
2. **Code you cannot explain is not finished.** From week 3 you check
   whether your answers are right.
3. **Getting stuck is normal.** Read the error message first.
