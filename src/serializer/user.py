from re import findall
import ipdb
from typing import Type, Optional, List, Dict
from datetime import datetime
from pydantic import Extra, validator, EmailStr, BaseModel, constr
from pydantic.error_wrappers import ErrorWrapper
from pydantic import Field, SecretStr
from src.serializer.project import ProjectSchema
from src.serializer import DateTimeModelMixin
from src.adapters.user import User
from src.serializer.validate_errors import BaseErrorSchema, ValidationErrorWithStatus


def validate_cpf(cls, v):
    if len(v) != 11:
        raise ValueError(f'cpf must be 11 characters long')
    if not v.isdigit():
        raise ValueError(f'cpf must have only numerical digits')
    if len(set(v)) == 1:
        return False

    sum_ = 0
    weight = 10
    for char in v[:-2]:
        sum_ += int(char) * weight
        weight -= 1
    verifying_digit = 11 - (sum_ % 11)
    if verifying_digit > 9:
        verifying_digit = 0
    if int(v[-2]) != verifying_digit:
        raise ValueError(f'cpf must be valid')

    sum_ = 0
    weight = 11
    for char in v[:-1]:
        sum_ += int(char) * weight
        weight -= 1
    verifying_digit = 11 - (sum_ % 11)
    if verifying_digit > 9:
        verifying_digit = 0
    if int(v[-1]) != verifying_digit:
        raise ValueError(f'cpf must be valid')

    return v


class UserBaseSchema(BaseModel):
    cpf: str
    name: str
    email: EmailStr
    fone: Optional[str]
    cnpj: Optional[str]
    occupation: str

    @validator('cpf', pre=True, always=True, allow_reuse=True)
    def cpf_validator(cls, v):
        return validate_cpf(cls, v)


class UserSchema(DateTimeModelMixin):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.forbid
        # arbitrary_types_allowed=True

    cpf: str
    name: str
    # password: constr(strip_whitespace=True, min_length=8)
    email: EmailStr
    active: bool = True
    fone: Optional[str]
    email_confirmed_at: Optional[datetime]
    cnpj: Optional[str]
    occupation: str
    # relationship("Project", uselist=False, back_populates="user")
    # project: Mapper[Optional["Project"]] = relationship(back_populates="manager")
    projects: Optional[List[ProjectSchema]] = []


class UserCredentialsSchema(BaseModel):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.ignore
        validate_assignment = True
        anystr_strip_whitespace = True
        fields = {'confirm_password': {'exclude': True}}

    password: str = Field(...)
    confirm_password: str = Field(...)  # constr(strip_whitespace=True, )

    @validator('password', pre=True, always=True)
    def validate_password_strength(cls, v):
        # ipdb.set_trace()
        min_length = 8
        errors = []

        if len(v) < min_length:
            errors.append(
                f'Password must be at least {min_length} characters long')
        if not findall("[a-z]", v):
            errors.append(
                "Password must contain at least one lowercase letter")
        if not findall("[A-Z]", v):
            errors.append(
                "Password must contain at least one uppercase letter")
        if not findall("[0-9]", v):
            errors.append("Password must contain at least one digit")
        if not findall("[!@#$%^&*()]", v):
            errors.append(
                "Password must contain at least one special character")

        if errors:
            raise ValidationErrorWithStatus(
                f"{'. '.join(errors)}.", status_error=422)
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if values.get('password', False) and v != values['password']:

            raise ValidationErrorWithStatus(
                'Password and confirm password must be equal.', status_error=401)
        return v


class UserUpdateCredentialsSuccess(BaseModel):
    msg: str = Field('success', )
    status_code: int = Field(200)
    status: str = Field('Ok', )


class UserSignin(UserSchema, UserCredentialsSchema):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.forbid
        validate_assignment = True


class UserSigninSuccess(BaseModel):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.forbid
        validate_assignment = True
        # fields = {'password': {'exclude': True}}

    cpf: str = Field(...)  # constr(strip_whitespace=True, min_length=11, )
    name: str = Field(...)  # constr(strip_whitespace=True, min_length=6)
    email: EmailStr


class UserLogin(BaseModel):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.forbid
        # fields = {'password': {'exclude': True}, 'email': {'exclude': True}}'confirm_password': {'exclude': True}

    password: str
    email: EmailStr


class UserLoginSuccess(BaseModel):
    class Config:
        extra = Extra.forbid

    token: str
    refresh_token: str


class UserLoginFail(BaseErrorSchema):
    title: str
    errors: str
    instance: str
    status: int  # 401

    class Config:
        arbitrary_types_allowed = True


class UserUpdateSchema(UserBaseSchema):
    class Config:
        extra = Extra.ignore

    __annotations__ = {k: Optional[v]
                       for k, v in UserBaseSchema.__annotations__.items()}


class UserUpdateSchemaSuccess(BaseModel):
    msg: str = Field('success', )
    status_code: int = Field(200)
    status: str = Field('Ok', )


class UserResetPassword(BaseModel):
    class Config:
        orm_mode = True
        model = User
        extra = Extra.forbid

    email: EmailStr
