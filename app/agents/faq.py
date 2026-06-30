from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser

from app.graph.state import ConversationState, append_ai_message
from app.utils.llm import get_llm

def build_faq_chain() -> Runnable:
    """
    FAQ agent chain.
    
    Uses a system prompt to answer general shipping questions.
    """

    system = SystemMessage(
        content=(
            "You are a shipping FAQ assistant. "
            "You can answer questions about shipping times, options, and policies. "
            "If the user asks something you don't know, respond politely that you don't have that information."       
        )
    )

    prompt = ChatPromptTemplate.from_template(

        [
            
            ("system", system.content),
            ("human", "{user_input}"),,
                       
        ]
    )
    llm = get_llm(purpose="agent")
    chain =  prompt | llm | StrOutputParser()
    return chain

def faq_node(state: ConversationState) -> ConversationState:
    """
    LangGraph node: faq agent.
    Reads the conversation and sets state["faq_answer] based on LLM output.
    
    """

    chain = build_faq_chain()

    #Build a simple text representation of the conversation
    message = state.get("messages", [])
    conversation_text = ""
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        conversation_text += f"{role}: {m.content}\n"

    result = chain.invoke({"user_input": conversation_text}).strip()
    state["faq_answer"] = result
    return state

