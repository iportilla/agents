"""
Tools Module for LangChain Agent

This module defines custom tools that can be used by the LangChain agent.
Each tool is decorated with @tool to make it compatible with LangChain's agent framework.

Tools available:
- fake_search: Simulates a search engine query
- summarize_csv: Loads and provides statistical summary of CSV files
"""

from langchain.tools import tool
import pandas as pd


@tool
def fake_search(query: str) -> str:
    """
    Simulate a search engine query and return mock results.
    
    This is a demonstration tool that simulates searching for information.
    In a real application, this would connect to an actual search API
    (e.g., Google Custom Search, Bing Search API, or DuckDuckGo).
    
    Args:
        query (str): The search query string to look up
        
    Returns:
        str: A formatted string containing mock search results
        
    Example:
        >>> fake_search("machine learning")
        "Search results for 'machine learning': A, B, and C."
    """
    return f"Search results for '{query}': A, B, and C."


@tool
def summarize_csv(path: str) -> str:
    """
    Load a CSV file and return statistical summary of its contents.
    
    This tool reads a CSV file using pandas and generates descriptive statistics
    for all numeric columns, including count, mean, std, min, quartiles, and max.
    
    Args:
        path (str): File path to the CSV file to analyze
        
    Returns:
        str: A string representation of the DataFrame's statistical summary
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist at the specified path
        pd.errors.EmptyDataError: If the CSV file is empty
        
    Example:
        >>> summarize_csv("data/sales.csv")
        "       column1    column2
        count    100.0      100.0
        mean      50.5       75.2
        ..."
    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(path)
    
    # Generate descriptive statistics and convert to string format
    return df.describe().to_string()
