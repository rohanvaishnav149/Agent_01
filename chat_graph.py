"""PHASE 1: a simple LangGraph chatbot with memory.

Graph:   START -> chatbot -> END
"""
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver

from config import llm


SYSTEM_PROMPT = SystemMessage(
    "You are a friendly voice assistant for school students. "
    "Answer in simple English in 2 to 4 short sentences. "
    "Do not use markdown, tables or emojis, because your answer is read aloud."
)


# Node: one step of the graph. It gets the chat so far and returns the AI reply.
def chatbot(state: MessagesState):
    reply = llm.invoke([SYSTEM_PROMPT] + state["messages"])
    return {"messages": [reply]}


# Build the graph.
builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# InMemorySaver remembers the conversation while the program is running.
graph = builder.compile(checkpointer=InMemorySaver())

# The thread_id is the "conversation name". Same id = same memory.
CONFIG = {"configurable": {"thread_id": "student-chat"}}


def ask_ai(user_text):
    """Send the user's sentence to the graph and return the AI answer as text."""
    result = graph.invoke({"messages": [("user", user_text)]}, CONFIG)
    return result["messages"][-1].content


# Typed test:  python chat_graph.py
if __name__ == "__main__":
    print("Type your question (or 'exit').")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit", "stop"}:
            break
        if question:
            print("AI:", ask_ai(question))
