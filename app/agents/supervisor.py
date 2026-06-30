from typing import Dict

from langchain_core.prompts import ChatPromtTemplet
from langchain_core.runnables import Runnable 
from langchain_core.output_parsers import StartOutputParser

from app.graph.state import ConversationState
from app.utils.llm import get_llm

def build_supervisor_chain() -> Runnable:
    """
    Supervisor chain that decides which agent should handle the message.
    It return one of: "tracking", "faq", "escalation".
    """

    prompt = ChatPromptTemplate.from_templet(
        """
You are a Supervisor for a package tracking assistant.

Decide which specialized agent should handle the user's latest message.

Agents
- "tracking": questions about where a package is, tracking status, delivery time.
- "faq": general shipping questions (delivery times, shipping options, etc.)
- "escalation": complaints, issues that require human intervention.

Conversation:
{conversation}

"""
    )

    llm = get_llm(purpose="supervisor")
    chain = prompt | llm | StartOutputParser()
    return chain

def supervisor_decide(state: ConversationState) -> ConversationState:
    """
    LangGraph node: supervisor.
    Reads the conversation and sets state["route] based on LLM output.
    
    """

    chain = build_supervisor_chain()

    #Build a simaple =text representation of the conversation 
    message = state.get("messages", [] )
    conversation_text = ""
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        conversation_text += f"{role}: {m.content}\n"

        route = chain.invoke({"conversation": conversation_text}).strip().lower()

        if route not in {"tracking", "faq", "escalation"}:
            route = "escaltion" #fallback

            state["route"] = route
            return state
        