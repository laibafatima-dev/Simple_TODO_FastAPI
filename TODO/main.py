from fastapi import FastAPI
from . import models
from .database import engine
from .routers import tasks, users, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(tasks.router)
app.include_router(users.router)

# @app.get("/")
# def welcome():
#     return {"message": "Welcome to my todo list"}

# @app.post("/add", status_code=status.HTTP_201_CREATED, tags=['task'])
# def add_item(request : schemas.TODO, db: Session = Depends(get_db)):
#     new_item = models.TODODB(description = request.description, status = request.status, owner_of_task = 1)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item
    
# @app.get("/tasks", response_model=List[schemas.ShowTODO], tags=['task'])
# def get_task_details(db: Session = Depends(get_db)):
#     tasks = db.query(models.TODODB).all()
#     return tasks


# @app.get("/tasks/specific{id}", status_code=200, response_model=schemas.ShowTODO, tags=['task'])
# def get_specific_task(id, response : Response,db: Session = Depends(get_db)):
#     task = db.query(models.TODODB).filter(models.TODODB.id == id).first()
#     if not task:
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"The task with this id {id} is not found here")
#     return task

# @app.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['task'])
# def delete_item(item_id : int, db: Session = Depends(get_db)):

#     task = db.query(models.TODODB).filter(models.TODODB.id == item_id).first()
#     if not task:
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"item with this id {item_id} is not here and cab't be deleted")
    
#     db.delete(task)
#     db.commit()
#     return 
   


# @app.put("/add/{item_id}", status_code=status.HTTP_202_ACCEPTED, tags=['task'])
# def update_item(item_id,request : schemas.TODO ,db: Session = Depends(get_db)):
#     task = db.query(models.TODODB).filter(models.TODODB.id == item_id).first()
#     print("Incoming request data:", request)


#     if not task:
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no task with this id {item_id} to update")

#     task.description = request.description
#     task.status = request.status

#     db.commit()
#     db.refresh(task)
#     return {"details": "Successfully updates"}
    


#-------- creating users----------
# @app.put("/user", tags=['user'])
# def create_user(request : schemas.User, db: Session = Depends(get_db)):

#     new_user = models.Users(name = request.name, email = request.email, password = Hash.argon2(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user



# @app.get("/user/show{user_id}", response_model=schemas.ShowUsers, status_code = status.HTTP_200_OK, tags=['user'])
# def show_user_detail(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()

#     if not user:
#         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with this id {user_id}")
    
#     return user



# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port="9000")