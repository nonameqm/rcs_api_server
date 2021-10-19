from datetime import datetime, timedelta
from fastapi import APIRouter

import bcrypt
import jwt

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from common.const import JWT_SECRET, JWT_ALGORITHM
from database.conn import db
from database.schema import User, Company
from models import SnsType, Token, UserToken, TestUserRegister




router=APIRouter(prefix="/auth")


@router.post("/register/{sns_type}", status_code=200, response_model=Token)
async def register(sns_type: SnsType, reg_info: TestUserRegister, session: Session=Depends(db.session)):
    """
    `Register API`\n
    :param sns_type:\n
    :param reg_info:\n
    :param session:\n
    :return:
    """

    if sns_type == SnsType.email:
        if not reg_info.email or not reg_info.pw:
            return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided"))
        is_exist = await is_email_exist(reg_info.email)
        if is_exist:
            return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))
        
        if not is_company_exist(reg_info.company):
            return JSONResponse(status_code=400, content=dict(msg="No such company exists"))

        hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
        new_user = User.create(session, auto_commit=True, email=reg_info.email, pw=hash_pw,  company_id=Company.get(CompanyName=reg_info.company).CompanyID)
        token = dict(Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw'}))}")
        return token

    return JSONResponse(status_code=400, content=dict(msg="Not Supported"))

@router.post("/login/{sns_type}", status_code=200)
async def login(sns_type: SnsType, user_info: TestUserRegister):
    pass


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

def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow()+timedelta(hours=expires_delta)})
    encoded_jwt=jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt