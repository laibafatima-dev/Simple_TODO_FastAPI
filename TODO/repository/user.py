from .. import schemas, models, hashing
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

def create_user(request: schemas.User, db: Session):

    #---email uniqueness check------
    email = db.query(models.Users).filter(models.Users.email == request.email).first()
    if email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email is already registered")

    #------username uniqueness check-----
    username = db.query(models.Users).filter(models.Users.username == request.username).first()
    if username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username is already taken")

    new_user = models.Users(username=request.username, name = request.name, email = request.email, password = hashing.Hash.argon2(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show_user_detail(user_id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == UUID(user_id)).first()

    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with this id {user_id}")
    
    return user