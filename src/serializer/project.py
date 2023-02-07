import ipdb
from enum import Enum
from typing import Optional
from datetime import datetime
from . import CoreModel, validator, DateTimeModelMixin, Field, ValidationError, Extra
from src.repository.user import UserRepository
from src.adapters.project import Project

class StatusEnum(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    STOPPED = "STOPPED"
    DONE = "DONE"

 
# ipdb.set_trace()
class ProjectSchema(DateTimeModelMixin):       
    class Config:
        orm_mode = True
        # orm_model = Project
        extra = Extra.forbid
        # recursive_model

    name: str
    start:datetime =  Field(default_factory=datetime.utcnow)
    end: datetime | None
    status: str = Field(default=StatusEnum.IN_PROGRESS)
    manager: int | None

    @validator("manager")
    def manager_id_exists(cls, value):
        ipdb.set_trace()
        if value and not UserRepository().exists(value.id):
            raise ValueError("Invalid user_id")


# erro=None
# try:
#     ProjectSchema()
#     ipdb.set_trace()
# except Exception as err:
#     ipdb.set_trace()
#     erro=err
    # user_id = Column(ForeignKey('users.id'), primary_key=False)
    # user = relationship("User", back_populates="projects")

    
    # tasks = relationship("Contract", back_populates="project")
    
    
   # @validator("manager")
   # def manager_id_exists(cls, value):
   #     ipdb.set_trace()
   #     if value and not UserRepository.exists(value.id):
   #         raise ValueError("Invalid user_id")

# if __name__:
try:
#         ipdb.set_trace()
    project = ProjectSchema(name="Projeto 2", end=datetime.now())
except ValidationError as e:
    ipdb.set_trace()
    print(e)