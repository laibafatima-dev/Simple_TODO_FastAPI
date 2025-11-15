import enum 

class UserRolesEnum(str, enum.Enum):
    user = "user"
    admin = "admin"