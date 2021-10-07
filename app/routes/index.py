from collections import namedtuple
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.base import state_attribute_str
from starlette.responses import Response

from database.conn import db
from database.schema import User

router = APIRouter()

@router.get("/")
async def index(session: Session = Depends(db.session),):
    current_time=datetime.utcnow()
    return Response(f"Notification API (UTC: {current_time.strftime('%Y.%m.%d.%H:%M:%S')})")