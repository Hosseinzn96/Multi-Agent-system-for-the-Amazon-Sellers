from src.config import DATA_CSV_PATH
from src.data.loader import load_products_df

def main():
    print("CSV Path:", DATA_CSV_PATH)

    df = load_products_df(DATA_CSV_PATH, nrows=2000)
    print(f"Loaded {len(df)} rows")

    # Try to detect the main product name column
    name_columns = [c for c in df.columns if "name" in c.lower() or "title" in c.lower()]

    if not name_columns:
        print("\nNo 'name' or 'title' columns found. Columns available:")
        print(df.columns)
        return

    name_col = name_columns[0]
    print(f"\nUsing product name column: {name_col}\n")

    print("=== First 30 Product Names ===")
    for i, name in enumerate(df[name_col].head(30), start=1):
        print(f"{i}. {name}")

if __name__ == "__main__":
    main()
