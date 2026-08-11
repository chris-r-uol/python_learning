# Setup — using Chinese services

Many students on this course are from China, and many prefer the services
they already use at home. That is fine. Nothing in this course requires a
Western account, a Western AI assistant, or a Western search engine — this
page says what works, service by service, so you do not have to find out by
trial and error.

The short version: **the course teaches a method, not a product.** Specify
precisely, generate one piece at a time, verify against a case you can check
by hand. That method works identically with every assistant on this page.

---

## AI assistants

From week 3 onwards you work with an AI assistant. The in-class
demonstrations use whichever assistant the university licenses, but for your
own work any capable assistant is acceptable, and the Chinese services are
fully capable of everything this course asks:

| Service | Where | Worth knowing |
|---|---|---|
| **DeepSeek** (深度求索) | chat.deepseek.com | Free, and very strong at code. If you want one recommendation from this list, this is it. |
| **Kimi** (Moonshot) | kimi.moonshot.cn | Popular with students; handles long documents well — useful when pasting large error output. |
| **Tongyi Qianwen** (通义千问, Alibaba) | tongyi.aliyun.com | Strong general assistant. |
| **Ernie Bot** (文心一言, Baidu) | yiyan.baidu.com | Baidu's assistant. |
| **Doubao** (豆包, ByteDance) | doubao.com | Widely used; capable for course-level code. |

Practical notes:

- These services usually sign in with a **+86 phone number or WeChat** — for
  most of you that is easier than creating a new Western account, which is
  exactly why this page exists.
- All of them are reachable from the UK without any special arrangement.
- Pick one and stay with it for the rest of the course. The skill you are
  building — specifying and verifying — transfers between assistants, but
  switching mid-project costs you the feel you have developed for how yours
  behaves.

**One rule applies whatever you choose:** the verification checklist from
week 3 is not optional with any assistant, Chinese or Western. Every one of
them produces confident, plausible, wrong answers in exactly the way the
week 3 demonstration shows, and the checks are how you catch it.

## Prompting in Chinese

Prompt in whichever language you specify most precisely in. A specification
written in clear Chinese is worth more than a vague one written in English —
the code comes back in Python either way. Asking the assistant to *explain
code in Chinese* is also a legitimate and excellent use of it: "逐行解释这段
代码" ("explain this code line by line") is exactly check 4 of the
verification checklist, in the language you think fastest in.

Two things should stay in English: the **names in your code** (variables,
functions, comments), because your work will be read in the gallery and
shared with people who read English; and the **three sentences per chapter**
in your atlas, for the same reason. Your `prompts.md` record may be in
Chinese — it is a record of what you actually did.

## Search and learning resources

Baidu works fine for finding things, with one caution: Python answers on
Chinese forums are sometimes several versions out of date. Two resources
worth knowing instead:

- **The official Python documentation, in Chinese:**
  [docs.python.org/zh-cn/3/](https://docs.python.org/zh-cn/3/) — a full,
  official translation, always current.
- **Liao Xuefeng's Python tutorial** (廖雪峰) and **runoob** (菜鸟教程) — the
  two standard Chinese-language Python learning sites. Good for a second
  explanation of anything from weeks 1–2, in Chinese.

## If you work from China during the course

Term breaks happen. If you take the project home, three things change:

- **Google Colab does not work in China.** If you are on the Colab fallback,
  plan around this — or better, get the local setup working before you
  travel; it needs no Google services at all.
- **GitHub Codespaces depends on GitHub**, which is usually reachable from
  China but can be slow or intermittent. It is an excellent option while you
  are in the UK; it is not the one to depend on for a working trip home. A
  local installation is.
- **PyPI and GitHub can be slow or unreliable.** For package installs, the
  Tsinghua mirror is the standard fix:

  ```
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  For GitHub, commit locally as usual and push when the connection
  cooperates; your university VPN, if you have one, usually resolves both.
- **The course data is already on your machine.** The atlas is designed
  cache-first: every data source has a fallback copy in
  `project/data/external/`, and your own fetched copies live in your project
  folder. Fetch everything you need while you are in the UK, and the whole
  project works offline afterwards.

## If you do not have a Google account

Only the Colab fallback needs one. If you would rather not create one, say
so during setup week — the local installation works without any Google
services, and we would rather set that up with you than have you stuck.

---

One more thing, because it is the point of the page: using DeepSeek instead
of the licensed assistant, prompting in Chinese, and reading the
documentation in Chinese are not workarounds or second-best options. They
are you configuring your tools to think at full speed, which is what a
professional does. The only thing this course insists on is what comes
after the generation: that you check.
