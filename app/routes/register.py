from datetime import datetime, timedelta
from os import name
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
from database.schema import User, Company, Factory, Robot, RobotTypeList, Method, SubjectTypeList
from models import CompanyRegister, RegisterMessage, Token, FactoryRegister, RobotRegister, MethodRegister


router=APIRouter(prefix="/register")

@router.post("/company", status_code=200)
async def register_new_company(reg_info: CompanyRegister ,session: Session=Depends(db.session)):
    """
        `Register Company`\n
        :param reg_info:\n
        :return:
    """
    if not reg_info.company_name:
        return JSONResponse(status_code=400, content=dict(msg="Company Name must be provided"))
    is_exist=is_company_exist(reg_info.company_name)
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="Company Already Exists"))
    new_user = Company.create(session, auto_commit=True, CompanyName=reg_info.company_name)
    return

@router.post("/factory", status_code=200)
async def register_new_factory(reg_info: FactoryRegister, session: Session=Depends(db.session)):
    """
        `Register Factory`\n
        :param reg_info: \n
        :return:
    """
    if not reg_info.company_name or not reg_info.factory_name:
        return JSONResponse(status_code=400, content=dict(msg="Wrong Parameters (Company and Factory Name are both needed)"))

    if is_company_exist(reg_info.company_name):
        if is_factory_exist(factory_name=reg_info.factory_name, company_name=reg_info.company_name):
            return JSONResponse(status_code=400, content=dict(msg="Factory Already Exists"))
        new_factory=Factory.create(
            session, 
            auto_commit=True,
            CompanyID=Company.get(CompanyName=reg_info.company_name).CompanyID,
            factory_name=reg_info.factory_name,
            FactoryLoc= reg_info.FactoryLoc
        )
        return

    else:
        return JSONResponse(status_code=400, content=dict(msg="No such company exists"))

@router.post("/robot", status_code=200)
async def register_new_robot(reg_info: RobotRegister, session: Session=Depends(db.session)):
    """
        `Register Robot`\n
        :param reg_info: \n
        :return:
    """
    factoryID= None
    methodID = None
    if not reg_info.robot_serial or not reg_info.robot_type or not reg_info.robot_ip:
        return JSONResponse(status_code=400, content=dict(msg="Serial, Type, Ip cannot be ommitted"))

    if reg_info.factory_name:
        if not is_factory_exist(factory_name=reg_info.factory_name):
            return JSONResponse(status_code=400, content=dict(msg="No such factory exists"))
        else: 
            factoryID= Factory.get(factory_name=reg_info.factory_name).FactoryID
    if not is_robottype_exist(reg_info.robot_type):
        #TODO : Robot Type automatically registered
        return JSONResponse(status_code=400, content=dict(msg="Check your robot type again"))

    new_robot=Robot.create(
        session,
        auto_commit=True,
        RobotSerial = reg_info.robot_serial,
        FactoryID = factoryID,  
        #TODO - MethodID Control
        MethodID = methodID,
        robot_type = reg_info.robot_type,
        loc_x = reg_info.loc_x,
        loc_y = reg_info.loc_y
    )

    return

@router.post("/method", status_code=200)
async def register_new_method(reg_info: MethodRegister, session:Session=Depends(db.session)):
    
    if not reg_info.method_file_loc or not reg_info.method_name_version or not reg_info.robot_type or not reg_info.subject_type or not reg_info.maker_email:
        return JSONResponse(status_code=400, content=dict(msg="Data is not fully given"))
    
    maker=None
    if not is_email_exist(email=reg_info.maker_email):
        return JSONResponse(status_code=400, content=dict(msg="ID doesn't exist"))
    else:
        maker = User.get(email=reg_info.maker_email).ID

    if not is_subjecttype_exist(subject_type=reg_info.subject_type):
        return JSONResponse(status_code=400, content=dict(msg="Subject doesn't exist"))
    if not is_robottype_exist(robot_type=reg_info.robot_type):
        return JSONResponse(status_code=400, content=dict(msg="Robot doesn't exist"))

    if is_method_exist(name_version=reg_info.method_name_version):
        return JSONResponse(status_code=400, content=dict(msg="Method already exists"))

    return maker
    new_method = Method.create(
        session,
        auto_commit=True,
        MethodNameVersion= reg_info.method_name_version,
        Maker = maker,
        RobotType = reg_info.robot_type,
        SubjectType = reg_info.subject_type,
        MethodFileLoc = reg_info.method_file_loc   
    )

    return
    #TODO : Docker Image Create




def is_method_exist(name_version: str):
    get_method=Method.get(MethodNameVersion=name_version)
    if get_method:
        return True
    return False

def is_subjecttype_exist(subject_type: str):
    get_subjecttype=SubjectTypeList.get(SubjectType=subject_type)
    if get_subjecttype:
        return True
    return False

def is_robottype_exist(robot_type: str):
    get_robottype=RobotTypeList.get(RobotType=robot_type)
    if get_robottype:
        return True
    return False

def is_factory_exist(factory_name: str, company_name: str=None):
    if company_name is not None:
        company_id=Company.get(CompanyName=company_name).CompanyID
        get_factory=Factory.get(CompanyID=company_id, factory_name=factory_name)
        if get_factory:
            return True
        return False
        
    else:
        get_factory=Factory.get(factory_name=factory_name)
        if get_factory:
            return True
        return False

def is_company_exist(name: str):
    get_company=Company.get(CompanyName=name)
    if get_company:
        return True
    return False

async def is_email_exist(email: str):
    get_email=User.get(email=email)
    if get_email:
        return True
    return False
