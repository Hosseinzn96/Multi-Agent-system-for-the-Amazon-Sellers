from src.agents.product_catalog.tools import get_product_info

def main():
    product_name = input("Enter a product name: ")
    print("\n--- RESULT ---")
    print(get_product_info(product_name))

if __name__ == "__main__":
    main()
