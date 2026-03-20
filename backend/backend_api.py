import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# ---------------------------------
# Enable CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# File Paths
# ---------------------------------

# Get the directory of the current file (backend folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Navigate to the parent directory and then to the data/processed folder
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "processed")

FILES = {
    "revenue": os.path.join(DATA_DIR, "monthly_revenue.csv"),
    "customers": os.path.join(DATA_DIR, "top_customers.csv"),
    "categories": os.path.join(DATA_DIR, "category_performance.csv"),
    "regions": os.path.join(DATA_DIR, "regional_analysis.csv")
}

# ---------------------------------
# Utility function to load CSV
# ---------------------------------

def load_csv(file_path):

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Data file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df.to_dict(orient="records")


# ---------------------------------
# Health Check
# ---------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------
# Revenue Endpoint
# ---------------------------------

@app.get("/api/revenue")
def get_revenue():

    data = load_csv(FILES["revenue"])

    return {
        "count": len(data),
        "data": data
    }


# ---------------------------------
# Top Customers
# ---------------------------------

@app.get("/api/top-customers")
def get_top_customers():

    data = load_csv(FILES["customers"])

    return {
        "count": len(data),
        "data": data
    }


# ---------------------------------
# Category Performance
# ---------------------------------

@app.get("/api/categories")
def get_categories():

    data = load_csv(FILES["categories"])

    return {
        "count": len(data),
        "data": data
    }


# ---------------------------------
# Regional Analysis
# ---------------------------------

@app.get("/api/regions")
def get_regions():

    data = load_csv(FILES["regions"])

    return {
        "count": len(data),
        "data": data
    }