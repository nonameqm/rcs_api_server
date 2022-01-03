from datetime import datetime, timedelta
from os import name
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile

import bcrypt
from fastapi.param_functions import File
import jwt
import shutil

from fastapi import APIRouter, Depends
from pydantic.errors import EmailError
from pydantic.types import Json

from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import JSON
from starlette.responses import JSONResponse

from database.conn import db
from database.schema import User, Company, Factory, Robot, RobotTypeList, Method, SubjectTypeList, RobotDataTypeList, RobotData
from models import CompanyRegister, RegisterMessage, Token, FactoryRegister, RobotRegister, MethodRegister, DataUpdate, CommandUpdate

from routes.logic.data_check import *
import requests

router=APIRouter(prefix="/set")

@router.post("/update_robot_data/", status_code=200)
async def update_robot_date(update_data: DataUpdate,  session: Session=Depends(db.session)):
    if is_robot_exist(robot_serial=update_data.robot_serial):
        return JSONResponse(status_code=400, content=dict(msg="Robot does not exist"))
    
    robot_id=Robot.get(RobotSerial=update_data.robot_serial).RobotID
    data=Robot.filter(RobotID=robot_id, RobotDataType=update_data.type).all()[0]

    if data is not None:
        data.RobotDataValue=update_data.value
    return


@router.post("/set_execution_file", status_code=200)
async def get_file(file: UploadFile = File(...)):
    with open('static/'+file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename}
    


@router.post("/set_command", status_code=200)
async def set_command(command: CommandUpdate=None):
    if command==None:
        return "No Command Input"
    
    
    url='http://'+command.robot_ip
    command={
        'robot_serial': command.robot_serial,
        'robot_command': command.robot_command,
        'robot_param': command.robot_param
    }
    headers={'Content-Type':'application/json; charset=utf-8'}
    response=requests.post(url, json=command, headers=headers, timeout=2)

    if response.status_code==200:
        return response.status_code
    