from database.conn import db
from database.schema import User, Company, Factory, Robot, RobotTypeList, Method, SubjectTypeList, RobotDataTypeList
from models import CompanyRegister, RegisterMessage, Token, FactoryRegister, RobotRegister, MethodRegister

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

def is_robot_exist(robot_serial: str=None, robot_ip: str=None):
    get_robot_through_serial=Robot.get(RobotSerial=robot_serial)
    get_robot_through_robot_ip=Robot.get(robot_ip=robot_ip)
    if get_robot_through_robot_ip or get_robot_through_serial:
        return True
    else:
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
