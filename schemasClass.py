from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    email: str
    password: str


class ActionDiary(BaseModel):
    datatime: List[str] = []
    incident: List[str] = []
    loss: List[str] = []


class CurrentCondition(BaseModel):
    plant: str
    term: str
    condition: str


class TechnologyTreatments(BaseModel):
    date: List[str] = []
    action: List[str] = []
    data1: List[str] = []
    data2: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Users(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

