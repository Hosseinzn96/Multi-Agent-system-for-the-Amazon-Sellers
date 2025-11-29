import pandas as pd

def load_products_df(csv_path: str, nrows: int = 2000) -> pd.DataFrame:
    return pd.read_csv(csv_path, nrows=nrows)

def detect_columns(products_df: pd.DataFrame) -> dict:
    def find_col(substrings, default=None):
        for col in products_df.columns:
            col_lower = col.lower()
            if any(s in col_lower for s in substrings):
                return col
        return default

    return {
        "name_col":        find_col(["name", "title"]),
        "price_min_col":   find_col(["amountmin", "pricemin", "min"]),
        "price_max_col":   find_col(["amountmax", "pricemax", "max"]),
        "availability_col":find_col(["availability", "instock", "in stock"]),
        "store_col":       find_col(["merchant", "store", "source"]),
        "category_col":    find_col(["category", "categories"]),
        "url_col":         find_col(["url", "link"]),
        "weight_col":      find_col(["weight"]),
        "brand_col":       find_col(["brand", "manufacturer"]),
        "image_url_col":   find_col(["imageurl", "imageurls", "picture", "img"]),
    }
