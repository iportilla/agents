
# Streamlit Agentic AI Exercise — Solution Key

## 1. Correct File Structure
```
streamlit_agent_app/
├── app.py
├── tools.py
└── requirements.txt
```

## 2. Correct requirements.txt
```
streamlit
langchain
langchain-openai
pandas
python-dotenv
```

## 3. Correct tools.py
```python
from langchain.tools import tool
import pandas as pd

@tool
def fake_search(query: str) -> str:
    """Return fake search results."""
    return f"Search results for '{query}': A, B, and C."

@tool
def summarize_csv(path: str) -> str:
    """Load and summarize a CSV file."""
    df = pd.read_csv(path)
    return df.describe().to_string()
```

## 4. Correct app.py
```python
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from tools import fake_search, summarize_csv
import os

st.set_page_config(page_title="Agentic AI Demo", page_icon="🤖")

st.title("🤖 Agentic AI Demo")
st.write("This is a simple LangChain agent with tools + Streamlit UI.")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini")

tools = [fake_search, summarize_csv]

prompt = """You are an AI agent that can call tools.
Use tools only when needed.
Return clear explanations."""

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

user_input = st.text_input("Ask the agent a question:",
                           placeholder="e.g., Search for data science trends")

if st.button("Run Agent"):
    if user_input.strip():
        with st.spinner("Agent thinking..."):
            result = executor.invoke({"input": user_input})
        st.success("Agent Response:")
        st.write(result["output"])
```

## 5. Expected Outputs
- Fake search returns: `"A, B, and C"`.
- CSV summary returns `.describe()` output.
- Text questions produce direct LLM answers.

## 6. Common Errors + Fixes
| Error | Fix |
|------|------|
| Missing langchain-openai | pip install langchain-openai |
| API key missing | export OPENAI_API_KEY=your_key |
| Tool not registered | Add tool to tools list |
| Wrong CSV path | Use absolute path |

## 7. Bonus Solutions
### A. File Upload
```python
uploaded = st.file_uploader("Upload a CSV")
```

### B. New Joke Tool
```python
@tool
def joke(topic: str): ...
```

### C. Add Memory
```python
ConversationBufferMemory()
```



P@ssw0rd2025
