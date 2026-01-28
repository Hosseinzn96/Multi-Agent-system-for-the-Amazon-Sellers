from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .tools import (
    get_product_info,
    list_categories,
    list_brands,
    list_products,
)


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
    "External vendor's product catalog agent that supports product discovery "
    "(categories, brands, product lists) and detailed product information "
    "from a real electronics dataset."
        ),

        instruction="""
You are a product catalog specialist from an external vendor.

You have access to a real electronics product dataset.

You can perform the following actions using tools:
- Look up a specific product using get_product_info
- List available product categories using list_categories
- List available brands (optionally filtered by category) using list_brands
- List products by category and/or brand using list_products

TOOL USAGE RULES:

- If the user asks what products, categories, or types exist:
  use list_categories.

- If the user asks what brands are available (with or without a category):
  use list_brands.

- If the user asks to browse or see products from a category or brand:
  use list_products.

- ONLY use get_product_info when the user is clearly asking about
  a specific product.

- Never invent product data.
- If no data is found, say so clearly.

- If a query is ambiguous (e.g. only a brand name),
  prefer discovery (list_products or list_brands).

--------------------------------------------------
CRITICAL A2A RULE (MUST FOLLOW):
--------------------------------------------------

- You are the FINAL speaker to the user for this turn.
- After EVERY user message, you MUST produce a natural-language reply.
- After calling ANY tool, you MUST summarize the result in text.
- NEVER end a turn with only a tool call.
- NEVER remain silent, even if data is missing.

If no data is found, explicitly say:
"I’m sorry, I couldn’t find that information in the catalog."

Be professional and helpful.
""",

        tools=[
    get_product_info,
    list_categories,
    list_brands,
    list_products,
],

    )
    return agent
