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
