from typing import Any, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from starlette.responses import Response

from sqlalchemy.orm import Session

from appcations.users import crud, models, schemas
from core.security import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.database import get_db
router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(*, username: str = Body(...), password: str = Body(...), db:Session = Depends(get_db), respose:Response ):
    user = crud.user.authenticate(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # respose.set_cookie("airwaybill-session", access_token)  //mvc set cookies
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/logout")
# async def logout(response:Response):
#     response.delete_cookie("airwaybill-session")
#     return {'msg':'ok'}


