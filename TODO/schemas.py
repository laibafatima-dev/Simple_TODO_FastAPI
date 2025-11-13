from pydantic import BaseModel


class TODO(BaseModel):
    description : str
    status : bool

#----schema for user----

class User(BaseModel):
    name : str
    email : str
    password : str


class ShowUsers(BaseModel):
    name : str
    email : str

    class Config:
        orm_mode = True

class ShowTODO(BaseModel):
    description : str
    status : bool
    user : ShowUsers
    
    
    class Config():
        orm_mode = True


class UserLogin(BaseModel):
    email : str
    password : str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
