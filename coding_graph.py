"""PHASE 2: a LangGraph coding agent that can use the safe file tools.

Graph:
    START -> assistant --(AI wants a tool)--> tools --> back to assistant
                       --(no tool needed)--> END
"""
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from config import llm
from file_tools import ALL_TOOLS


SYSTEM_PROMPT = SystemMessage(
    "You are a friendly voice coding assistant for school students. "
    "You can chat normally, and you can use tools to work with files "
    "in the workspace folder. "
    "When the student asks to create or edit a file, call the tool directly. "
    "Do not ask the student to confirm first, "
    "because the tool itself shows a preview and asks them. "
    "Before explaining or editing a file, read it with read_file. "
    "To change a file, call edit_file with the COMPLETE new file content. "
    "Never say a file was created or changed unless the tool result says so. "
    "Answer in simple English in a few short sentences. "
    "Do not use markdown or emojis and do not repeat whole files, "
    "because your answer is read aloud."
)

# Tell the AI which tools exist.
llm_with_tools = llm.bind_tools(ALL_TOOLS)


# Node 1: the AI thinks and either answers or asks for a tool.
def assistant(state: MessagesState):
    reply = llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])
    return {"messages": [reply]}


# Build the graph.
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
# Node 2: runs the tool the AI asked for.
# handle_tool_errors=True: if a tool fails, the error message goes back to the AI
# (the app does not crash).
builder.add_node("tools", ToolNode(ALL_TOOLS, handle_tool_errors=True))

builder.add_edge(START, "assistant")
# Tool needed? go to "tools". No tool needed? go to END.
builder.add_conditional_edges("assistant", tools_condition)
# After a tool runs, go back to the AI.
builder.add_edge("tools", "assistant")

graph = builder.compile(checkpointer=InMemorySaver())

CONFIG = {"configurable": {"thread_id": "student-coding"}, "recursion_limit": 12}


def ask_ai(user_text):
    """Send the user's sentence to the coding agent and return the final answer."""
    old_count = len(graph.get_state(CONFIG).values.get("messages", []))
    result = graph.invoke({"messages": [("user", user_text)]}, CONFIG)

    # Show which tools the AI used in this turn (nice for learning).
    for message in result["messages"][old_count:]:
        for call in getattr(message, "tool_calls", []):
            print(f"[Tool used] {call['name']}")

    return result["messages"][-1].content


# Typed test (no microphone needed):  python coding_graph.py
if __name__ == "__main__":
    print("Type a request, e.g. 'list my files' (or 'exit').")
    while True:
        request = input("\nYou: ").strip()
        if request.lower() in {"exit", "quit", "stop"}:
            break
        if request:
            print("AI:", ask_ai(request))
