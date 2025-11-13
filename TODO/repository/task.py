from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_all_tasks(db: Session):
    tasks = db.query(models.TODODB).all()
    return tasks

def create(request: schemas.TODO, db: Session):
    new_item = models.TODODB(description = request.description, status = request.status, owner_of_task = 1)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def delete(item_id: int, db: Session):
    task = db.query(models.TODODB).filter(models.TODODB.id == item_id).first()
    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"item with this id {item_id} is not here and cab't be deleted")
    
    db.delete(task)
    db.commit()
    return 

def update_item(item_id: int, request: schemas.TODO, db: Session):
    task = db.query(models.TODODB).filter(models.TODODB.id == item_id).first()
    print("Incoming request data:", request)


    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {item_id} to update")

    task.description = request.description
    task.status = request.status

    db.commit()
    db.refresh(task)
    return {"details": "Successfully updates"}


def get_specific_task(id: int, db: Session):
    task = db.query(models.TODODB).filter(models.TODODB.id == id).first()
    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"The task with this id {id} is not found here")
    return task

def add_item(request: models.TODODB, db: Session):
    new_item = models.TODODB(description = request.description, status = request.status, owner_of_task = 1)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item