"""tinyeval worker for the support bot. In evals/support.sh:

    worker uv run python -m evals.worker

It reads each input up to a NUL byte and prints the reply and a NUL byte,
so the app starts once per worker, not once per test case.
"""

import sys

import anthropic

from app.support import answer, client  # the import builds the client once


def reply(message: str) -> str:
    # When the cause isn't the app (no key, a bad key, a rate limit, a server error,
    # a timeout or the network), tinyeval counts the test case as couldn't run.
    # Any other API error, like a bad model name, is the reply, so the eval fails.
    if not (client.api_key or client.auth_token or client.credentials):
        return "#tinyeval couldnt_run ANTHROPIC_API_KEY isn't set\n"
    try:
        return answer(message)
    except anthropic.APIStatusError as e:
        if e.status_code in (401, 429) or e.status_code >= 500:
            return f"#tinyeval couldnt_run anthropic: {e.status_code} {type(e).__name__}\n"
        return f"anthropic: {e}"
    except anthropic.APIConnectionError as e:  # APITimeoutError is one too
        return f"#tinyeval couldnt_run anthropic: {type(e).__name__}\n"


def main() -> None:
    rest = b""
    while chunk := sys.stdin.buffer.read1():
        *inputs, rest = (rest + chunk).split(b"\0")
        for message in inputs:
            sys.stdout.buffer.write(reply(message.decode()).encode() + b"\0")
            sys.stdout.buffer.flush()


if __name__ == "__main__":
    main()
