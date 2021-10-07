from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.conn import db
from routes import index, auth, register


from common.config import conf

def create_app():
    c=conf()
    app=FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)


    app.include_router(index.router)
    app.include_router(auth.router)
    app.include_router(register.router)
    
    return app

app = create_app()

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=conf().PROJ_RELOAD)