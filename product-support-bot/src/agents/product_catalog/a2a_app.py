from google.adk.a2a.utils.agent_to_a2a import to_a2a

from .agent import create_product_catalog_agent

def create_a2a_app(port: int = 8001):
    agent = create_product_catalog_agent()
    return to_a2a(agent, port=port)
