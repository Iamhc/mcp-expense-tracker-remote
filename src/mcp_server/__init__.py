from fastmcp import FastMCP 

mcp=FastMCP(name="demo")

@mcp.tool 
def add(a:int,b:int):
  return a+b

if __name__=="__main__":
    mcp.run()
