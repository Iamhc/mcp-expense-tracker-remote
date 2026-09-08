from fastmcp import FastMCP 
import os
from pymongo import MongoClient
mcp=FastMCP(name="expense-tracker")

def init_db():
  URI=os.getenv("MONGO_URI")
  client=MongoClient(URI)
  db=client["Cluster0"]
  collection=db["expense-tracker"]
  return collection

expenses=init_db()

@mcp.tool
def add(expense:int,spent_on:str,date:str,time:str):
   expenditure={
      "expense":expense,
      "spent_on":spent_on,
      "date":date,
      "time":time
   }
   result=expenses.insert_one(expenditure)

   if result.inserted_id:
    return f"result :{result.inserted_id}"
   else:
    return "not done"

@mcp.tool
def show(date:str="",time:str="",start_date:str="",end_date:str=""):
  query={}
  
  if start_date and end_date:
    query["date"]={"$gte":start_date,"$lte":end_date}
  elif date:
    query["date"]=date

  if time:
    query["time"]=time

  result=list(expenses.find(query))

  for r in result:
    r["_id"]=str(r["_id"])
  
  return result
  

if __name__=="__main__":
    mcp.run()
