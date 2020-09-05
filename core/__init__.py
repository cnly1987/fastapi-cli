
import os
import sys

from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

 
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




templates = Jinja2Templates(directory='templates')

def render(html, *args, **kwargs):
    return templates.TemplateResponse(html, *args, **kwargs)  


def get_app():
    app = FastAPI()
    app.debug = True
    app.mount("/static", StaticFiles(directory=os.path.join(base_dir,'static')), name="static")
     
    app.add_middleware( CORSMiddleware, allow_origins=["*"],  allow_credentials=True,  allow_methods=["*"], allow_headers=["*"],  ) 
    
    return app