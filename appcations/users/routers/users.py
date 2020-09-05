
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session 

from core.database import get_db
from core.security import get_current_user, get_current_active_superuser
from utils.cbv import InferringRouter, cbv

from appcations.users import schemas, crud, models

user_router = InferringRouter()




@cbv(user_router)
class UserRouter:

    db: Session = Depends(get_db)
    # user:models.User = Depends(get_current_active_superuser)

    @user_router.get('/', response_model=List[schemas.User])
    def lists(self, skip: int = 0,limit: int = 100, ):
        users = crud.user.get_multi(self.db, skip=skip, limit=limit)
        return users 


    @user_router.post('/', response_model=schemas.User)
    def create(self, user: schemas.UserCreate):
        db_user = crud.user.get_by_username(self.db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="User username already registered")
        return crud.user.create(self.db, user)
    
    @user_router.get("/{id}", response_model=schemas.User)
    def get(self, id: int):
        db_user = crud.user.get(self.db, id)
        if db_user is None:                
            raise HTTPException(status_code=404, detail="User not found") 
        return db_user
    
    @user_router.delete("/{id}", response_model=schemas.User)
    def delete(self, id: int):
        db_user = crud.user.get(self.db, id)
        if db_user is None:                
            raise HTTPException(status_code=404, detail="User not found")
        crud.user.delete(self.db, id)
        return db_user
    
    @user_router.put("/{id}", response_model=schemas.User)
    def put(self, id: int, user:schemas.UserUpdate):
        db_user = crud.user.get(db=self.db, id=id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        g = crud.user.update(db=self.db, db_obj=db_user, obj_in=user)
        return g
    
    @user_router.patch("/{id}", response_model=schemas.User)
    def patch(self, id: int, user:schemas.UserPatch):
        db_user = crud.user.get(self.db, id) 
        if db_user is None:
            raise HTTPException(status_code=400, detail="User not found")
        g = crud.user.patch(db=self.db, db_obj=db_user, obj_in=user)
        return g