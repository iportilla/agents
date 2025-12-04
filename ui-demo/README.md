# Agentic AI Demo - Streamlit Application

A simple demonstration of a LangChain ReAct agent integrated with Streamlit, showcasing how AI agents can use tools to extend their capabilities.

## 📋 Overview

This application demonstrates:
- **LangChain Agent Framework**: Uses LangGraph's `create_react_agent` to build a ReAct (Reasoning + Acting) agent
- **Custom Tools**: Two example tools that the agent can use:
  - `fake_search`: Simulates web search functionality
  - `summarize_csv`: Analyzes and summarizes CSV files
- **Streamlit UI**: Clean web interface for interacting with the agent
- **OpenAI Integration**: Powered by GPT-4o-mini for cost-effective performance

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Web Interface         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      LangGraph ReAct Agent              │
│  (Reasoning + Tool Selection)           │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ fake_search  │    │summarize_csv │
│    Tool      │    │    Tool      │
└──────────────┘    └──────────────┘
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd streamlit_agent_app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-actual-api-key-here"
   ```
   
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
streamlit_agent_app/
├── app.py              # Main Streamlit application
├── tools.py            # Custom tool definitions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Components Explained

### app.py
The main application file that:
- Configures the Streamlit interface
- Initializes the OpenAI language model
- Creates the ReAct agent with custom tools
- Handles user input and displays agent responses

### tools.py
Defines custom tools for the agent:
- **fake_search**: Demonstrates how to create a search tool (returns mock results)
- **summarize_csv**: Loads a CSV file and returns statistical summary using pandas

## 💡 Usage Examples

Try asking the agent questions like:

1. **Using the search tool:**
   - "Search for the latest AI news"
   - "Find information about machine learning"

2. **Using the CSV summarizer:**
   - "Summarize the CSV file at data/sales.csv"
   - "Analyze the data in report.csv"

3. **General questions:**
   - "What tools do you have available?"
   - "Explain what a ReAct agent is"

## 🛠️ Customization

### Adding New Tools

To add a new tool, edit `tools.py`:

```python
from langchain.tools import tool

@tool
def your_custom_tool(parameter: str) -> str:
    """
    Description of what your tool does.
    
    Args:
        parameter: Description of the parameter
        
    Returns:
        Description of the return value
    """
    # Your tool logic here
    return "result"
```

Then add it to the tools list in `app.py`:
```python
from tools import fake_search, summarize_csv, your_custom_tool

tools = [fake_search, summarize_csv, your_custom_tool]
```

### Changing the Language Model

Edit the model in `app.py`:
```python
llm = ChatOpenAI(model="gpt-4")  # or "gpt-3.5-turbo", etc.
```

## 📚 Dependencies

- **streamlit**: Web application framework
- **langchain**: LLM application framework
- **langchain-openai**: OpenAI integration for LangChain
- **langchain-core**: Core LangChain functionality
- **langgraph**: Agent workflow library
- **pandas**: Data analysis (for CSV tool)
- **python-dotenv**: Environment variable management

## 🔒 Security Notes

- **Never commit your API key** to version control
- Always use environment variables for sensitive data
- The placeholder API key in the code will not work - you must provide your own

## 📖 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## 🤝 Contributing

This is a demonstration project for educational purposes. Feel free to:
- Add new tools
- Improve the UI
- Enhance error handling
- Add more features

## 📝 License

This project is for educational purposes.
