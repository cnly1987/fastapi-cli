from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

from utils.cbv import InferringRouter, cbv

from core.crud import CRUDBase
from core.database import get_db

# from .database import Base
Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel) 
PatchSchemaType = TypeVar("PatchSchemaType", bound=BaseModel) 



class ViewSets(Generic[ModelType, ListSchemaType, CreateSchemaType, UpdateSchemaType, PatchSchemaType]):

    db: Session = Depends(get_db)
    
    def __init__(self, model: Type[ModelType], ListSchema:Type[ListSchemaType], CreateSchema:Type[CreateSchemaType], UpdateSchema:Type[UpdateSchemaType],PatchSchema:Type[PatchSchemaType] ):
        self.model = model
        self.ListSchema = ListSchema
        self.CreateSchema = CreateSchema
        self.UpdateSchema = UpdateSchema
        self.PatchSchema = PatchSchema
        self.crud = CRUDBase(self.model)
    
 
    def lists(self, db:Session, skip: int = 0,limit: int = 100):
        res = self.crud.get_multi(db, skip=skip, limit=limit)
        return res

    def create(self, db:Session, in_obj: ListSchemaType):
        db_obj = self.crud.get_by_name(db, name=in_obj.name)
        if db_obj:
            raise HTTPException(status_code=400, detail="name already registered")
        return self.crud.create(db, in_obj)
    
    def get(self, db:Session, id: int):
        db_obj = self.crud.get(db, id)
        if db_obj is None:                
            raise HTTPException(status_code=404, detail="not found") 
        return db_obj
    
    def delete(self, db:Session,id: int):
        db_obj = self.crud.get(db, id)
        if db_obj is None:                
            raise HTTPException(status_code=404, detail="not found")
        self.crud.delete(db, id)
        return db_obj
    
    def put(self, db:Session, id: int, obj_in:UpdateSchemaType ):
        db_obj = self.crud.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="not found")
        g = self.crud.update(db=db, db_obj=db_obj, obj_in=obj_in)
        return g
    
    def patch(self, db:Session, id: int, obj_in:UpdateSchemaType):
        db_obj = self.crud.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="not found")
        g = self.crud.update(db=db, db_obj=db_obj, obj_in=obj_in)
        return g

    def as_view(self):
        router =  APIRouter()

        @router.get('/', response_model=List[self.ListSchema])
        async def lists(db=self.db,skip: int = 0,limit: int = 100):
            return self.lists(db=db, skip=skip, limit=limit)
        
        @router.post('/', response_model=self.ListSchema)
        async def post(in_obj:self.CreateSchema, db=self.db):
            return self.create(db,in_obj=in_obj)

        @router.get("/{id}", response_model=self.ListSchema)
        async def retrive(db=self.db, id:int=id):
            return self.get(db,id)
        
        @router.delete("/{id}", response_model=self.ListSchema)
        async def delete(db=self.db, id:int=id):
            return self.delete(db,id)
        
        @router.put("/{id}", response_model=self.ListSchema)
        async def put(in_obj:self.UpdateSchema, db=self.db, id:int=id):
            return self.put(db=db,id=id, obj_in=in_obj)
        
        @router.patch("/{id}", response_model=self.ListSchema)
        async def patch(in_obj:self.PatchSchema, db=self.db, id:int=id):
            return self.patch(db=db,id=id, obj_in=in_obj)
        
        return router

        
     
