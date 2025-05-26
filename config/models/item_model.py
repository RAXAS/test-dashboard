from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field
from uuid import UUID


class ItemCreate(BaseModel):
    title: str  # = Field(..., min_length=1, max_length=80)
    description: str

class RandomId(BaseModel):
    id: UUID

class BaseItem(BaseModel):
    title: str
    description: str
    id: UUID
    owner_id: UUID


class ItemsPage(BaseModel):
    data: List[BaseItem]
    count: int

class ValidationErrorCtx(BaseModel):
    min_length: Optional[int] = None
    max_length: Optional[int] = None


class ValidationErrorItem(BaseModel):
    type: str
    loc: List[Union[str, int]]
    msg: str
    input: Any
    ctx: Optional[ValidationErrorCtx] = None

class ValidationErrorItemResponse(BaseModel):
    detail: List[ValidationErrorItem]