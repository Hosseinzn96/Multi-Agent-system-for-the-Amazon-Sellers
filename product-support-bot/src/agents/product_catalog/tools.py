import pandas as pd
import re


# ----------------------------
# Normalization & tokenization
# ----------------------------

def normalize(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().str.strip()


def tokenize(text: str) -> set[str]:
    """
    Normalize and split text into alphanumeric tokens.
    Handles case, punctuation, commas, &, etc.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return set(text.split())


def category_matches(user_category: str, dataset_category: str) -> bool:
    """
    Returns True if user category intent overlaps
    with dataset category tokens.
    """
    if not user_category or not dataset_category:
        return False

    user_tokens = tokenize(user_category)
    dataset_tokens = tokenize(dataset_category)

    return len(user_tokens & dataset_tokens) > 0


# ----------------------------
# Imports from loader
# ----------------------------

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


# ----------------------------
# Product lookup (UNCHANGED)
# ----------------------------

def get_product_info(product_name: str) -> str:
    if not isinstance(product_name, str) or not product_name.strip():
        return "Please provide a valid product name."

    query = product_name.lower().strip()
    df = products_df.copy()

    if name_col is None or name_col not in df.columns:
        return "Dataset does not contain a valid product name column."

    df["__name_lower__"] = normalize(df[name_col])

    exact_matches = df[df["__name_lower__"] == query]

    if exact_matches.empty:
        matches = df[df["__name_lower__"].str.contains(query, na=False, regex=False)]
    else:
        matches = exact_matches

    if matches.empty:
        return f"No information found for '{product_name}'."

    best = matches.copy()

    sort_price_col = price_min_col if price_min_col else price_max_col
    if sort_price_col and sort_price_col in df.columns:
        best["__price_num__"] = pd.to_numeric(best[sort_price_col], errors="coerce")

        priced = best.dropna(subset=["__price_num__"])
        if not priced.empty:
            best = priced.sort_values("__price_num__")
         # else: keep original matches even if price is missing
    best_row = best.iloc[0]


    def safe_get(row, col, default="Unknown"):
        if col and col in row.index and not pd.isna(row[col]):
            return row[col]
        return default

    lines = [
        f"Product: {safe_get(best_row, name_col)}",
        f"Brand: {safe_get(best_row, brand_col)}",
        f"Category: {safe_get(best_row, category_col)}",
    ]

    price_min = safe_get(best_row, price_min_col)
    price_max = safe_get(best_row, price_max_col)

    if price_min != "Unknown" and price_max != "Unknown" and price_min != price_max:
        lines.append(f"Price range: {price_min} – {price_max}")
    elif price_max != "Unknown":
        lines.append(f"Price: {price_max}")
    elif price_min != "Unknown":
        lines.append(f"Price: {price_min}")
    else:
        lines.append("Price: Unknown")

    lines.append(f"Availability: {safe_get(best_row, availability_col)}")
    lines.append(f"Store: {safe_get(best_row, store_col)}")

    weight = safe_get(best_row, weight_col)
    if weight != "Unknown":
        lines.append(f"Weight: {weight}")

    url = safe_get(best_row, url_col, "")
    if url:
        lines.append(f"URL: {url}")

    image_url = safe_get(best_row, image_url_col, "")
    if image_url and image_url != url:
        lines.append(f"Image URL: {image_url}")

    return "\n".join(lines)


# ----------------------------
# Discovery tools (UPDATED)
# ----------------------------

def list_categories() -> str:
    if not category_col or category_col not in products_df.columns:
        return "No category information available."

    categories = normalize(products_df[category_col]).unique()

    if len(categories) == 0:
        return "No categories found."

    return "Available categories:\n- " + "\n- ".join(sorted(categories))


def list_brands(category: str | None = None) -> str:
    df = products_df

    if not brand_col or brand_col not in df.columns:
        return "No brand information available."

    if category:
        df = df[
            products_df[category_col]
            .dropna()
            .astype(str)
            .apply(lambda c: category_matches(category, c))
        ]

    brands = normalize(df[brand_col]).dropna().unique()

    if len(brands) == 0:
        return "No brands found."

    return "Available brands:\n- " + "\n- ".join(sorted(brands))


def list_products(category: str | None = None, brand: str | None = None) -> str:
    df = products_df

    if category:
        df = df[
            products_df[category_col]
            .dropna()
            .astype(str)
            .apply(lambda c: category_matches(category, c))
        ]

    if brand:
        df = df[normalize(df[brand_col]) == brand.lower().strip()]

    if df.empty:
        return "No products found."

    names = (
        df[name_col]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    return "Products:\n- " + "\n- ".join(sorted(names[:20]))
