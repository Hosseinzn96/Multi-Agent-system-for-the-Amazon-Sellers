from typing import Dict, Any

def save_last_product(tool_context, product_name: str) -> Dict[str, Any]:
    """
    Save the last product that the user asked about into ADK session state.
    Also shifts the previous last_product into second_last_product.
    """
    if product_name and isinstance(product_name, str):
        new_product = product_name.strip()

        # If we already had a last_product, move it to second_last_product
        prev_last = tool_context.state.get("user:last_product")
        if prev_last and prev_last != new_product:
            tool_context.state["user:second_last_product"] = prev_last

        tool_context.state["user:last_product"] = new_product

    return {
        "status": "saved",
        "last_product": tool_context.state.get("user:last_product"),
        "second_last_product": tool_context.state.get("user:second_last_product"),
    }


def get_last_product(tool_context) -> Dict[str, Any]:
    """
    Retrieve the last and second-last products from session state.

    Used for follow-up questions like:
      - "how much is the weight?"
      - "compare the last two products"
    """
    last_product = tool_context.state.get("user:last_product")
    second_last = tool_context.state.get("user:second_last_product")
    return {
        "last_product": last_product,
        "second_last_product": second_last,
    }


def save_preferred_brand(tool_context, brand_name: str) -> Dict[str, Any]:
    """
    Save the user's preferred brand in session state.

    Example triggers in conversation:
      - "I prefer Samsung products"
      - "My favorite brand is Sony"
    """
    if brand_name and isinstance(brand_name, str):
        tool_context.state["user:preferred_brand"] = brand_name.strip()

    return {
        "status": "saved",
        "preferred_brand": tool_context.state.get("user:preferred_brand"),
    }


def get_preferred_brand(tool_context) -> Dict[str, Any]:
    """
    Retrieve the user's preferred brand from session state.

    Used when the user asks things like:
      - "show me something from my preferred brand"
      - "recommend a TV from my favorite brand"
    """
    preferred_brand = tool_context.state.get("user:preferred_brand")
    return {
        "preferred_brand": preferred_brand,
    }
