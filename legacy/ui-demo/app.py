"""
Agentic AI Demo - Streamlit Application

This application demonstrates a simple LangChain ReAct agent with custom tools,
integrated into a Streamlit web interface. The agent can use tools to search for
information and analyze CSV files.

Key Components:
- LangChain: Framework for building LLM-powered applications
- LangGraph: Library for creating agent workflows
- OpenAI GPT-4o-mini: The language model powering the agent
- Streamlit: Web framework for the user interface
- Custom Tools: fake_search and summarize_csv

Usage:
    Run with: streamlit run app.py
    Set OPENAI_API_KEY environment variable before running
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import fake_search, summarize_csv
import os

# Configure the Streamlit page with title and icon
st.set_page_config(page_title="Agentic AI Demo", page_icon="🤖")

# Display the main title and description
st.title("🤖 Agentic AI Demo")
st.write("This is a simple LangChain agent with tools + Streamlit UI.")

# ============================================================================
# API Key Configuration
# ============================================================================
# Attempt to retrieve the OpenAI API key from environment variables
# If not found, use a placeholder (you should set the actual key in your environment)
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    # Warning: Replace this placeholder with your actual API key via environment variable
    api_key = "sk-placeholder_for_your_api_key"
    st.warning("⚠️ Using placeholder API key. Set OPENAI_API_KEY environment variable.")

# Set the API key in the environment for the OpenAI client
os.environ['OPENAI_API_KEY'] = api_key

# ============================================================================
# Agent Setup
# ============================================================================
# Initialize the language model (GPT-4o-mini is cost-effective and fast)
llm = ChatOpenAI(model="gpt-4o-mini")

# Define the list of tools available to the agent
# These tools extend the agent's capabilities beyond just text generation
tools = [fake_search, summarize_csv]

# Create a ReAct (Reasoning + Acting) agent
# This agent can reason about which tools to use and execute them
agent = create_react_agent(llm, tools)

# ============================================================================
# User Interface
# ============================================================================
# Create a text input field for user queries
user_input = st.text_input(
    "Ask the agent a question:", 
    placeholder="e.g., Search for machine learning news"
)

# Create a button to trigger the agent
if st.button("Run Agent"):
    # Only process if the user has entered something
    if user_input.strip():
        # Display a spinner while the agent is processing
        with st.spinner("Agent thinking..."):
            # Invoke the agent with the user's message
            # The agent will decide which tools (if any) to use
            result = agent.invoke({"messages": [("user", user_input)]})
        
        # Display the agent's response
        st.success("Agent Response:")
        # Extract the final message from the agent's response
        st.write(result["messages"][-1].content)
    else:
        st.error("Please enter a question before running the agent.")

# ============================================================================
# Setup Instructions
# ============================================================================
# To set your OpenAI API key, run this command in your terminal:
# export OPENAI_API_KEY="your-actual-api-key-here"

