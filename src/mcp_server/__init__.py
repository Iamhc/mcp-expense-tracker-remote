import os
from fastmcp import FastMCP
from pymongo import MongoClient

mcp = FastMCP(name="expense-tracker", auth=None)

_collection = None

def get_collection():
    """Lazily connect to MongoDB on first use, not at import time."""
    global _collection
    if _collection is None:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI environment variable not set")
        client = MongoClient(uri)
        _collection = client["Cluster0"]["expense-tracker"]
    return _collection

@mcp.tool
def add(expense: int, spent_on: str, date: str, time: str = "") -> str:
    """Add a new expense record to MongoDB."""
    expenses = get_collection()
    expenditure = {"expense": expense, "spent_on": spent_on, "date": date, "time": time}
    result = expenses.insert_one(expenditure)
    return f"result :{result.inserted_id}" if result.inserted_id else "not done"

@mcp.tool
def show(date: str = "", time: str = "", start_date: str = "", end_date: str = "") -> list:
    """Query expenses by single date, date range, or time."""
    expenses = get_collection()
    query = {}
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    elif date:
        query["date"] = date
    if time:
        query["time"] = time
    result = list(expenses.find(query))
    for r in result:
        r["_id"] = str(r["_id"])
    return result

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)