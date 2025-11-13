from fastapi import APIRouter, HTTPException, status , Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..repository import task
from . import oauth2

router = APIRouter(
    tags=['tasks']
)
get_db = database.get_db

@router.get("/")
def welcome():
    return {"message": "Welcome to my todo list"}

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_item(request : schemas.TODO, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return add_item(request, db)


@router.get("/")
def welcome():
    return {"message": "Welcome to my todo list"}

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_item(request : schemas.TODO, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.create(request, db)
    

@router.get("/tasks", response_model=List[schemas.ShowTODO])
def get_task_details(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_all_tasks(db)


@router.get("/tasks/specific{id}", status_code=200, response_model=schemas.ShowTODO)
def get_specific_task(id,db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.get_specific_task(id, db)

@router.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id : int, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.delete(item_id, db)


@router.put("/add/{item_id}", status_code=status.HTTP_202_ACCEPTED)
def update_item(item_id,request : schemas.TODO ,db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return task.update_item(item_id, request, db)