from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status



def get_all_tasks(db: Session, current_user):
    tasks = db.query(models.TODODB).all()
    return tasks



def create(request: schemas.TODO, db: Session, current_user):

    id_by_user = db.query(models.TODODB).filter(models.TODODB.id_by_user == request.id_by_user).all()
    if id_by_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"task id should be unique")

    
    creator = current_user["username"]

    # Assign only if admin    

    new_task = models.TODODB(
        id_by_user = request.id_by_user,
        description=request.description,
        status=request.status,
        creator=creator,
        assigner=None
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task





def delete(task_id: int, db: Session, current_user):
    task = db.query(models.TODODB).filter(models.TODODB.id_by_user == task_id).first()

    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to delete")

    if current_user['username'] != task.creator and current_user['username'] != "admin":
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to delete this task")

    db.delete(task)
    db.commit()
    return {"deleted successfully"}




def update_task(task_id: int, request: schemas.TODO, db: Session, current_user):
    task = db.query(models.TODODB).filter(models.TODODB.id_by_user == task_id).first()


    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to update")

    if current_user['username'] != task.creator and current_user['username'] != "admin":
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to update this task")
    
    id_by_user = db.query(models.TODODB).filter(models.TODODB.id_by_user == request.id_by_user).all()
    if id_by_user and task_id != task.id_by_user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"this id is already taken")


    task.description = request.description
    task.status = request.status
    task.id_by_user = request.id_by_user

    db.commit()
    db.refresh(task)
    return task


def get_specific_task(id: int, db: Session):
    task = db.query(models.TODODB).filter(models.TODODB.id_by_user == id).first()
    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"The task with this id {id} is not found here")
    return task



def assign_task(task_id: int,username : str , db: Session, current_user):
    print("this is current user")
    print(current_user)
    if current_user['role'] != 'admin':
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail=f"you are unauthorize to assign task")
    
    task = db.query(models.TODODB).filter(models.TODODB.id_by_user == task_id).first()

    if not task:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {task_id} to delete")
    
    user = db.query(models.TODODB).filter(models.Users.username==username).first()

    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username")
    
    user.assigner = current_user['role']
    return user
    
