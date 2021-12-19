from dataclasses import FrozenInstanceError
from enum import auto
from typing import Text
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.expression import false, null
from sqlalchemy.sql.sqltypes import TEXT, VARCHAR, Float

from database.conn import Base, db


class BaseMixin:
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1: cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        get_id = self.id
        ret = None

        self._session.flush()
        if qs > 0 :
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        print(self.served)
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()

class User(Base, BaseMixin):
    __tablename__ = "testuser"
    ID = Column(Integer, primary_key=True)
    email = Column(String(length=255), nullable=False)
    pw = Column(String(length=255), nullable=False)
    usertype = Column(Enum("Admin", "Company-Host", "Company-User", "Developer"), default="Company-User")
    name = Column(String(length=255), nullable=True)
    status = Column(Enum("active", "deleted", "blocked"), default="active")
    company_id = Column(Integer, ForeignKey("Company.CompanyID"))
    phone_number = Column(String(length=20), nullable=True, unique=True)
    profile_img = Column(String(length=1000), nullable=True)
    sns_type = Column(Enum("FB", "G", "K", 'N'), nullable=True)
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

class RobotTypeList(Base, BaseMixin):
    __tablename__ = "robottypelist"
    RobotType = Column(String(length=30), primary_key=True)

class RobotDataTypeList(Base, BaseMixin):
    __tablename__ = "robotdatatypelist"
    RobotType = Column(String(length=30), ForeignKey("robottypelist.robottype"),primary_key=True)
    RobotDataType = Column(String(length=30), nullable=False, primary_key=True)
    Explanation = Column(TEXT, nullable=True)
    RealTime = Column(Integer, nullable=False, default=1)

class RobotData(Base, BaseMixin):
    __tablename__ = "robotdata"
    RobotDataID = Column(Integer, primary_key=True)
    RobotType = Column(String(length=30), ForeignKey("robotdatatypelist.RobotType"))
    RobotDataType = Column(String(length=30), ForeignKey("robotdatatypelist.RobotDataType"))
    RobotID = Column(Integer, ForeignKey("robot.RobotID"))
    RobotDataValue = Column(Float, nullable=False, default=0)

class SubjectTypeList(Base, BaseMixin):
    __tablename__ = "subjecttypelist"
    SubjectType = Column(String(length=30), primary_key=True)

class Company(Base, BaseMixin):
    __tablename__ = "company"
    CompanyID = Column(Integer, primary_key=True)
    CompanyName = Column(String(length=255), nullable=False)

class Factory(Base, BaseMixin):
    __tablename__ = "factory"
    FactoryID = Column(Integer, primary_key=True)
    CompanyID = Column(Integer, ForeignKey("company.CompanyID"), nullable=False)
    FactoryLoc = Column(String(length=100), nullable=True)
    factory_name = Column(String(length=200), nullable=False)

class Robot(Base, BaseMixin):
    __tablename__ = "robot"
    RobotID = Column(Integer, primary_key=True)
    RobotSerial = Column(String(length=30), nullable=True)
    FactoryID = Column(Integer, ForeignKey("factory.FactoryID"), nullable=True)
    MethodID = Column(Integer, ForeignKey("method.MethodID"), nullable=True)
    robot_type = Column(String(length=30), ForeignKey("robottypelist.RobotType"), nullable=False, default='X-ARM6 Test')
    robot_ip = Column(String(length=100), nullable=False, unique=True)
    loc_x = Column(Float, nullable=True)
    loc_y = Column(Float, nullable=True)

class Method(Base, BaseMixin):
    __tablename__ = "method"
    MethodID = Column(Integer, primary_key=True)
    MethodNameVersion = Column(TEXT, nullable=False)
    Maker = Column(Integer, ForeignKey("testuser.ID"), nullable=False)
    RobotType = Column(String(length=30), ForeignKey("robottypelist.RobotType"), nullable=False)
    SubjectType = Column(String(length=30), ForeignKey("subjecttypelist.SubjectType"), nullable=False)
    MethodFileLoc = Column(TEXT, nullable=False)


