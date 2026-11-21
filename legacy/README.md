# Legacy material

Earlier versions of this course, kept for reference. Nothing here is used by the current
lecture or lab, and nothing outside this folder depends on it.

| Path | What it is |
|---|---|
| [`REACT_ACTIVITY_README.md`](REACT_ACTIVITY_README.md) | The no-code "Fun ReAct Lab" classroom activity |
| [`docs/`](docs/) | The original lecture PDF, *Intro to Agentic AI* |
| [`labs/01`–`04`](labs/) | LangChain + OpenAI notebooks: math, search, CSV and skill agents |
| [`labs/Lab-5/`](labs/Lab-5/) | A reasoning agent on the OpenAI API with a Streamlit UI |
| [`labs/calculator/`](labs/calculator/) | The calculator as a cloud MCP server (Docker + SSE) |
| [`ui-demo/`](ui-demo/) | A Streamlit front end for a LangChain agent, with an exercise solution key |

These use OpenAI models and older LangChain APIs, and are not maintained. Known issues:

- `ui-demo/solution_key.md` uses the old `AgentExecutor` API, while `ui-demo/app.py` uses LangGraph.
- The calculator's `eval` with `__builtins__` turned off is not a sandbox: an expression such
  as `().__class__.__base__.__subclasses__()` reaches Python internals. Don't expose it publicly.
