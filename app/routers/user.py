from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify



router1 = APIRouter(prefix='/user', tags=['user'])

@router1.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router1.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    select_user = db.scalar(select(User).where(User.id == user_id))
    if select_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return select_user

@router1.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'
    }

@router1.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    updated_user = db.scalar(select(User).where(User.id == user_id))
    if updated_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(
                                   firstname=update_user.firstname,
                                   lastname=update_user.lastname,
                                   age=update_user.age,
                                    slug=slugify(update_user.firstname)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router1.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    deleted_user = db.scalar(select(User).where(User.id == user_id))
    if deleted_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.execute(delete(User).where(User.id == user_id).values())
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
