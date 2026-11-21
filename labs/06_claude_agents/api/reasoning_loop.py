"""A math-tutor agent on the Claude API, with the loop written by hand.

Every agent is the same loop, whatever the framework or provider:

    ask the model -> it asks for a tool -> run it -> send the result back -> repeat

Run:  python api/reasoning_loop.py "What is 15 times 23, then add 10?"
Auth: ANTHROPIC_API_KEY in the environment (or `ant auth login`).
"""

import sys

import anthropic

MODEL = "claude-opus-5-5"
client = anthropic.Anthropic()

SYSTEM = """You are a math tutor who solves problems step by step.
Use the multiply tool for every multiplication, however small.
Explain each step in one short sentence, then give the final answer on its own line."""

# A tool is a name, a description and an input schema. The model never runs
# it: it asks for it, and this program runs it.
TOOLS = [
    {
        "name": "multiply",
        "description": "Multiply two numbers and return the product.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,  # the model's inputs always match the schema
    }
]


def run_tool(name: str, args: dict) -> str:
    if name == "multiply":
        return str(args["a"] * args["b"])
    raise ValueError(f"Unknown tool: {name}")


def solve(problem: str, max_turns: int = 10) -> str:
    messages = [{"role": "user", "content": problem}]

    for turn in range(1, max_turns + 1):
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
            # If a safety classifier declines, retry on a fallback model in the same call.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )

        # Keep the whole assistant turn (text, thinking and tool_use blocks) in the history.
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "refusal":
            return "The model declined this request."
        if response.stop_reason != "tool_use":
            # No tool requested: this is the answer.
            return "".join(b.text for b in response.content if b.type == "text")

        # The model asked for one or more tools. Run them all and send every
        # result back in ONE user message.
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                output, failed = run_tool(block.name, block.input), False
            except Exception as e:
                output, failed = f"Error: {e}", True
            print(f"  turn {turn}: {block.name}({block.input}) -> {output}")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": failed,
                }
            )
        messages.append({"role": "user", "content": results})

    return f"Stopped after {max_turns} turns without a final answer."


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "A store sells 15 boxes a day with 24 eggs each. How many eggs in 6 days?"
    print(f"Problem: {question}")
    print(solve(question))
