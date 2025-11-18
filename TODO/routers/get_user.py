from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = get_settings()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    
        return {"email": payload.get("sub"),
                "username": payload.get("username"),
                "role": payload.get("role")}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
