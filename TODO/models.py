from .database import Base
from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .enums import roles, task_status
import uuid

class TODODB(Base):
    __tablename__ = "TODOTABLE"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    id_by_user = Column(Integer, unique=True, nullable=False)
    description = Column(String)
    status = Column(Enum(task_status.TaskStatus), default=task_status.TaskStatus.pending)

    # who created the task
    creator = Column(String, ForeignKey("Users.username"))
    task_creator = relationship(
        "Users",
        foreign_keys=[creator],           
        back_populates="creator_user"
    )

    # who assigned the task
    assigner = Column(String, ForeignKey("Users.username"))
    task_assigner = relationship(
        "Users",
        foreign_keys=[assigner],          
        back_populates="assigner_user"
    )



class Users(Base):
    __tablename__ = "Users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)    
    username = Column(String, nullable=False, unique=True)
    name = Column(String)
    email = Column(String, unique=True)      
    password = Column(String)
    role = Column(Enum(roles.UserRolesEnum), default=roles.UserRolesEnum.user)

    # tasks this user created
    creator_user = relationship(
        "TODODB",
        foreign_keys="TODODB.creator",   
        back_populates="task_creator"
    )

    # tasks this user assigned
    assigner_user = relationship(
        "TODODB",
        foreign_keys="TODODB.assigner",  
        back_populates="task_assigner"
    )
