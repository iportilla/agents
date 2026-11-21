# From Chat to Agent with Claude

A 60-minute lecture and hands-on lab on how AI agents work, using the Claude app and
Claude Code: models, tools, the agent loop, harnesses, skills, subagents, MCP servers,
and what keeps an agent safe.

## Contents

| Path | What it is |
|---|---|
| Lecture deck | [From Chat to Agent with Claude](https://claude.ai/artifact/VxdYTsrmJ1zVErnfKw6zXz): 18 slides with speaker notes; exports to PowerPoint or PDF |
| [`labs/06_claude_agents/`](labs/06_claude_agents/) | The lab: build a CSV analyst four ways in Claude Code. Start with [`LAB.md`](labs/06_claude_agents/LAB.md) |
| [`legacy/`](legacy/) | Earlier material (LangChain/OpenAI notebooks, the old lecture, the ReAct activity), kept for reference |

## The hour

| Minutes | Section |
|---|---|
| 0–5 | A model only writes text |
| 5–10 | Tools: a name, a description and inputs |
| 10–17 | The agent loop, as a diagram and as code |
| 17–22 | Harnesses: the Claude app and Claude Code |
| 22–30 | Four ways to add abilities: built-in tools, skills, subagents, MCP servers |
| 30–35 | What keeps an agent safe |
| 35–60 | Lab |

## Before class

Students need Claude Code (signed in) and Python 3.10+. In the lab folder:

```bash
cd labs/06_claude_agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The take-home API exercise also needs an Anthropic API key.

## License

MIT. See [LICENSE](LICENSE).
