import pandas as pd
import argparse
from pandas.errors import EmptyDataError

# --------------------------------------------------
# Default configuration (can be overridden by CLI)
# --------------------------------------------------

CONFIG = {
    "customers": "customers_clean.csv",
    "orders": "orders_clean.csv",
    "products": "products.csv",
    "out_monthly": "monthly_revenue.csv",
    "out_top_customers": "top_customers.csv",
    "out_category": "category_performance.csv",
    "out_region": "regional_analysis.csv"
}

# --------------------------------------------------
# Safe data loader
# --------------------------------------------------

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {file_path} ({len(df)} rows)")
        return df
    except FileNotFoundError:
        print(f"ERROR: File not found -> {file_path}")
        exit()
    except EmptyDataError:
        print(f"ERROR: File is empty -> {file_path}")
        exit()


# --------------------------------------------------
# Merge datasets
# --------------------------------------------------

def merge_data(customers, orders, products):

    # orders + customers
    orders_with_customers = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="left"
    )

    # orders_with_customers + products
    full_data = pd.merge(
        orders_with_customers,
        products,
        left_on="product",
        right_on="product_name",
        how="left"
    )

    # unmatched counts
    missing_customers = orders_with_customers["name"].isna().sum()
    missing_products = full_data["product_name"].isna().sum()

    print("\nMerge Report")
    print("Orders without matching customer:", missing_customers)
    print("Orders without matching product:", missing_products)

    return full_data


# --------------------------------------------------
# Monthly Revenue
# --------------------------------------------------

def monthly_revenue(full_data, output):

    df = full_data[full_data["status"] == "completed"]

    result = (
        df.groupby("order_year_month")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_revenue"})
    )

    result.to_csv(output, index=False)

    print("Saved:", output)


# --------------------------------------------------
# Top Customers
# --------------------------------------------------

def top_customers(full_data, output):

    df = full_data[full_data["status"] == "completed"]

    result = (
        df.groupby(["customer_id", "name", "region"])["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_spend"})
        .sort_values("total_spend", ascending=False)
        .head(10)
    )

    result.to_csv(output, index=False)

    print("Saved:", output)

    return result


# --------------------------------------------------
# Category Performance
# --------------------------------------------------

def category_performance(full_data, output):

    df = full_data[full_data["status"] == "completed"]

    result = (
        df.groupby("category")
        .agg(
            total_revenue=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            number_of_orders=("order_id", "count")
        )
        .reset_index()
    )

    result.to_csv(output, index=False)

    print("Saved:", output)


# --------------------------------------------------
# Regional Analysis
# --------------------------------------------------

def regional_analysis(full_data, output):

    df = full_data[full_data["status"] == "completed"]

    customers_per_region = df.groupby("region")["customer_id"].nunique()
    orders_per_region = df.groupby("region")["order_id"].count()
    revenue_per_region = df.groupby("region")["amount"].sum()

    result = pd.DataFrame({
        "customers": customers_per_region,
        "orders": orders_per_region,
        "total_revenue": revenue_per_region
    }).reset_index()

    result["avg_revenue_per_customer"] = (
        result["total_revenue"] / result["customers"]
    )

    result.to_csv(output, index=False)

    print("Saved:", output)


# --------------------------------------------------
# Churn Calculation
# --------------------------------------------------

def add_churn_flag(full_data, top_customers_df, output):

    df = full_data[full_data["status"] == "completed"]

    latest_date = pd.to_datetime(df["order_date"]).max()

    last_orders = (
        df.groupby("customer_id")["order_date"]
        .max()
        .reset_index()
    )

    last_orders["order_date"] = pd.to_datetime(last_orders["order_date"])

    last_orders["churned"] = (
        latest_date - last_orders["order_date"]
    ).dt.days > 90

    result = pd.merge(
        top_customers_df,
        last_orders[["customer_id", "churned"]],
        on="customer_id",
        how="left"
    )

    result.to_csv(output, index=False)

    print("Updated with churn flag:", output)


# --------------------------------------------------
# Main Pipeline
# --------------------------------------------------

def main(args):

    customers = load_csv(args.customers)
    orders = load_csv(args.orders)
    products = load_csv(args.products)

    full_data = merge_data(customers, orders, products)

    monthly_revenue(full_data, args.out_monthly)

    top_df = top_customers(full_data, args.out_top_customers)

    category_performance(full_data, args.out_category)

    regional_analysis(full_data, args.out_region)

    add_churn_flag(full_data, top_df, args.out_top_customers)

    print("\nAnalysis completed successfully.")


# --------------------------------------------------
# CLI Arguments
# --------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--customers", default=CONFIG["customers"])
    parser.add_argument("--orders", default=CONFIG["orders"])
    parser.add_argument("--products", default=CONFIG["products"])

    parser.add_argument("--out_monthly", default=CONFIG["out_monthly"])
    parser.add_argument("--out_top_customers", default=CONFIG["out_top_customers"])
    parser.add_argument("--out_category", default=CONFIG["out_category"])
    parser.add_argument("--out_region", default=CONFIG["out_region"])

    args = parser.parse_args()

    main(args)