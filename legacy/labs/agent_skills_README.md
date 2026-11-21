# Agent Skills

A **skill** is a plain-text (Markdown) file that defines an agent's role, rules, and output format. Injecting it as a system prompt gives the LLM a focused persona without changing any Python code.

---

## What Is a Skill?

```mermaid
flowchart LR
    SK["skill.md\n─────────────\nRole\nRules\nTone\nOutput format"]
    -->|read at startup| SP["System Prompt"]
    SP -->|prepended to every call| LLM["LLM\ngpt-4o-mini"]
    LLM -->|structured response| OUT["Agent Output"]
```

---

## How It Fits Into the Agent Architecture

```mermaid
flowchart TD
    U([User Input]) --> CTR

    CTR{Controller}

    CTR -->|Read context| MEM["Memory\n─────────────\nConversation History\nVector Store"]
    MEM -->|Inject into prompt| CTR

    CTR -->|Load skill| SK["skill.md\n─────────────\nRole · Rules · Tone\nOutput format"]
    SK -->|System message| CTR

    CTR -->|Generate / reason| LLM["Model\n─────────────\ngpt-4o-mini\nChatOpenAI"]
    LLM -->|Tool call request| CTR
    LLM -->|Final answer| CTR

    CTR -->|Execute tool| TOOLS["Tools\n─────────────\nCalculator\nSearch\nload_csv\n…"]
    TOOLS -->|Observation| CTR

    CTR -->|Write result| MEM
    CTR -->|Return response| U
```

---

## Skill File Anatomy

```mermaid
mindmap
  root((skill.md))
    Role
      Who the agent is
      Domain expertise
    Rules
      What to always do
      What to never do
      Output sections
    Tone
      Style of writing
      Level of detail
    Example output
      Format reference
      Field names
```

---

## Loading a Skill at Runtime

```mermaid
sequenceDiagram
    participant F as skill.md
    participant A as Agent Setup
    participant S as SystemMessage
    participant L as LLM

    A->>F: Path("skill.md").read_text()
    F-->>A: skill_text (string)
    A->>S: SystemMessage(content=skill_text)
    S-->>A: system message object
    A->>L: create_react_agent(llm, tools, state_modifier=system_message)
    L-->>A: agent ready

    Note over A,L: Every subsequent invoke() prepends the skill as the system prompt
```

---

## Hot-Reload Pattern

Edit `skill.md` and re-run — no kernel restart required.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant F as skill.md
    participant A as Agent

    Dev->>F: Edit role / rules / tone
    Dev->>A: Re-run hot-reload cell
    A->>F: read_text()
    F-->>A: updated skill_text
    A->>A: Rebuild agent with new SystemMessage
    Note over A: Next invoke() uses updated instructions
```

---

## Skill vs. Tool vs. Memory

```mermaid
graph TD
    subgraph SK["Skill"]
        SK1["What: Markdown prompt file"]
        SK2["When: loaded at agent creation"]
        SK3["Effect: shapes behaviour & output format"]
        SK4["Swap: edit .md file, hot-reload"]
    end

    subgraph TL["Tool"]
        TL1["What: Python function"]
        TL2["When: called on demand by LLM"]
        TL3["Effect: retrieves or computes data"]
        TL4["Swap: change function / registration"]
    end

    subgraph MEM["Memory"]
        MEM1["What: message history / vector store"]
        MEM2["When: read & written each turn"]
        MEM3["Effect: retains context across turns"]
        MEM4["Swap: change checkpointer / store"]
    end
```

| | Skill | Tool | Memory |
|---|---|---|---|
| Format | Markdown file | Python function | Message list / vector DB |
| Controls | LLM behaviour & style | Data access & computation | Context across turns |
| Changed by | Editing `.md` | Editing Python | Conversation state |
| Required? | Optional | Optional | Optional |

---

## Decision Tree — When to Use a Skill

```mermaid
flowchart TD
    Start([New agent]) --> Q1{Does the agent need\na specific persona\nor output format?}
    Q1 -->|No| A1[No skill needed\nuse default LLM behaviour]
    Q1 -->|Yes| Q2{Will the persona\nchange at runtime?}
    Q2 -->|No| A2[Hard-code system prompt\nin agent definition]
    Q2 -->|Yes| A3[Use a skill.md file\nhot-reload on change]
    A3 --> Q3{Multiple personas\nor domains?}
    Q3 -->|No| B1[Single skill.md]
    Q3 -->|Yes| B2[One skill.md per persona\nload by name at startup]
```

---

## Component Overview

```mermaid
classDiagram
    class SkillLoader {
        +path: Path
        +read() str
    }

    class SystemMessage {
        +content: str
    }

    class ChatOpenAI {
        +model: gpt-4o-mini
        +temperature: 0
    }

    class ReactAgent {
        +invoke(inputs) dict
    }

    SkillLoader --> SystemMessage : produces
    SystemMessage --> ReactAgent : state_modifier
    ChatOpenAI --> ReactAgent : llm
```

---

## Setup

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Install dependencies

```bash
pip install python-dotenv langchain langchain-openai langgraph langchain-core
```

### Configure environment

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
```

---

## Minimal Example

```python
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

skill_text = Path("skill.md").read_text()

agent = create_react_agent(
    ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=[],
    state_modifier=SystemMessage(content=skill_text),
)

result = agent.invoke({"messages": [("user", "Review my code: def f(x): return x/0")]})
print(result["messages"][-1].content)
```

> See **`04_skill_agent.ipynb`** for the full runnable example including hot-reload.

---

## Skill File Template

```markdown
# Skill: <Name>

## Role
<One sentence describing who the agent is and what it does.>

## Rules
- <Always do X>
- <Never do Y>
- Output must contain these sections: …

## Tone
- <Style notes>

## Example output format
\`\`\`
### Section 1
…
### Verdict
…
\`\`\`
```
