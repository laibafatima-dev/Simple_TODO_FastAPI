from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from . import tokens
from typing import Annotated



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return tokens.verify_token(token, credentials_exception)