from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StartOutputParser

from app.graph.state import ConversationState, append_ai_message
from app.utils.llms import get_llm

def buils_esacation_chain() -> Runnable:
    """
    Escalation agent chain.
    handles compaints or unknown requests that require human interaction.
    """
    
    system = SystemMessage (
        content=(
            "You are an escalation assistant for a shiping company. "
            "Be empathetic, acknownledge the issue, and explain that the case "
            "will be escalated to human support. colect any useful details"
        )

    )
    llm = get_llm(purpose="agent")
    Chain = prompt | llm | StartOutputParser()
    return Chain

def escalation_node(state: ConversationState) -> ConversationState:
    """
    LangGraph node: escalation agent.
    Reads the conversation and sets state["escalation_message"] based on LLM output.
    
    """

    chain = build_escalation_chain()

    #Build a simple text representation of the conversation
    message = state.get("messages", [])
    conversation_text = ""
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        conversation_text += f"{role}: {m.content}\n"

    result = chain.invoke({"conversation": conversation_text}).strip()
    state["escalation_message"] = result
    return state

