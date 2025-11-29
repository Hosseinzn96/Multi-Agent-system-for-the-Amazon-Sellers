from src.config import DATA_CSV_PATH
from src.data.loader import load_products_df, detect_columns

products_df = load_products_df(DATA_CSV_PATH, nrows=2000)
columns = detect_columns(products_df)

name_col        = columns["name_col"]
price_min_col   = columns["price_min_col"]
price_max_col   = columns["price_max_col"]
availability_col= columns["availability_col"]
store_col       = columns["store_col"]
category_col    = columns["category_col"]
url_col         = columns["url_col"]
weight_col      = columns["weight_col"]
brand_col       = columns["brand_col"]
image_url_col   = columns["image_url_col"]
