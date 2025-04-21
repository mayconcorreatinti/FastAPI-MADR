from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


#/accounts
class Credentials(BaseModel):
    username: str
    email: EmailStr
    password: str


class PublicCredentials(BaseModel):
    id: int
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


#/novelists
class CreateNovelists(BaseModel):
    name:str


class NovelistsId(BaseModel):
    id: int
    name: str


class UpdateNovelists(BaseModel):
    name: str | None = None


class ManyNovelists(BaseModel):
    novelists: list[NovelistsId]
