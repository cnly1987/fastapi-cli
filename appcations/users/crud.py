from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from core.crud import CRUDBase
from appcations.users.models import User, Group, Permission, UserGroup, PermissionGroup
from appcations.users.schemas import UserCreate, UserUpdate, UserPatch
from utils.passlib import check_password_hash, generate_password_hash



class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session,  username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session,  obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password=generate_password_hash(obj_in.password), 
            # is_super=obj_in.is_super,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj 
        
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User: 
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = generate_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def patch(
        self, db: Session, *, db_obj: User, obj_in: Union[UserPatch, Dict[str, Any]]
    ) -> User: 
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = generate_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password 
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session,  username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_super(self, user: User) -> bool:
        return user.is_super


 

user = CRUDUser(User)
group = CRUDBase(Group)
permission = CRUDBase(Permission)
group_user = CRUDBase(UserGroup)
group_permission = CRUDBase(PermissionGroup)