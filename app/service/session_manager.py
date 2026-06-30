from typing import Dict
from app.graph.state import ConversationState

class SessionManager:

    """
    Very simple in-memory session store.
    In a real app you'd use a database or cache like Redis to store session state.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, ConversationState] = {}

    def get_state(self, session_id: str) -> ConversationState:
        if session_id not in self._sessions:

            # Initialize new session state if it doesn't exist
            self._sessions[session_id] = {"message": [], "session_id": session_id: session_id}
               return self._sessions[session_id]
        
        def set_state(self, session_id: str, state: ConversationState) -> None:
            self._sessions[session_id] = state

session_manager = SessionManager()


