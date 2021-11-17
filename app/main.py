from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.conn import db
from routes import index, auth, register, get, set_data


from common.config import conf

def create_app():
    c=conf()
    app=FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(index.router)
    app.include_router(auth.router)
    app.include_router(register.router)
    app.include_router(get.router)
    app.include_router(set_data.router)

    return app

app = create_app()

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=conf().PROJ_RELOAD)