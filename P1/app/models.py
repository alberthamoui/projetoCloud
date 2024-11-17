from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserList(BaseModel):
    users: List[User]

class Login(BaseModel):
    email: EmailStr
    senha: str

class Consult(BaseModel):
    email: EmailStr
    nome: str