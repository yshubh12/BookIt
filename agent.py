from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, ToolMessage

from pydantic import BaseModel, Field
from typing import List, Optional
from langgraph.graph import StateGraph, END

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from calendar_utils import get_available_slots, book_slot
from utils import parse_time_from_text, find_closest_slot

import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

class AgentState(BaseModel):
    messages: List
    parsed_time: Optional[str] = None


# Step 1: Intent Router
def route_intent(state):
    message = state.messages[-1].content  # ✅ Extract message text
    print("Routing based on message:", message)

    if "book" in message.lower() or "schedule" in message.lower():
        return "check_time"
    return "ask_user_slot"



# Step 2: Check for datetime
def check_for_time(state):
    message = state["messages"][-1].content
    parsed_time = parse_time_from_text(message)
    state["parsed_time"] = parsed_time
    if parsed_time:
        return "check_slot"
    return "ask_user_slot"

# Step 3: Find and Book Closest Slot
def check_slot(state):
    slots = get_available_slots()
    parsed_time = state["parsed_time"]
    chosen = find_closest_slot(parsed_time, slots)
    if chosen:
        book_slot(chosen["iso"])
        state["messages"].append(HumanMessage(content=f"✅ Your appointment is booked for {chosen['readable']}"))
    else:
        state["messages"].append(HumanMessage(content="🕒 No close slot found, please pick one manually."))
    return END

# Step 4: Ask user to select manually
def ask_user_slot(state):
    slots = get_available_slots()
    if slots:
        state["messages"].append(HumanMessage(content="🕒 Sure! Please select one of the available time slots to confirm."))
    else:
        state["messages"].append(HumanMessage(content="❌ No slots available."))
    return END

# Define Graph
graph = StateGraph(AgentState)

graph.add_node("check_time", RunnableLambda(check_for_time))
graph.add_node("check_slot", RunnableLambda(check_slot))
graph.add_node("ask_user_slot", RunnableLambda(ask_user_slot))

graph.add_node("router", RunnableLambda(route_intent))
graph.set_entry_point("router")

graph.add_edge("check_time", "check_slot")
graph.add_edge("check_time", "ask_user_slot")
graph.add_edge("check_slot", END)
graph.add_edge("ask_user_slot", END)

tailor_talk_graph = graph.compile()

def handle_user_input(user_input):
    messages = [HumanMessage(content=user_input)]
    state = {"messages": messages}
    result = tailor_talk_graph.invoke(state)
    return result["messages"][-1].content

