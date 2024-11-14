from fastapi import APIRouter
from routers import task, user


app = APIRouter()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router1)