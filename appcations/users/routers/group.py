
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session 


from core.database import get_db
from core.security import get_current_user, get_current_active_superuser
from utils.cbv import InferringRouter, cbv

from appcations.users import schemas, crud, models

group_router = InferringRouter()


def check_permission(perm:str='users_can_add', user = Depends(get_current_user)):
    if perm not in user.permissions:
        raise HTTPException(status_code=403, detail="permission forbid")
    return perm


@cbv(group_router)
class GroupRouter:

    db: Session = Depends(get_db)
    # user:models.User = Depends(get_current_active_superuser)

    @group_router.get('/', response_model=List[schemas.Group])  
    def lists(self, skip: int = 0,limit: int = 100):
        groups = crud.group.get_multi(self.db, skip=skip, limit=limit)
        return groups 


    @group_router.post('/', response_model=schemas.Group)
    def create(self, group: schemas.GroupBase):
        db_group = crud.group.get_by_name(self.db, name=group.name)
        if db_group:
            raise HTTPException(status_code=400, detail="Group name already registered")
        return crud.group.create(self.db, group)
    
    @group_router.delete("/{group_id}", response_model=schemas.Group)
    def delete(self, group_id: int):
        db_group = crud.group.get(self.db, group_id)
        if db_group is None:                
            raise HTTPException(status_code=404, detail="Group not found")
        crud.group.delete(self.db, group_id)
        return db_group
    
    @group_router.put("/{group_id}", response_model=schemas.Group)
    def put(self, group_id: int, group:schemas.GroupBase):
        db_group = crud.group.get(db=self.db, id=group_id)
        if not db_group:
            raise HTTPException(status_code=404, detail="Group not found")
        g = crud.group.update(db=self.db, db_obj=db_group, obj_in=group)
        return g
    
    @group_router.patch("/{group_id}", response_model=schemas.Group)
    def put(self, group_id: int, group:schemas.GroupBase):
        db_group = crud.group.get(db=self.db, id=group_id)
        if not db_group:
            raise HTTPException(status_code=404, detail="Group not found")
        g = crud.group.update(db=self.db, db_obj=db_group, obj_in=group)
        return g