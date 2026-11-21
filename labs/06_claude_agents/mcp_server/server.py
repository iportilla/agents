"""lab-tools: the MCP server for Lab 06 (starter version).

Run by Claude Code over stdio. Register it from the lab folder with:

    claude mcp add --scope project lab-tools -- .venv/bin/python mcp_server/server.py

Each function marked @mcp.tool() becomes one tool. Claude sees three things:
the function name (the tool's name), its typed parameters (the inputs), and the
docstring (the description). The docstring is the only thing Claude knows about
when to use the tool, so write it for a new teammate.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lab-tools")


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression such as '25 * 17' or '(3 + 4) ** 2'
    and return the result. Use this for any arithmetic rather than working it
    out yourself."""
    try:
        # WARNING: deliberately unsafe. Turning off __builtins__ is NOT a
        # sandbox. Step 5 of the lab shows why, and solutions/ has a safe version.
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {e}"


# TODO (lab step 4): add a csv_stats tool here.
# Copy the shape of calculate() above. Spend most of your time on the docstring.


if __name__ == "__main__":
    mcp.run()  # stdio transport: Claude Code starts this process and talks over stdin/stdout
