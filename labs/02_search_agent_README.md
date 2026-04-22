# Lab 02 — Search Agent

A minimal ReAct agent that uses a `search` tool backed by a fake in-memory knowledge base, built with LangChain 1.x and LangGraph.

---

## Architecture

```mermaid
graph TD
    A[User Query] --> B[LangGraph ReAct Agent]
    B --> C{LLM\ngpt-4o-mini}
    C -->|Tool call| D[Search Tool]
    D -->|Lookup in results dict| E[Search Results]
    E -->|Observation| C
    C -->|Final answer| F[Agent Output]
```

---

## ReAct Loop

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as LLM (gpt-4o-mini)
    participant T as Search Tool

    U->>A: "Search for AI agents"
    A->>L: messages + tool definitions
    L-->>A: Thought + Tool call: search("AI agents")
    A->>T: lookup("ai agents")
    T-->>A: "Top results: 1) LangChain Docs, 2) AutoGPT, 3) Research Papers"
    A->>L: Observation: search results
    L-->>A: Final Answer: summary of results
    A-->>U: Formatted answer
```

---

## Search Tool Logic

```mermaid
flowchart TD
    Q["query: str"] --> L["query.lower()"]
    L --> M{keyword match\nin results dict?}
    M -->|Yes| R["Return mapped results"]
    M -->|No| G["Return generic fallback:\n'Results for query: A, B, C'"]
```

---

## Component Overview

```mermaid
classDiagram
    class ChatOpenAI {
        +model: gpt-4o-mini
        +temperature: 0
    }

    class search {
        <<@tool>>
        +query: str
        +results: dict
        +__call__(query) str
    }

    class ReactAgent {
        +invoke(inputs) dict
    }

    ReactAgent --> ChatOpenAI : uses
    ReactAgent --> search : equipped with
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

## How It Works

```mermaid
flowchart LR
    subgraph Env["Environment Setup"]
        E1[".env file"] -->|load_dotenv| E2["OPENAI_API_KEY"]
    end

    subgraph Tool["Search Tool"]
        T1["@tool decorator"] --> T2["search()"]
        T2 --> T3["keyword lookup dict"]
    end

    subgraph Agent["Agent Construction"]
        A1["ChatOpenAI\ngpt-4o-mini"] --> A3["create_react_agent"]
        A2["search tool"] --> A3
    end

    subgraph Run["Execution"]
        R1["Input messages"] --> R2["agent.invoke()"]
        R2 --> R3["messages list"]
        R3 -->|last message| R4["Final answer"]
    end

    Env --> Agent
    Tool --> Agent
    Agent --> Run
```

1. **Load environment** — `load_dotenv(override=True)` reads `OPENAI_API_KEY` from `.env`.
2. **Define the tool** — The `@tool` decorator turns `search()` into a LangChain tool. It checks a hardcoded dict for known keywords (`ai agents`, `python`, `machine learning`) and falls back to a generic response.
3. **Create the agent** — `create_react_agent(llm, tools)` wires the LLM and tools into a LangGraph state machine.
4. **Invoke** — Pass `{"messages": [{"role": "user", "content": "..."}]}` and read `result["messages"][-1].content`.

---

## Built-in Knowledge Base

| Keyword | Results returned |
|---|---|
| `ai agents` | LangChain Documentation, AutoGPT Project, AI Agent Research Papers |
| `python` | Python.org, Python Tutorial, Python Package Index |
| `machine learning` | Scikit-learn, TensorFlow, PyTorch |
| *(anything else)* | Generic fallback: Example Result A, B, C |

---

## Key Difference from Lab 01

```mermaid
graph LR
    subgraph Lab01["Lab 01 — Math Agent"]
        C1["Tool defined with Tool()"] --> C2["Wraps plain function"]
    end
    subgraph Lab02["Lab 02 — Search Agent"]
        D1["Tool defined with @tool"] --> D2["Decorator auto-generates schema"]
    end
```

Lab 02 uses the `@tool` decorator instead of `Tool(...)`, which automatically infers the tool's name, description, and input schema from the function signature and docstring.

---

## Dependencies

| Package | Purpose |
|---|---|
| `langchain-openai` | OpenAI LLM integration |
| `langgraph` | ReAct agent state machine |
| `langchain-core` | `@tool` decorator |
| `python-dotenv` | Load `.env` variables |
