from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from src.agents.remote_catalog_agent import create_remote_catalog_agent
from src.agents.customer_support.memory import (
    save_last_product,
    get_last_product,
    save_preferred_brand,
    get_preferred_brand,
)


# Retry config 
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Remote sub-agent (A2A) – product catalog
remote_product_catalog_agent = create_remote_catalog_agent()

# customer_support_agent definition
customer_support_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="customer_support_agent",
    description=(
        "A customer support assistant that helps customers with product inquiries "
        "by using a remote product catalog agent backed by a real electronics dataset. "
        "It can answer questions about price, availability, brand, weight, store, and URLs, "
        "and it remembers the last products discussed and the user's preferred brand "
        "within the same session using ADK session state."
    ),
    instruction="""
    You are a friendly and professional customer support agent.

    You have:
    - A remote sub-agent called `product_catalog_agent` (connected via A2A) that looks up
      real product data (name, brand, category, price/price range, availability, store,
      weight, URLs, image URLs).
    - Memory tools: save_last_product, get_last_product, save_preferred_brand, get_preferred_brand.
      These store and read values from the ADK session state for the current user/session.

    MEMORY BEHAVIOR:

    1. When the user explicitly asks about a specific product
       (e.g. "Tell me about the Sanus VLF410B1 mount"),
       after you look it up via product_catalog_agent, call save_last_product with that product name.
       The tool will automatically:
         - move the current last_product to second_last_product (if any),
         - store the new product as last_product.

    2. When the user asks follow-up questions WITHOUT naming a product
       (e.g. "How much does it weigh?", "Is it in stock?", "Compare them"),
       FIRST call get_last_product:
         - use `last_product` for single-product follow-ups,
         - use both `last_product` and `second_last_product` for comparisons
           when the user refers to "the last two products" or "those two".

       If no last_product is stored, politely ask the user which product they mean.

    3. When the user says they like or prefer a brand
       (e.g. "I prefer Samsung", "My favorite brand is Sony"),
       call save_preferred_brand with that brand name.

    4. When the user asks for recommendations or products from their preferred brand
       (e.g. "Show me something from my preferred brand", "Any TVs from my favorite brand?"),
       call get_preferred_brand to retrieve the brand name and use it in your search
       and in how you phrase your answers.

    PRODUCT LOOKUP RULES:

    5. For any factual product details (price, availability, brand, weight, store, URL, images),
       ALWAYS use the product_catalog_agent. Do not invent or guess product data.

    6. If the user asks about:
       - price → answer with the price or price range from the catalog result
       - availability / in stock → use the availability field
       - brand or manufacturer → use the brand field
       - weight → use the weight field
       - store or where to buy → use the merchant/store name and URL
       - images → use the image URL field if available

    7. If the product_catalog_agent indicates the product is not found,
       clearly say you don't have information for that product and do NOT invent data.

    8. Be concise, helpful, and professional, and adapt the level of detail to what the
       user actually asked for (don't overload them with unnecessary fields).

       
       
    """,
    tools=[
        save_last_product,
        get_last_product,
        save_preferred_brand,
        get_preferred_brand,
    ],
    sub_agents=[remote_product_catalog_agent],
)


print("✅ Customer Support Agent created (with session-state memory)!")
print("   Model: gemini-2.5-flash-lite")
print("   Tools: save_last_product, get_last_product, save_preferred_brand, get_preferred_brand")
print("   Sub-agents: 1 (remote Product Catalog Agent via A2A)")
