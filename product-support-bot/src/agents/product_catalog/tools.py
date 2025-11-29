import pandas as pd

from .loader import (
    products_df,
    name_col,
    price_min_col,
    price_max_col,
    availability_col,
    store_col,
    category_col,
    url_col,
    weight_col,
    brand_col,
    image_url_col,
)


def get_product_info(product_name: str) -> str:
    if not isinstance(product_name, str) or not product_name.strip():
        return "Please provide a valid product name."

    query = product_name.lower().strip()
    df = products_df.copy()

    if name_col is None or name_col not in df.columns:
        return "Dataset does not contain a valid product name column."

    df["__name_lower__"] = df[name_col].astype(str).str.lower().str.strip()

    exact_matches = df[df["__name_lower__"] == query]

    if exact_matches.empty:
        matches = df[df["__name_lower__"].str.contains(query, na=False)]
    else:
        matches = exact_matches

    if matches.empty:
        return f"No information found for '{product_name}'."

    best = matches.copy()

    sort_price_col = price_min_col if price_min_col else price_max_col
    if sort_price_col and sort_price_col in df.columns:
        best["__price_num__"] = pd.to_numeric(best[sort_price_col], errors="coerce")
        best = best.dropna(subset=["__price_num__"])
        if not best.empty:
            best = best.sort_values("__price_num__")

    best_row = best.iloc[0]

    def safe_get(row, col, default="Unknown"):
        if col and col in row.index and not pd.isna(row[col]):
            return row[col]
        return default

    name         = safe_get(best_row, name_col)
    price_min    = safe_get(best_row, price_min_col)
    price_max    = safe_get(best_row, price_max_col)
    availability = safe_get(best_row, availability_col)
    store        = safe_get(best_row, store_col)
    category     = safe_get(best_row, category_col)
    url          = safe_get(best_row, url_col, "")
    weight       = safe_get(best_row, weight_col)
    brand        = safe_get(best_row, brand_col)
    image_url    = safe_get(best_row, image_url_col, "")

    lines = [
        f"Product: {name}",
        f"Brand: {brand}",
        f"Category: {category}",
    ]

    if price_min != "Unknown" and price_max != "Unknown" and price_min != price_max:
        lines.append(f"Price range: {price_min} – {price_max}")
    elif price_max != "Unknown":
        lines.append(f"Price: {price_max}")
    elif price_min != "Unknown":
        lines.append(f"Price: {price_min}")
    else:
        lines.append("Price: Unknown")

    lines.append(f"Availability: {availability}")
    lines.append(f"Store: {store}")

    if weight != "Unknown":
        lines.append(f"Weight: {weight}")

    if url:
        lines.append(f"URL: {url}")

    if image_url and image_url != url:
        lines.append(f"Image URL: {image_url}")

    return "\n".join(lines)
