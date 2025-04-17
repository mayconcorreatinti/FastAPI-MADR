from pydantic import BaseModel, EmailStr


class message(BaseModel):
    message: str


class credentials(BaseModel):
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
