from datetime import datetime

class User(object):   

    def __init__(self,
        cpf: str, name: str, username: str, password: str, email: str, active: str, fone: str, email_confirmed_at: datetime,
        cnpj: str, occupation: str) -> None:        
    
        self.cpf = cpf
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.active = active
        self.fone = fone
        self.email_confirmed_at = email_confirmed_at
        self.cnpj = cnpj
        self.occupation = occupation

class Aluno(object):   

    def __init__(self,name, start, end, status) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.status = status
