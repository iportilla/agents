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

prompt = """You are an AI agent that can call tools when needed.
If a tool is useful, use it.
If not, answer directly.
Provide clear, step-by-step reasoning."""

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

user_input = st.text_input(
    "Ask the agent a question:",
    placeholder="Try: 'search for machine learning news'"
)

if st.button("Run Agent"):
    if user_input.strip():
        with st.spinner("Agent thinking..."):
            result = executor.invoke({"input": user_input})
        st.success("Agent Response:")
        st.write(result["output"])
