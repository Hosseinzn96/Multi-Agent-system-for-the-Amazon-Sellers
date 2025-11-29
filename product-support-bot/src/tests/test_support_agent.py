from dotenv import load_dotenv
import os
load_dotenv()

import asyncio

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from src.agents.customer_support.agent import customer_support_agent

# Shared session service for tests
session_service = InMemorySessionService()
app_name = "support_app"
user_id = "demo_user"


async def test_a2a_communication(user_query: str, session_id: str = "test_session_1"):
    """
    Test the A2A communication between Customer Support Agent and Product Catalog Agent,
    using a persistent session so ADK session_state is preserved.
    """

    # Ensure the session exists; if it already exists just reuse it
    try:
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
    except Exception:
        # Session already exists – fine
        pass

    runner = Runner(
        agent=customer_support_agent,
        app_name=app_name,
        session_service=session_service,
    )

    test_content = types.Content(parts=[types.Part(text=user_query)])

    print(f"\n👤 Customer: {user_query}")
    print("\n🎧 Support Agent response:")
    print("-" * 60)

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=test_content,
    ):
        if not event.is_final_response():
            continue

        content = getattr(event, "content", None)
        if not content:
            continue

        parts = getattr(content, "parts", None)
        if not parts:
            continue

        for part in parts:
            text = getattr(part, "text", None)
            if text:
                print(text)

    print("-" * 60)


async def main():
    # First turn: ask about a specific product
    await test_a2a_communication(
        "Tell me about the Boytone - 2500W 2.1-Ch. Home Theater System.",
        session_id="test_session_2",
    )

    # Second turn: follow-up question using memory (last_product)
    await test_a2a_communication(
        "How much does it weigh?",
        session_id="test_session_2",
    )


if __name__ == "__main__":
    asyncio.run(main())





