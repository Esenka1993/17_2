from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    select_task = db.scalar(select(Task).where(Task.id == task_id))
    if select_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return select_task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, create_task: CreateTask):
    user_with_task = db.scalar(select(User).where(User.id == user_id))
    if user_with_task is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(insert(Task).where(User.id == user_id)).values(username=create_task.username,
                                   firstname=create_task.firstname,
                                   lastname=create_task.lastname,
                                   age=create_task.age)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    updated_task = db.scalar(select(Task).where(Task.id == task_id))
    if updated_task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db.execute(update(Task).where(Task.id == task_id).values(
        username=update_task.username,
        firstname=update_task.firstname,
        lastname=update_task.lastname,
        age=update_task.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    deleted_task = db.scalar(select(Task).where(Task.id == task_id))
    if deleted_task is None:
        raise HTTPException(status_code=404, detail='Task was not found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}