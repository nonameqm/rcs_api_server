from datetime import datetime, timedelta
from os import name
from typing import List, Optional
from fastapi import APIRouter

import bcrypt
from fastapi.param_functions import File
import jwt

from fastapi import APIRouter, Depends
from pydantic.errors import EmailError
from pydantic.types import Json

from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import JSON
from starlette.responses import JSONResponse

from database.conn import db
from database.schema import User, Company, Factory, Robot, RobotTypeList, Method, SubjectTypeList, RobotDataTypeList, RobotData
from models import CompanyRegister, RegisterMessage, Token, FactoryRegister, RobotRegister, MethodRegister, DataUpdate

from routes.logic.data_check import *

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


@router.post("/get_execution_file", status_code=200)
async def get_execution_file(files: List[bytes]):
    for file in files:
        contents = await file.read()
        # dockerfile created

    


        