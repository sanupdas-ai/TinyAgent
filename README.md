# TinyAgent

A compact, educational AI agent harness written in pure Python for experimenting with local large language models. The code uses Python's standard library to communicate with an OpenAI-compatible HTTP endpoint.

## Components

| File | Purpose |
| --- | --- |
| `agent.py` | Main agent, conversation flow, and an example run. |
| `llm.py` | HTTP client and structured response and step types. |
| `memory.py` | Conversation memory, trimming, and LLM-based summarization. |
| `trajectory.py` | Records queries and execution steps. |
| `utils.py` | Terminal viewer for responses, memory, and trajectories. |
| `prompting.py` | Few-shot prompting experiment. |
| `test.py` | Local model endpoint example. |

## Local model connection

The default endpoint is `http://localhost:11434/v1`. Run a compatible local inference server and make sure the model configured in the example is available. You can adjust the model name and endpoint through `LLM` in `llm.py`.

The endpoint example can be run with:

```bash
python3 test.py
```

Examples make live requests to the local model server. No model weights are included in this repository.

## Development status

This is an evolving learning project. Memory and trajectory components are implemented; planning and tool execution are currently placeholders in the agent.
