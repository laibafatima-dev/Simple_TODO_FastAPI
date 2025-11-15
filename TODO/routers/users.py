from fastapi import APIRouter, HTTPException, Depends, status
from .. import models, schemas, database
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    tags=['user']
)
get_db = database.get_db

@router.put("/user", response_model=schemas.ShowUsers, status_code = status.HTTP_200_OK)
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)



@router.get("/user/show{user_id}", response_model=schemas.ShowUsers, status_code = status.HTTP_200_OK)
def show_user_detail(user_id: int, db: Session = Depends(get_db)):
    return user.show_user_detail(user_id, db)