# src/memory_session_service.py

from google.adk.sessions import InMemorySessionStore, SessionService


class InMemorySessionService(SessionService):
    """
    Simple wrapper so we can easily share a single session service
    between tests, Gradio app, etc.
    """

    def __init__(self):
        super().__init__(session_store=InMemorySessionStore())
