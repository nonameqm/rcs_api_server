from datetime import datetime
from enum import Enum
from typing import List

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr, IPvAnyAddress



class DataUpdate(BaseModel):
    robot_serial: str=None
    type: str=None
    value: float=None

class MethodRegister(BaseModel):
    method_name_version: str = None
    maker_email : str = None
    robot_type : str = None
    subject_type : str = None
    method_file_loc : str = None

class RobotRegister(BaseModel):
    robot_serial : str = None
    factory_name : str = None
    method_id : str = None
    robot_type : str = None
    robot_ip : str = None
    loc_x : float = None
    loc_y : float = None

class CompanyRegister(BaseModel):
    company_name : str = None

class FactoryRegister(BaseModel):
    factory_name : str = None
    company_name : str = None
    FactoryLoc : str = None

class TestUserRegister(BaseModel):
    email: str = None
    pw: str = None
    company: str = None
    name: str = None
    usertype: str = None
    

class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"

class RegisterMessage(BaseModel):
    message: str = None;    

class Token(BaseModel):
    Authorization: str = None

class EmailRecipients(BaseModel):
    name: str
    email: str

class SendMail(BaseModel):
    email_to: List[EmailRecipients] = None

class MessageOk(BaseModel):
    message: str = Field(default="OK")

class UserToken(BaseModel):
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode= True


class UserMe(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class AddApiKey(BaseModel):
    user_memo: str = None

    class Config:
        orm_mode = True

class GetApiKeyList(AddApiKey):
    id: int = None
    access_key: str = None
    created_at: datetime = None

class GetApiKeys(GetApiKeyList):
    secret_key: str = None

class CreateAPIWhiteLists(BaseModel):
    ip_addr: str = None

class GetAPIWhiteLists(CreateAPIWhiteLists):
    id: int

    class Config:
        orm_mode = True