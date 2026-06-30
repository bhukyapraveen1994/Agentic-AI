from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import system_message
from lamgchain_core.output_parsers import StrOutputParser

from app.graph.state import ConversationState, append_ai_messagefrom app.tools.tracking_api import mock_tracking_lookup
from app.tools.tracking_api import mock_tracking_lookup
from app.utils.llm import get_llm

def build_tracking_chain() -> Runnable:
    """
    tracking agent chain.
    
    Uses a system prompt + tool to answer "where is my package" questions.
    """

    system = SystemMessage(
        content=(
            
            "You are a package tracking assistant. "
            "You have access to a tool that can look up package status by tracking number. "
            "If the user asks about a package, use the tool to get the status and respond with it. "
            "If the user asks something else, respond politely that you can only help with package tracking."       
        )
    )

    llm = get_llm(purpose="agent").bind_tools([mock_tracking_lookup])
    chain =  prompt | llm | StrOutputParser()
    return chain

def tracking_node(state: ConversationState) -> ConversationState:
    """
    LangGraph node: tracking agent.
    Reads the conversation and sets state["tracking_results] based on LLM output.
    
    """

    chain = build_tracking_chain()

    #Build a simple text representation of the conversation
    message = state.get("messages", [])
    conversation_text = ""
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        conversation_text += f"{role}: {m.content}\n"

    result = chain.invoke({"conversation": conversation_text}).strip()
    state["tracking_results"] = result
    return state