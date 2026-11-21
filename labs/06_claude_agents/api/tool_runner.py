"""The same agent with the SDK's Tool Runner: you write the tools, the SDK
writes the loop.

Compare with reasoning_loop.py. The while loop, the tool_result messages and
the stop_reason checks are gone: the runner does them. The tool's name, input
schema and description now come from the function's name, type hints and
docstring, as with LangChain's @tool and the MCP server's @mcp.tool().

Run:  python api/tool_runner.py "What is 15 times 23, then add 10?"
"""

import sys

import anthropic
from anthropic import beta_tool

MODEL = "claude-opus-5-5"
client = anthropic.Anthropic()

SYSTEM = """You are a math tutor who solves problems step by step.
Use the multiply tool for every multiplication, however small.
Explain each step in one short sentence, then give the final answer on its own line."""


@beta_tool
def multiply(a: float, b: float) -> str:
    """Multiply two numbers and return the product.

    Args:
        a: First number.
        b: Second number.
    """
    return str(a * b)


def solve(problem: str) -> str:
    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        max_iterations=10,
        system=SYSTEM,
        tools=[multiply],
        messages=[{"role": "user", "content": problem}],
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    final = None
    for message in runner:  # one message per turn of the loop
        for block in message.content:
            if block.type == "tool_use":
                print(f"  {block.name}({block.input})")
        final = message

    if final is None or final.stop_reason == "refusal":
        return "The model declined this request."
    return "".join(b.text for b in final.content if b.type == "text")


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "A store sells 15 boxes a day with 24 eggs each. How many eggs in 6 days?"
    print(f"Problem: {question}")
    print(solve(question))
