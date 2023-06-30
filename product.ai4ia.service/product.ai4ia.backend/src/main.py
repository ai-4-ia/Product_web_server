import uvicorn
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from src import models
from src.db.database import SessionLocal, engine, Base
from src import routers

# Create database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Router
app.include_router(routers.user.router)


@app.get("/")
async def home_page():
    return {"message": "Welcome to my homepage"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
