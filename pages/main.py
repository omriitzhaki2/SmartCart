import pandas as pd

def main():
    products_path = 'data/products.csv'
    departments_path = 'data/departments.csv'
    aisles_path = 'data/aisles.csv'

    products_df = pd.read_csv(products_path)
    departments_df = pd.read_csv(departments_path)
    aisles_df = pd.read_csv(aisles_path)

    products_df = pd.merge(products_df, departments_df, on='department_id', how='left')
    products_df = pd.merge(products_df, aisles_df, on='aisle_id', how='left')
    products_df.to_csv('data/supermarket_products.csv')


if __name__ == '__main__':
    main()
