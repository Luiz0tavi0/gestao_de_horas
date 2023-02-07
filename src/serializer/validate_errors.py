from typing import Any
from pydantic.error_wrappers import ErrorWrapper
import ipdb
# from pydantic.dataclasses import Dataclass
from typing import List, Optional, Sequence, Tuple, Type, Union
from pydantic import BaseModel, Field, validator
from pydantic.error_wrappers import ValidationError, ErrorList


#
# class BaseError(BaseModel):
#     type : str # "/errors/incorrect-user-pass",
#     title : str # "Incorrect username or password.",
#     status : int # 401,
#     detail : str # "Authentication failed due to incorrect username or password.",
#     instance : str # "/login/log/abc123"


class ErrorSchema(BaseModel):
    field: str = Field(title='campo', alias='loc')
    msg: str
    type: str

#    ipdb.set_trace()
    @validator("field", pre=True)
    def turn_in_str(cls, value):
        # ipdb.set_trace()
        if type(value) is tuple and len(value) > 0:
            # ipdb.set_trace()
            return value[0]


class BaseErrorSchema(BaseModel):
    #    ipdb.set_trace()
    title: str
    errors: List[ErrorSchema]
    instance: str = Field("Instance de erro genérico")
    status: int  # 401

    class Config:
        arbitrary_types_allowed = True
        # validate_assignment=True
    # orm_mode = True
    # model = User
    # extra = Extra.forbid

    # ipdb.set_trace()


class ErrorUserValidateSchema(BaseErrorSchema):
    ...


class ErrorUserIntegrity(BaseModel):
    title: str = Field("Integrity Error")
    error: str
    instance: str = Field("User operation")
    status_code: int  # 401


Loc = Tuple[Union[int, str], ...]
ReprArgs = Sequence[Tuple[Optional[str], Any]]


class ValidationErrorWithStatus(ValueError):
    def __init__(self, *args: object, status_code: Optional[int] = 422) -> None:

        self.status_code = status_code
        super().__init__(*args)

#     __slots__ = 'exc', '_loc', 'status_error'
#     def __init__(self, exc: Exception, loc: Union[str, 'Loc'], status_error:Optional[int]=None) -> None:
#         super().__init__(exc, loc)
#         self.status_error = status_error
#
#     def __repr_args__(self) -> 'ReprArgs':
#         return [('exc', self.exc), ('loc', self.loc_tuple()), ('status_error', self.status_error)]
