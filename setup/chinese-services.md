# Setup — using Chinese services

Many students on this course are from China and prefer the services they use
at home. Nothing in this course requires a Western account, a Western AI
assistant or a Western search engine.

This page lists what works.

---

## AI assistants

From week 3 you work with an AI assistant. The class demonstrations use the
assistant the university licenses. For your own work, any capable assistant
is fine. The Chinese services below can do everything this course asks.

| Service | Where | Notes |
|---|---|---|
| **DeepSeek** (深度求索) | chat.deepseek.com | Free and strong at code. Choose this one if you are unsure. |
| **Kimi** (Moonshot) | kimi.moonshot.cn | Handles long documents well. Useful for long error messages. |
| **Tongyi Qianwen** (通义千问, Alibaba) | tongyi.aliyun.com | Strong general assistant. |
| **Ernie Bot** (文心一言, Baidu) | yiyan.baidu.com | Baidu's assistant. |
| **Doubao** (豆包, ByteDance) | doubao.com | Widely used and capable. |

Notes:

- Most sign in with a **+86 phone number or WeChat**. For many of you this
  is easier than creating a new account.
- All of them work from the UK with no special setup.
- Choose one and keep using it. Switching often costs you time.

The week 3 checklist applies to every assistant. All of them produce
answers that look right and are wrong.

## Prompting in Chinese

Write your prompt in the language you can be most precise in. A clear
Chinese prompt is better than a vague English one. The code comes back in
Python either way.

Asking the assistant to explain code in Chinese is also useful. "逐行解释这
段代码" means "explain this code line by line". That is check 4 of the
verification checklist.

Keep **variable and function names in English**. Python keywords, library
names and error messages are all in English. Mixing languages in one line
makes it harder to read. It also makes it faster for the TA to help you.

Comments, your `prompts.md` notes and the sentences in your atlas can be in
any language you choose.

## Search and learning

Baidu works for finding answers. One caution: Python answers on Chinese
forums are sometimes several versions out of date.

Two current sources:

- **Python documentation in Chinese:**
  [docs.python.org/zh-cn/3/](https://docs.python.org/zh-cn/3/). A full
  official translation.
- **Liao Xuefeng** (廖雪峰) and **runoob** (菜鸟教程). Both are good for a
  second explanation of anything in weeks 1 and 2.

## Working from China during the course

Four things change:

- **Google Colab does not work in China.** If you use Colab, plan for this.
  A local installation is better, and needs no Google services.
- **GitHub Codespaces depends on GitHub**, which is usually reachable but
  can be slow. Good in the UK. Do not rely on it for a trip home.
- **PyPI and GitHub can be slow.** For package installs, use the Tsinghua
  mirror:

  ```
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  For GitHub, save your work locally and push when the connection allows. A
  university VPN usually solves both.
- **The course data is already on your machine.** Every data source has a
  copy in `project/data/external/`. Download what you need in the UK, and
  the project works offline.

## If you do not have a Google account

Only Colab needs one. A local installation uses no Google services.
[Codespaces](codespaces.md) needs a GitHub account instead. Either route
works.

---

Using DeepSeek instead of the licensed assistant, prompting in Chinese, and
reading documentation in Chinese are all fine. Work in the language you
think fastest in. The course asks one thing of every assistant: check what
it gives you.
