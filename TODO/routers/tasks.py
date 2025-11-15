from fastapi import APIRouter, HTTPException, status , Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..repository import task
from . import oauth2, get_user

router = APIRouter(
    tags=['tasks']
)
get_db = database.get_db

@router.post("/add/task", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowTODO)
def add_task(request : schemas.TODO, db: Session = Depends(get_db), current_user: dict = Depends(get_user.get_current_user)):
    return task.create(request, db, current_user)
    

@router.get("/Get/All/task", response_model=List[schemas.ShowTODO])
def get_task_details(db: Session = Depends(get_db), current_user: dict = Depends(get_user.get_current_user)):
    return task.get_all_tasks(db, current_user)


@router.get("/tasks/specific{id}", status_code=200, response_model=schemas.ShowTODO)
def get_specific_task(id,db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_specific_task(id, db)

@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id : int, db: Session = Depends(get_db), current_user: dict = Depends(get_user.get_current_user)):
    return task.delete(task_id, db, current_user)


@router.put("/task/update{task_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowTODO)
def update_task(task_id,request : schemas.TODO ,db: Session = Depends(get_db), current_user: dict = Depends(get_user.get_current_user)):
    return task.update_task(task_id, request, db, current_user)

@router.patch("/task/assign{task_id}/{username}", status_code=200, response_model=schemas.ShowTODO)
def assign_task(task_id: int, username: str,db: Session = Depends(get_db), current_user: dict = Depends(get_user.get_current_user)):
    return task.assign_task(task_id, username, db, current_user)