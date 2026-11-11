# LLM evals for Python

A Python support bot whose AI call is tested on every pull request with [tinyeval](https://tinyeval.com).

## Run it

Clone this repo or use it as a template. You need [uv](https://docs.astral.sh/uv/). Then:

```sh
uv sync
export ANTHROPIC_API_KEY=sk-ant-...
uv run tinyeval
```

```
support
  ✓ refund after the window 15.6s
  ✓ missing package 14.1s
  ✓ refund inside the window 14.2s

All 3 evals passed (eval-results.json)
```

## What's here

- `app/support.py`: the bot. `answer(message)` calls Claude with the official `anthropic` package.
- `prompts/support.md`: the system prompt.
- `evals/worker.py`: builds the client once and answers each test case with tinyeval's worker helper.
- `evals/support.sh`: three test cases, each checked by a regex, a judge or both.
- `pyproject.toml` and `uv.lock`: the dependencies, locked. tinyeval is a dev dependency.
- `.github/workflows/evals.yml`: runs the evals on every pull request and push to main.

## Use it for your app

1. Replace `answer` with your AI call. Keep the worker, so your app starts once per worker and not once per test case.
2. Write your test cases in `evals/`. The [check lines](https://github.com/evalship-hq/tinyeval#writing-evals) cover regexes, JSON, your own graders and a model judge.
3. In a FastAPI or Django app, set up what your AI call needs once in the worker, then call your function in the loop. For Django, set `DJANGO_SETTINGS_MODULE` and call `django.setup()` before you import your models. The worker's stdout carries the replies, so send logs to stderr.

When the API call fails for a reason that isn't your code, such as a missing key, a rate limit or a timeout, tinyeval counts the test case as couldn't run, apart from the failures. Raise `CouldntRun` for your own such cases. A bug in your code is the reply, so the eval fails.

## In CI

Add `ANTHROPIC_API_KEY` as a repository secret. The bot and tinyeval's judge both use it. The workflow installs the locked dependencies with uv, then runs each test case 3 times. A failing eval fails the job, so it can gate merges. The results upload as the `eval-results` artifact. Without the secret, the eval step is skipped with a notice. Dependabot pull requests get no secrets, so they skip it too.

## Updating tinyeval

Dependabot opens a pull request for each new tinyeval release. To update by hand, run `uv lock --upgrade-package tinyeval-cli`.

## Compare pull requests with main

A fresh CI run has no earlier run to compare with. [evalship](https://evalship.com) reads `eval-results.json`, compares each pull request with main, tells flaky evals from real drops and comments on the pull request.

## License

MIT
