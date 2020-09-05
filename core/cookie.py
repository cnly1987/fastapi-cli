from typing import Optional

from fastapi import  Depends, status
from fastapi.security import APIKeyCookie
from starlette.responses import Response, RedirectResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session

from jose import jwt

from . import render
from .database import get_db
from .security import SECRET_KEY
from appcations.users import crud, models

class APIKeyCookieCustomer(APIKeyCookie):

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.cookies.get(self.model.name)
        if not api_key:
            if self.auto_error: 
                raise HTTPException( status_code=HTTP_403_FORBIDDEN, detail="Not authenticated" )
            else:
                return None
        return api_key


cookie_sec = APIKeyCookieCustomer(name="airwaybill-session")

def get_cookie_user(session: str = Depends(cookie_sec), db:Session=Depends(get_db)):
    try:
        payload = jwt.decode(session, SECRET_KEY)
        user = crud.user.get_by_username(db, payload["sub"])
        return user
    except Exception as e: 
        print(e)
        return RedirectResponse(url='/login')

