# Lab 01 — Math Agent

A minimal ReAct agent that uses a `Calculator` tool to evaluate mathematical expressions, built with LangChain 1.x and LangGraph.

---

## Architecture

```mermaid
graph TD
    A[User Query] --> B[LangGraph ReAct Agent]
    B --> C{LLM\ngpt-4o-mini}
    C -->|Tool call| D[Calculator Tool]
    D -->|eval expression| E[Result]
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
    participant T as Calculator Tool

    U->>A: "What is 25 * 17?"
    A->>L: messages + tool definitions
    L-->>A: Thought + Tool call: Calculator("25 * 17")
    A->>T: eval("25 * 17")
    T-->>A: "425"
    A->>L: Observation: "425"
    L-->>A: Final Answer: "The result is 425"
    A-->>U: "The result is 425"
```

---

## Component Overview

```mermaid
classDiagram
    class ChatOpenAI {
        +model: gpt-4o-mini
        +temperature: 0
    }

    class Tool {
        +name: Calculator
        +func: calculator()
        +description: string
    }

    class calculator {
        +expression: str
        +eval(expression) str
    }

    class ReactAgent {
        +invoke(inputs) dict
    }

    ReactAgent --> ChatOpenAI : uses
    ReactAgent --> Tool : equipped with
    Tool --> calculator : wraps
```

---

## Setup

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Install dependencies

```bash
pip install python-dotenv langchain langchain-openai langgraph langchain-core \
  "protobuf>=5.28.0,<7.0.0" "dataclasses-json>=0.6.7,<0.7.0"
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

    subgraph Agent["Agent Construction"]
        A1["ChatOpenAI\ngpt-4o-mini"] --> A3["create_react_agent"]
        A2["Calculator Tool"] --> A3
    end

    subgraph Run["Execution"]
        R1["Input messages"] --> R2["agent.invoke()"]
        R2 --> R3["messages list"]
        R3 -->|last message| R4["Final answer"]
    end

    Env --> Agent
    Agent --> Run
```

1. **Load environment** — `load_dotenv(override=True)` reads `OPENAI_API_KEY` from `.env`.
2. **Define the tool** — `calculator()` wraps Python's `eval` with restricted builtins for basic safety.
3. **Create the agent** — `create_react_agent(llm, tools)` wires the LLM and tools into a LangGraph state machine.
4. **Invoke** — Pass `{"messages": [("user", "...")]}` and read `result["messages"][-1].content`.

---

## Security Note

The `calculator` function restricts `eval` by passing `{"__builtins__": None}` as the globals dict, preventing access to built-in Python functions. Only mathematical operators are evaluated.

---

## Dependencies

| Package | Purpose |
|---|---|
| `langchain-openai` | OpenAI LLM integration |
| `langgraph` | ReAct agent state machine |
| `langchain-core` | `Tool` abstraction |
| `python-dotenv` | Load `.env` variables |
