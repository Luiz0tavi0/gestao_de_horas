from src.service_layer.interfaces.base import IService, abstractmethod
from .base import IRepository


class IUserRepository(IRepository):
    session = None

    @abstractmethod
    def get_user_by_id(self, identity):
        raise NotImplementedError()

    @abstractmethod
    def exists_by_id(self, identity) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def create(self, data):
        raise NotImplementedError()

    @abstractmethod
    def update(self, data):
        raise NotImplementedError()

    @abstractmethod
    def get_paginated(self, page: int, per_page: int):
        raise NotImplementedError()

    @abstractmethod
    def remove_by_id(self, id_: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_user_by_email(self, email: str):
        raise NotImplementedError()

    @abstractmethod
    def change_password(self, identity, data):
        raise NotImplementedError()
