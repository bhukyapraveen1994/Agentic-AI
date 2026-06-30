from langgraph.graph import StateGraph, END

from app.graph.state import ConversationState
from app.agents.supervisor import supervisor_node
from app.agents.tracking import tracking_node
from app.agents.faq import faq_node
from app.agents.escalation import escalation_node

def build_graph() -> StateGraph:

    """
    Build the langgraph for the multi-agent workflow.
    
    Nodes:
    - supervisor
    - tracking_agent
    - faq_agent
    - escalation_agent

    Edges :
    - entry -> supervisor
    - supervisor -> tracking_agent / faq_agent / escalation_agent (conditional)
    - each agent -> END
    """


    ## Create a geaph that uses ConversationState as its state type
    graph = StateGraph(ConversationState)

    # Add nodes (each node is a callable that takes and returns state)

    graph. add_node("supervisor", supervisor_node)
    graph.add_node("tracking_agent", tracking_node)
    graph.add_node("faq_agent", faq_node)
    graph.add_node("escalation_agent", escalation_node)

    # Conditional edge from supervisor based on state["route"]
    def supervisor_edge(state: ConversationState) -> str:

        """
        This funcationality is used by LangGraph to choose the next node.
        It reads state["route"] and returns the node name.
        
        """

        route = state.get("route", "escalation")
        if route == "tracking":
            return "tracking_agent"
        if route == "faq":
            return "faq_agent"
        

        graph.add_conditional_edges(
            "supervisor",
            route_decidor,
            {
                "tracking": "tracking_agent",
                "faq": "faq_agent",
                "escalation": "escalation_agent",   
            }

        )

        ## Each agent ends the workflow for this turn
        graph.add_edge("tracking_agent", END)
        graph.add_edge("faq_agent", END)
        graph.add_edge("escalation_agent", END)

        return graph
    