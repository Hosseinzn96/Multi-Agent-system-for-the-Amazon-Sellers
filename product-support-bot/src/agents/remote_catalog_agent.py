from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

def create_remote_catalog_agent() -> RemoteA2aAgent:
    """
    Remote proxy for the Product Catalog Agent, using its A2A agent card.
    """
    remote_product_catalog_agent = RemoteA2aAgent(
        name="product_catalog_agent",
        description="Remote product catalog agent from external vendor that provides product information.",
        agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
    )
    return remote_product_catalog_agent





'''import os
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

def create_remote_catalog_agent() -> RemoteA2aAgent:
    """
    Remote proxy for the Product Catalog Agent.
    Uses PRODUCT_CATALOG_BASE_URL if set; otherwise defaults to local dev.
    """
    base_url = os.getenv("PRODUCT_CATALOG_BASE_URL", "http://localhost:8001").rstrip("/")
    return RemoteA2aAgent(
        name="product_catalog_agent",
        description="Remote product catalog agent providing product information.",
        agent_card=f"{base_url}{AGENT_CARD_WELL_KNOWN_PATH}",
    )'''
