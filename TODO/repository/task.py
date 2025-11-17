from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID



def get_all_tasks(db: Session, current_user):
    if current_user['role'] == 'admin':
            tasks = db.query(models.TODODB).all()
    else:
        tasks = db.query(models.TODODB).filter(models.TODODB.creator == current_user['username']).all()

    if not tasks:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="no task created by this user")
    return tasks



def create(request: schemas.TODO, db: Session, current_user):    
    creator = current_user["username"]

    # Assign only if admin    

    new_task = models.TODODB(
        description=request.description,
        status=request.status,
        creator=creator,
        assigner=None
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task





def delete(task_id: UUID, db: Session, current_user):
    task = db.query(models.TODODB).filter(models.TODODB.id == task_id).first()

    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to delete")

    if current_user['username'] != task.creator and current_user['username'] != "admin":
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to delete this task")

    db.delete(task)
    db.commit()
    return {"deleted successfully"}




def update_task(task_id, request: schemas.TODO, db: Session, current_user):
    task = db.query(models.TODODB).filter(models.TODODB.id == task_id).first()


    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to update")

    if current_user['username'] != task.creator and current_user['username'] != "admin":
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to update this task")

    task.description = request.description
    task.status = request.status

    db.commit()
    db.refresh(task)
    return task


def get_specific_task(id, db: Session):
    task = db.query(models.TODODB).filter(models.TODODB.id == id).first()
    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"The task with this id {id} is not found here")
    return task



def assign_task(task_id,username : str , db: Session, current_user):
   
    if current_user['role'] != 'admin':
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to assign task")
    
    task = db.query(models.TODODB).filter(models.TODODB.id == task_id).first()

    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to assign")
    
    user = db.query(models.Users).filter(models.Users.username==username).first()

    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username")
    
    task.assigner = current_user['role']
    task.assigned_to = username
    db.commit()
    return task
    
