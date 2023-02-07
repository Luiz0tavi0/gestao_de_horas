from src.service_layer.interfaces.base import IService, abstractmethod

class IUserService(IService):
    
    @abstractmethod
    def signin(self, data):
        raise NotImplementedError()

    
    @abstractmethod
    def update(self, current_user, data):
        raise NotImplementedError()

    @abstractmethod
    def change_password(self, current_user, data):
        raise NotImplementedError()
        
    
    @abstractmethod
    def logout(self, data):
        raise NotImplementedError()