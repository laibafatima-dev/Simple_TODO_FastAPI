from .. import schemas, models, hashing
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_user(request: schemas.User, db: Session):
    new_user = models.Users(name = request.name, email = request.email, password = hashing.Hash.argon2(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show_user_detail(user_id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"no user with this id {user_id}")
    
    return user