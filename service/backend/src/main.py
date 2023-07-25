import uvicorn
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from src.db.database import engine, Base
from src.routers import user_router

# Create database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Router
app.include_router(user_router.router)


@app.get("/")
async def home_page():
    return {"message": "Welcome to my homepage"}

# Mount the app with a prefix path
app.mount("/backend", app)
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=80, reload=True)
