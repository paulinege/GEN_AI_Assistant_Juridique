from __future__ import annotations

from src.memory_agent import build_memory_agent

_agent = None

def get_memory_agent():
    global _agent
    if _agent is None:
        _agent = build_memory_agent()
    return _agent

def ask_agent_with_memory(query: str, thread_id: str = "default-thread") -> str:
    agent = get_memory_agent()

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config={"configurable": {"thread_id": thread_id}},
    )

    messages = result.get("messages", [])
    if not messages:
        return str(result)

    last = messages[-1]
    content = getattr(last, "content", None)

    if isinstance(content, str):
        return content

    return str(last)