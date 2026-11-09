"""A web shop's support bot: one Claude call per customer message."""

from pathlib import Path

import anthropic

PROMPT = (Path(__file__).parent.parent / "prompts" / "support.md").read_text()

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY


def answer(message: str) -> str:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        output_config={"effort": "low"},  # Opus 5.5 always thinks; a short reply needs little
        system=PROMPT,
        messages=[{"role": "user", "content": message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")
