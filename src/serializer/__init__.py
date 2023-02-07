from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field, ValidationError, Extra, EmailStr



    
class IDModelMixin(BaseModel):
    id: int

class DateTimeModelMixin(BaseModel):
    created_at: datetime = datetime.utcnow()
    updated_at: datetime | None
    # import ipdb;ipdb.set_trace()
    # @validator("created_at", "updated_at", pre=True)
    # def default_datetime(cls, value: datetime) -> datetime:
    #     import ipdb; ipdb.set_trace()
    #     return value or datetime.datetime.now()

class CoreModel(IDModelMixin, DateTimeModelMixin):
    ...
