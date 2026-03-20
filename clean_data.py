import pandas as pd
import numpy as np
from datetime import datetime
import re

# ---------------------------------------------------
# Utility Function : Cleaning Report
# ---------------------------------------------------

def cleaning_report(before_df, after_df, name):

    print(f"\n---- Cleaning Report: {name} ----")

    print("Rows before:", len(before_df))
    print("Rows after :", len(after_df))
    print("Duplicate rows removed:", len(before_df) - len(after_df))

    print("\nNull counts BEFORE:")
    print(before_df.isnull().sum())

    print("\nNull counts AFTER:")
    print(after_df.isnull().sum())


# ---------------------------------------------------
# Email Validation
# ---------------------------------------------------

def validate_email(email):

    if pd.isna(email):
        return False

    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return bool(re.match(pattern, str(email)))


# ---------------------------------------------------
# 1.1 Clean customers.csv
# ---------------------------------------------------

def clean_customers():

    df = pd.read_csv("customers.csv")

    before = df.copy()

    # Strip whitespace
    df["name"] = df["name"].astype(str).str.strip()
    df["region"] = df["region"].astype(str).str.strip()

    # Fill missing region
    df["region"] = df["region"].replace("", np.nan)
    df["region"] = df["region"].fillna("Unknown")

    # Lowercase email
    df["email"] = df["email"].astype(str).str.lower()

    # Validate email
    df["is_valid_email"] = df["email"].apply(validate_email)

    # Parse signup_date
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    # Remove duplicates based on customer_id
    df = df.sort_values("signup_date")
    df = df.drop_duplicates(subset="customer_id", keep="last")

    # Save cleaned file
    df.to_csv("customers_clean.csv", index=False)

    # Print report
    cleaning_report(before, df, "customers")

    return df


# ---------------------------------------------------
# Date Parser (Supports multiple formats)
# ---------------------------------------------------

def parse_date(date_value):

    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]

    for fmt in formats:
        try:
            return datetime.strptime(str(date_value), fmt)
        except:
            continue

    return pd.NaT


# ---------------------------------------------------
# 1.2 Clean orders.csv
# ---------------------------------------------------

def clean_orders():

    df = pd.read_csv("orders.csv")

    before = df.copy()

    # Parse order_date
    df["order_date"] = df["order_date"].apply(parse_date)

    # Drop rows where both customer_id and order_id are null
    df = df.dropna(subset=["customer_id", "order_id"], how="all")

    # Fill missing amount using product median
    df["amount"] = df.groupby("product")["amount"].transform(
        lambda x: x.fillna(x.median())
    )

    # If still missing, fill with overall median
    df["amount"] = df["amount"].fillna(df["amount"].median())

    # Normalize status column
    status_map = {
        "done": "completed",
        "complete": "completed",
        "completed": "completed",
        "pending": "pending",
        "cancelled": "cancelled",
        "canceled": "cancelled",
        "refund": "refunded",
        "refunded": "refunded"
    }

    df["status"] = (
        df["status"]
        .astype(str)
        .str.lower()
        .map(status_map)
        .fillna("pending")
    )

    # Derived column
    df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")

    # Save cleaned file
    df.to_csv("orders_clean.csv", index=False)

    # Print report
    cleaning_report(before, df, "orders")

    return df


# ---------------------------------------------------
# Main Pipeline
# ---------------------------------------------------

def main():

    print("Starting Data Cleaning Pipeline")

    customers = clean_customers()

    orders = clean_orders()

    print("\nCleaning completed successfully.")


# ---------------------------------------------------
# Run Script
# ---------------------------------------------------

if __name__ == "__main__":
    main()