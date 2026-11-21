"""lab-tools: the MCP server for Lab 06 (solution version).

Differences from the starter:
- calculate() parses the expression with `ast` and allows only numbers and
  arithmetic operators, instead of calling eval().
- csv_stats() is the tool students add in step 4. It only opens .csv files
  inside the lab folder, whatever path the model passes.

The input checks live here, in the server, not in a prompt: the model can be
talked out of an instruction, but it can't get past code it doesn't control.
"""

import ast
import operator
from pathlib import Path
from typing import Optional

import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lab-tools")

LAB_DIR = Path(__file__).resolve().parent.parent

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError(f"not allowed: {type(node).__name__}")


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression such as '25 * 17' or '(3 + 4) ** 2'
    and return the result. Supports + - * / // % ** and parentheses on numbers
    only. Use this for any arithmetic rather than working it out yourself."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval")))
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def csv_stats(path: str, column: str, group_by: Optional[str] = None) -> str:
    """Compute summary statistics (count, mean, min, max) for one numeric column
    of a CSV file in the lab folder, for example column='salary' in
    'sample.csv'. Set group_by to a column name such as 'department' to get one
    row of statistics per group. Use this instead of reading the whole file
    when the question asks for an average, total, minimum, maximum or count."""
    target = (LAB_DIR / path).resolve()
    if target.suffix != ".csv" or LAB_DIR not in target.parents:
        return "Error: only .csv files inside the lab folder can be read."
    if not target.exists():
        return f"Error: {path} not found."

    df = pd.read_csv(target)
    for name in [column] + ([group_by] if group_by else []):
        if name not in df.columns:
            return f"Error: no column '{name}'. Columns: {', '.join(df.columns)}"
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Error: column '{column}' is not numeric."

    stats = ["count", "mean", "min", "max", "sum"]
    if group_by:
        table = df.groupby(group_by)[column].agg(stats).round(2)
        return f"{column} by {group_by} in {path}:\n{table.to_string()}"
    row = df[column].agg(stats).round(2)
    return f"{column} in {path}:\n{row.to_string()}"


if __name__ == "__main__":
    mcp.run()
