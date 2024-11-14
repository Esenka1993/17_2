from fastapi import APIRouter


router1 = APIRouter(prefix='/user', tags=['user'])

@router1.get("/")
async def all_users():
    pass

@router1.get("/user_id")
async def user_by_id():
    pass

@router1.post("/create")
async def create_user():
    pass

@router1.put("/update")
async def update_user():
    pass

@router1.delete("/delete")
async def delete_user():
    pass
