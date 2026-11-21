# Lab 03 — CSV Analyzer Agent

A ReAct agent that loads a CSV file and returns a statistical summary using a `load_csv` tool backed by pandas, built with LangChain 1.x and LangGraph.

---

## Architecture

```mermaid
graph TD
    A[User Query] --> B[LangGraph ReAct Agent]
    B --> C{LLM\ngpt-4o-mini}
    C -->|Tool call| D[load_csv Tool]
    D -->|pd.read_csv| E[pandas DataFrame]
    E -->|shape + columns +\ndescribe| F[Statistical Summary]
    F -->|Observation| C
    C -->|Final answer| G[Agent Output]
```

---

## ReAct Loop

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as LLM (gpt-4o-mini)
    participant T as load_csv Tool
    participant P as pandas

    U->>A: "Load and analyze the CSV at sample.csv"
    A->>L: messages + tool definitions
    L-->>A: Thought + Tool call: load_csv("sample.csv")
    A->>T: load_csv("sample.csv")
    T->>P: pd.read_csv("sample.csv")
    P-->>T: DataFrame (15 rows × 5 cols)
    T-->>A: shape, columns, df.describe()
    A->>L: Observation: statistical summary
    L-->>A: Final Answer: narrative interpretation
    A-->>U: Summary with insights
```

---

## Tool Logic

```mermaid
flowchart TD
    I["path: str"] --> R["pd.read_csv(path)"]
    R --> S{Success?}
    S -->|Yes| B1["shape: rows × cols"]
    S -->|No| E["Return error string"]
    B1 --> B2["columns list"]
    B2 --> B3["df.describe() stats"]
    B3 --> O["Return formatted summary string"]
```

---

## Sample Dataset — `sample.csv`

15 employees across 5 departments.

```mermaid
pie title Employees by Department
    "Engineering" : 4
    "Marketing"   : 3
    "Sales"       : 3
    "Finance"     : 3
    "HR"          : 2
```

| Column | Type | Description |
|---|---|---|
| `name` | string | Employee name |
| `age` | int | Age in years |
| `salary` | int | Annual salary (USD) |
| `department` | string | Department name |
| `years_experience` | int | Years of experience |

---

## Component Overview

```mermaid
classDiagram
    class ChatOpenAI {
        +model: gpt-4o-mini
        +temperature: 0
    }

    class load_csv {
        <<@tool>>
        +path: str
        +read_csv(path) DataFrame
        +describe() str
        +__call__(path) str
    }

    class ReactAgent {
        +invoke(inputs) dict
    }

    class pandas {
        +read_csv(path) DataFrame
        +DataFrame.describe() DataFrame
        +DataFrame.shape tuple
        +DataFrame.columns Index
    }

    ReactAgent --> ChatOpenAI : uses
    ReactAgent --> load_csv : equipped with
    load_csv --> pandas : delegates to
```

---

## Setup

### Prerequisites

- Python 3.9+
- An OpenAI API key
- A CSV file accessible from the working directory

### Install dependencies

```bash
pip install python-dotenv langchain langchain-openai langgraph langchain-core pandas
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

    subgraph Tool["load_csv Tool"]
        T1["@tool decorator"] --> T2["load_csv()"]
        T2 --> T3["pandas\nread + describe"]
    end

    subgraph Agent["Agent Construction"]
        A1["ChatOpenAI\ngpt-4o-mini"] --> A3["create_react_agent"]
        A2["load_csv tool"] --> A3
    end

    subgraph Run["Execution"]
        R1["Input: file path\nin user message"] --> R2["agent.invoke()"]
        R2 --> R3["messages list"]
        R3 -->|last message| R4["Narrative answer"]
    end

    Env --> Agent
    Tool --> Agent
    Agent --> Run
```

1. **Load environment** — `load_dotenv(override=True)` reads `OPENAI_API_KEY` from `.env`.
2. **Define the tool** — `load_csv()` uses pandas to read a CSV, returning shape, column names, and `df.describe()` as a formatted string.
3. **Create the agent** — `create_react_agent(llm, tools)` builds the LangGraph state machine.
4. **Invoke** — Pass a natural-language request containing the file path; the agent decides to call the tool and interprets the output.

---

## What `df.describe()` Returns

`df.describe()` generates summary statistics for all numeric columns:

| Statistic | Meaning |
|---|---|
| `count` | Number of non-null values |
| `mean` | Average |
| `std` | Standard deviation |
| `min` / `max` | Range |
| `25%` / `50%` / `75%` | Quartiles |

The LLM then narrates these statistics in plain language.

---

## Progression Across Labs

```mermaid
graph LR
    L1["Lab 01\nMath Agent\nTool: calculator()\neval()"] --> L2["Lab 02\nSearch Agent\nTool: search()\ndict lookup"]
    L2 --> L3["Lab 03\nCSV Agent\nTool: load_csv()\npandas I/O"]
    L3 --> L4["Lab 04+\nMore complex\nagents & tools"]

    style L3 fill:#d0e8ff,stroke:#3399ff
```

Each lab adds a more realistic tool while keeping the same `create_react_agent` pattern.

---

## Dependencies

| Package | Purpose |
|---|---|
| `langchain-openai` | OpenAI LLM integration |
| `langgraph` | ReAct agent state machine |
| `langchain` | `@tool` decorator |
| `pandas` | CSV loading and statistical summary |
| `python-dotenv` | Load `.env` variables |
