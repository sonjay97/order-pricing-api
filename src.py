from fastapi import FastAPI, HTTPException
from databases import Database
import asyncpg
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
database = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/orders/{order_number}")
async def get_order(order_number: str):
    query = "SELECT * FROM orders WHERE order_number = :order_number"
    result = await database.fetch_one(query=query, values={"order_number": order_number})
    
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return dict(result)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)