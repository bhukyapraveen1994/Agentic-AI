from pydantic import BaseModel
from fastapi import APIRouter

from app.graph.state import append_user_message
from app.graph.workflow import build_graph
from app.service.session_manager import session manager

#Build the LangGraph app once
_graph = build_graph()

class ChatRequest(BaseModel):

    session_id: str
    user_message: str

    class ChatResponse(BaseModel):
        session_id: str
        reply: str
        route: str
        router = APIRouter()


        @router.post("/chat", response_model=ChatResponse)
        async def chat_endpoint(payload: ChatRequest) -> ChatRequest:
            """
            POST /chat
            
            Body:
            {
                "session_id": "abc123",
                "user_message": "Where is my package?"
            }

            Returns the assistant reply and the route chosen by the suoervisor.
            """

            #Load existing state for this session
            state =  session_manager.get_state(payload.session_id)

            #Append the new user message
            state =session_manager.get_state(state, payload.user_message)

            #Run the graph for this turn
            result_state = _graph.run(state)

            #Persist the updated stste
            session_manager.set_state(payload.session_id,result_state)

            #The last assistant message is our reply
            message = result_state.get("messages",[])
            reply_text = ""
            for m in reversed(messages):
                if m.type == "ai":
                    reply_text = m.content
                    break

    route = result_state.get("route", "unknown")
    return ChatResponse(
        session_id=payload.session_id,
        reply=reply_text,
        route=route
    )