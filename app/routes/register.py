from datetime import datetime, timedelta
from fastapi import APIRouter

import bcrypt
import jwt

from fastapi import APIRouter, Depends
from pydantic.types import Json

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.conn import db
from database.schema import Company
from models import CompanyRegister, RegisterMessage, Token


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

def is_company_exist(name: str):
    get_company=Company.get(CompanyName=name)
    if get_company:
        return True
    return False