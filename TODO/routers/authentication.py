from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from ..hashing import Hash
from sqlalchemy.orm import Session
from . import tokens
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=['login']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user_details = db.query(models.Users).filter(models.Users.username == request.username).first()

    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user with this username')
    
    if not Hash.verify(user_details.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password')

    
    access_token = tokens.create_access_token(
            data={
                "sub": user_details.email,
                "username": user_details.username,
                "role": user_details.role
            }
        )
    return schemas.Token(access_token=access_token, token_type="bearer")
