from typing import List, Optional

from pydantic import BaseModel

from . import models
from core.serializer import modelSerializer

 
class UserBase(BaseModel):
    username: str
    email: str
    name: str= None
    company: str= None
    department: str= None
    address: str= None 


class UserCreate(UserBase):
    password: str
    is_active: bool= True
    # is_super: bool = False


class UserUpdate(BaseModel): 

    email:str = None
    company: Optional[str]= None
    department: Optional[str]= None
    password: str = None
    name: str= None 
    is_active: bool= True
    

class UserPatch(BaseModel):

    email: Optional[str]= None
    name: Optional[str]= None
    company: Optional[str]= None
    department: Optional[str]= None
    address: Optional[str]= None 
    password: Optional[str]= None
    is_active: Optional[bool]= None
    

class User(UserBase):
    id:int
    uuid:str
    is_active: bool= True
    groups:list
    permissions:list
    # is_super: bool = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# class GroupBase(BaseModel):
#     name: str 

#     class Config:
#         orm_mode = True


# class Group(GroupBase):
#     id:int 

#     class Config:
#         orm_mode = True



# class Permission(BaseModel):
#     name: str 

# class UserGroup(BaseModel):
#     user_id: int 
#     group_id: int 

# class PermissionGroup(BaseModel):
#     permission_id: int 
#     group_id: int  


GroupBase = modelSerializer(models.Group, exclude=['id'])
PermissionBase = modelSerializer(models.Permission, exclude=['id'])
UserGroupBase = modelSerializer(models.UserGroup, exclude=['id'] )
PermissionGroupBase = modelSerializer(models.PermissionGroup, exclude=['id'])

class Group(GroupBase):
    id:int

class Permission(PermissionBase):
    id:int

class UserGroup(UserGroupBase):
    id:int

class PermissionGroup(PermissionGroupBase):
    id:int

