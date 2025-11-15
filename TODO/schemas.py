from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
from uuid import UUID
from .enums import roles, task_status

class TODO(BaseModel):
    id_by_user : int
    description: str
    status: task_status.TaskStatus = task_status.TaskStatus.pending


#---------USER SCHEMAS--------

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: Optional[str] = Field(None)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=15)
    role : roles.UserRolesEnum = roles.UserRolesEnum.user

    # ---- PASSWORD VALIDATION ----

    @field_validator("password")
    def validate_password(cls, pwd):
        pattern = r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&]).{8,}$"
        if not re.match(pattern, pwd):
            raise ValueError(
                "Password must contain at least: 1 uppercase letter, "
                "1 digit, and 1 special character (@$!%*?&)."
            )
        return pwd

    # ---- USERNAME VALIDATION ----

    @field_validator("username")
    def validate_username(cls, value):
        pattern = r"^[A-Za-z0-9_]+$"
        if not re.match(pattern, value):
            raise ValueError("Username may contain only letters, digits, and underscores.")
        return value


class ShowUsers(BaseModel):
    username: str
    email: str
    role : roles.UserRolesEnum = roles.UserRolesEnum.user

    class Config:
        from_attributes = True  


class ShowTODO(BaseModel):
    id_by_user : int
    description: str
    status: task_status.TaskStatus
    task_creator: ShowUsers
    task_assigner: Optional[ShowUsers] = None

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role : str
    username : str


