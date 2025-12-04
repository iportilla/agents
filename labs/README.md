# Agentic AI Examples

This package includes simple introductory LangChain agent examples for teaching a 60-minute session on agentic AI. Each notebook demonstrates the ReAct (Reasoning + Acting) pattern with different tools.

## Included Notebooks

### 1. `01_math_agent.ipynb`
A minimal agent that uses a calculator tool to perform mathematical calculations. Demonstrates:
- Creating custom tools with the `Tool` class
- Using Python's `eval()` for mathematical expressions
- Basic ReAct agent setup with verbose output

### 2. `02_search_agent.ipynb`
A simple agent using a custom fake search tool. Demonstrates:
- Creating custom tool functions
- Simulating external API calls (search engine)
- Pattern matching for different query types

### 3. `03_csv_agent.ipynb`
An agent that loads and analyzes CSV files. Demonstrates:
- Using the `@tool` decorator for tool creation
- File I/O operations within tools
- Error handling in tool functions
- Returning structured data summaries

## Requirements

```bash
pip install langchain langchain-openai langchainhub pandas
```

## Setup

1. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. For the CSV agent notebook, create a sample CSV file named `sample.csv` or modify the path in the notebook.

## Usage

1. Open each notebook in Jupyter:
   ```bash
   jupyter notebook
   ```

2. Run cells sequentially to see the agent in action

3. The `verbose=True` setting will show you the agent's reasoning process, including:
   - The agent's thoughts
   - Which tools it decides to use
   - Tool outputs
   - Final answers
