from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .tools import get_product_info

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def create_product_catalog_agent() -> LlmAgent:
    agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="product_catalog_agent",
        description=(
            "External vendor's product catalog agent that provides detailed product "
            "information (price range, availability, store, brand, weight, URLs, images) "
            "from a real electronics dataset."
        ),
        instruction="""
    You are a product catalog specialist from an external vendor.

    When the user asks about a product, ALWAYS use the get_product_info tool
    to look it up in the catalog.

    - If the user only asks about price, you may answer with just the price info.
    - If they ask about weight, brand, availability, store, or URL, use the tool
      output to answer those specifically.
    - If they ask for a general description, summarize all the key fields returned
      by the tool (name, brand, category, price range, availability, store,
      weight, URL, image URL if present).

    If the tool says the product is not found, clearly say you don't have
    information for that product and do NOT invent data.
    Be professional and helpful.
    """,
        tools=[get_product_info],
    )
    return agent
