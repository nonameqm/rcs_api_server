from datetime import datetime, timedelta
from os import name
from typing import Optional
from fastapi import APIRouter

import bcrypt
import jwt

from fastapi import APIRouter, Depends
from pydantic.errors import EmailError
from pydantic.types import Json

from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import JSON
from starlette.responses import JSONResponse

from database.conn import db
from database.schema import User, Company, Factory, Robot, RobotTypeList, Method, SubjectTypeList, RobotDataTypeList, RobotData
from models import CompanyRegister, RegisterMessage, Token, FactoryRegister, RobotRegister, MethodRegister

from routes.logic.data_check import *


router=APIRouter(prefix="/get")

@router.get("/factory_list/{company_name}", status_code=200)
async def get_factory_list_of_company(company_name: str, session=Depends(db.session)):
    if is_company_exist(company_name)==False:
        return JSONResponse(status_code=400, content=dict(msg="Company does not exist"))
    company_id=Company.get(CompanyName=company_name).CompanyID
    factory_list=Factory.filter(CompanyID=company_id).all()
    for factory in factory_list:
        robot_list=Robot.filter(FactoryID=factory.FactoryID).all()
        setattr(factory, "Total_Robot", len(robot_list))
        on_move=0;
        for robot in robot_list:
            status=RobotData.get(RobotID=robot.RobotID, RobotDataType="robot_status")
            if status is not None:
                if status.RobotDataValue==1:
                    on_move=on_move+1
        setattr(factory, "robot_on_move", on_move)

    return factory_list



@router.get("/robot_list", status_code=200)
async def get_robot_list(company_name: Optional[str]=None, factory_name: Optional[str]=None, session=Depends(db.session)):
    robot_list=[]
    if company_name==None and factory_name==None:
        return JSONResponse(status_code=400, content=dict(msg="You need to input either factory or company"))
    
    if company_name is not None:
        if is_company_exist(company_name)==False:
            return JSONResponse(status_code=400, content=dict(msg="Company does not exist"))
        company_id=Company.get(CompanyName=company_name).CompanyID
        factory_list=Factory.filter(CompanyID=company_id).all()
        for factory in factory_list:
            robots=Robot.filter(FactoryID=factory.FactoryID).all()
            for robot in robots:
                setattr(robot, 'factory_name', Factory.get(FactoryID=robot.FactoryID).factory_name)
                robot_data_list=RobotData.filter(RobotID=robot.RobotID).all()
                for robot_data in robot_data_list:
                    setattr(robot, robot_data.RobotDataType, robot_data.RobotDataValue)
                robot_list.append(robot)
        
        return robot_list

    if factory_name is not None:
        if is_factory_exist(factory_name)==False:
            return JSONResponse(status_code=400, content=dict(msg="Factory does not exist"))
        factory_id=Factory.get(factory_name=factory_name).FactoryID
        robots=Robot.filter(FactoryID=factory_id).all()
        for robot in robots:
            robot_data_list=RobotData.filter(RobotID=robot.RobotID).all()
            for robot_data in robot_data_list:
                setattr(robot, robot_data.RobotDataType, robot_data.RobotDataValue)
            robot_list.append(robot)
        return robot_list

@router.get("/robot_data/{robot_serial}", status_code=200)
async def get_robot_data_by_serial(robot_serial: str):
    if robot_serial is None:
        return JSONResponse(status_code=400, content=dict(msg="Please Enter Robot Serial"))

    if is_robot_exist(robot_serial=robot_serial)==False:
        return JSONResponse(status_code=400, content=dict(msg="No such robot exists"))


    robot_id=Robot.get(RobotSerial=robot_serial).RobotID
    data_list=RobotData.filter(RobotID=robot_id).all()


    if len(data_list)==0:
        return JSONResponse(status_code=400, content=dict(msg="Robot data is not defined in this robot"))
    else:
        return data_list