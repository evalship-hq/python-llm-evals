"""tinyeval worker for the support bot. In evals/support.sh:

    worker uv run python -m evals.worker

The app starts once per worker, not once per test case.
"""

from tinyeval import CouldntRun, worker  # before the app, so the app's prints go to stderr

from app.support import answer, client  # the import builds the client once


def reply(message: str) -> str:
    # worker() counts an API error that isn't the app's fault (a bad key, a rate limit, a server error,
    # a timeout or the network) as couldn't run. Any other error, like a bad model name, is the reply, so the eval fails.
    if not (client.api_key or client.auth_token or client.credentials):
        raise CouldntRun("ANTHROPIC_API_KEY isn't set")
    return answer(message)


if __name__ == "__main__":
    worker(reply)
