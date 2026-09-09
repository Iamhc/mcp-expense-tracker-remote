import os
from fastmcp import FastMCP 
from pymongo import MongoClient

# Initialize FastMCP (auth=None allows local HTTP testing without auth headers)
mcp = FastMCP(name="expense-tracker", auth=None)

def init_db():
    URI = os.getenv("MONGO_URI")
    if not URI:
        raise ValueError("MONGO_URI environment variable not set")
    client = MongoClient(URI)
    db = client["Cluster0"]
    collection = db["expense-tracker"]
    return collection

expenses = init_db()

@mcp.tool
def add(expense: int, spent_on: str, date: str, time: str = "") -> str:
    """Add a new expense record to MongoDB Atlas."""
    expenditure = {
        "expense": expense,
        "spent_on": spent_on,
        "date": date,
        "time": time
    }
    result = expenses.insert_one(expenditure)

    if result.inserted_id:
        return f"result :{result.inserted_id}"
    return "not done"

@mcp.tool
def show(date: str = "", time: str = "", start_date: str = "", end_date: str = "") -> list:
    """Query expenses by single date, date range, or time."""
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
    # Runs standard HTTP mode locally on 127.0.0.1:8000
    mcp.run(transport="http", host="0.0.0.0", port=8000)