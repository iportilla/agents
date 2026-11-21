# From Chat to Agent with Claude

A 60-minute lecture and hands-on lab on how AI agents work, using the Claude app and
Claude Code: models, tools, the agent loop, harnesses, skills, subagents, MCP servers,
and what keeps an agent safe.

## Contents

| Path | What it is |
|---|---|
| [`docs/From-Chat-to-Agent-with-Claude.pdf`](docs/From-Chat-to-Agent-with-Claude.pdf) | The lecture slides as a PDF (18 slides). The editable deck, with speaker notes, is [online](https://claude.ai/artifact/VxdYTsrmJ1zVErnfKw6zXz) |
| [`docs/Lab-Build-a-CSV-Analyst-Four-Ways.pdf`](docs/Lab-Build-a-CSV-Analyst-Four-Ways.pdf) | The lab walkthrough slides as a PDF (17 slides), to show while students work. The editable deck, with speaker notes, is [online](https://claude.ai/artifact/Tr2TMrbsYPhPXWLZYJt1y9) |
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

Every student needs a Claude account that includes Claude Code: a paid plan (Pro, Max,
Team or Enterprise) or a Claude Console API key. Then either:

- **Their laptop:** Claude Code and Python 3.10+, set up as in the lab's
  [`LAB.md`](labs/06_claude_agents/LAB.md) (Option A).
- **A class VM on AWS:** for students who can't install Claude Code. You set up one Ubuntu
  VM with an account per student; they only need SSH. See
  [`labs/06_claude_agents/cloud/`](labs/06_claude_agents/cloud/README.md).

The take-home API exercise also needs an Anthropic API key.

## License

MIT. See [LICENSE](LICENSE).
