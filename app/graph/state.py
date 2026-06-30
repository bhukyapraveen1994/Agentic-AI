from typing import List, Optional, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class ConversationState(TypedDict, total=False):
    """
    Shared state for the LangGraph workflow.

    This is the "state" that flows between nodes.
    LangGraph will pass this TypedDict between agents.  
    """

    messages: List[BaseMessage]
    """
    The list of messages in the conversation.
    """

    system_prompt: Optional[str]
    """
    The system prompt for the conversation, if any.
    """

    #All message in the conversation (user + assistant)
    message: List[BaseMessage]

    # Which route the supervisor chose: "tracking", "faq", "escalation"
    route: Optional[str]

    #Optional field filled by agents
    tracking_results: Optional[str]
    faq_answer: Optional[str]
    escalation_note: Optional[str]

    def append_user_message(state: ConversationState, text: str) -> ConversationState:
        """ Helper to add a new user message to the state. """
        messages = state.get("messages", [])
        messages.append(HumanMessage(content=text))
        state["messages"] = messages
        return state  


def append_ai_message(state: ConversationState, text: str) -> ConversationState:
    """ Helper to add a new AI message to the state. """
    messages = state.get("message", [])
    messages.append(AIMessage(content=text))
    state["message"] = messages
    return state    

