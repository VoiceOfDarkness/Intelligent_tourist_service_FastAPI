from datetime import datetime
from typing import List
from uuid import UUID, uuid1

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from places.destination import TourBasicInfo

router = APIRouter()


pending_users = dict()
approved_users = dict()


class Signup(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    birthday: datetime


class User(BaseModel):
    id: UUID
    username: str
    password: str


class Tourist(BaseModel):
    id: UUID
    login: User
    date_signed: datetime
    booked: int
    tours: List[TourBasicInfo]


@router.post('/ch02/user/signup/')
def signup(signup: Signup):
    try:
        userid = uuid1()
        login = User(id=userid, username=signup.username, password=signup.password)
        tourist = Tourist(id=userid, login=login, date_signed=datetime.now(), booked=0, tours=list())
        tourist_json = jsonable_encoder(tourist)
        pending_users[userid] = tourist_json
        return JSONResponse(content=tourist_json, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={'message': 'invalid operation'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
