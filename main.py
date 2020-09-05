import uvicorn
from fastapi import Request

from core import get_app, render
from core.database import engine

from appcations.users import models as users_model 
# from appcations.users.router import router as users_router

from appcations.users.routers.users import user_router as user_router
from appcations.users.routers.group import group_router as group_router
from appcations.users.routers.auth import router as auth_router




app = get_app()

# users_model.Base.metadata.create_all(bind=engine)

 
app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/users")
app.include_router(group_router, prefix="/api/groups")




if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=3200, reload=True, debug=True)