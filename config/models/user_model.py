from typing import List, Dict, Any, Union

from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    username: EmailStr  # Тут баг на бэке, просит передавать username, а не email при логине
    password: str


class UserCreds(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class GetUser(BaseModel):
    email: str
    is_active: bool
    is_superuser: bool
    full_name: str
    id: UUID

class UserToken(BaseModel):
    access_token: str
    token_type: str

class ErrorDetail(BaseModel):
    type: str
    loc: List[str]
    msg: str
    input: str
    ctx: Dict[str, Any]

class ErrorUserResponse(BaseModel):
    detail: Union[str, List[ErrorDetail]]
