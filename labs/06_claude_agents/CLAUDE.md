# Lab 06 — Claude agents

Claude Code reads this file at the start of every session in this folder. It is
project memory: short facts and rules, not a tutorial.

## What is here
- `sample.csv`: 15 employees (name, age, salary, department, years_experience)
- `primes.py`: a small script with some deliberate problems, for the code-review skill
- `mcp_server/server.py`: the lab's MCP server (`lab-tools`)
- `starter/skill.md`: a plain prompt file that lab step 2 turns into a skill
- `api/`: a math-tutor agent on the Claude API, written with and without the Tool Runner

## Rules
- Treat `sample.csv` as read-only data. Never edit or delete it.
- Never read `.env` files.
- When you give a number, say which tool or command produced it.
