from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import Base, generate_uuid, SessionLocal

from utils.passlib import generate_password_hash, check_password_hash

session = SessionLocal()


class User(Base):
    
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(100), name="uuid", default=generate_uuid, unique=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String(200))

    email = Column(String(30), unique=True, index=True)
    name = Column(String(30),  index=True)
    address = Column(Text() )
    company = Column(String(130),  nullable=True)
    department = Column(String(120),  nullable=True)
                            
    is_active = Column(Boolean, default=True)
    is_super =Column(Boolean, default=False) 

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    #保存密码使用set_password，加密密码
    def set_password(self, password):
        self.password = set_password(password)
    
    #check_password比对密码，返回True or False
    def check_password(self,  password):
        return  check_password(self.password, password)

    @property
    def groups(self):
        try:
            group_ids = [i.group_id for i in session.query(UserGroup).filter_by( user_id =self.id ).all()]
            groups = [i.name for i in session.query(Group).filter(Group.id.in_(group_ids)).all()] 
        except Exception as e:
            return []
        return groups
    
    @property   
    def permissions(self):
        try:
            group_ids = [i.group_id for i in session.query(UserGroup).filter_by( user_id =self.id ).all()]
            permission_ids = [i.group_id for i in session.query(PermissionGroup).filter( PermissionGroup.group_id.in_(group_ids) ).all()]
            permissions = [i.code for i in session.query(Permission).filter(Permission.id.in_(permission_ids)).all()] 
        except Exception as e: 
            return []
        return permissions

class Permission(Base):

    __tablename__ = "auth_permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30),  index=True)
    code = Column(String(30),  index=True)

class Group(Base):

    __tablename__ = "auth_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30),  index=True)

class UserGroup(Base):

    __tablename__ = "auth_users_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,index=True)
    group_id = Column(Integer,index=True)

class PermissionGroup(Base):
    
    __tablename__ = "auth_permission_groups"

    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer,index=True)
    group_id = Column(Integer,index=True)


