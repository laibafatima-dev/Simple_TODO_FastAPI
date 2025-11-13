from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class TODODB(Base):
    __tablename__ = "TODOTABLE"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(Boolean)

    owner_of_task = Column(Integer, ForeignKey('Users.id'))
    user = relationship("Users", back_populates='todo')
 

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    todo = relationship("TODODB", back_populates='user')


