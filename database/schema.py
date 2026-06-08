from pydantic import BaseModel

from typing import Optional


# USER REGISTRATION

class UserCreate(BaseModel):

    username: str

    email: str

    password: str


# USER LOGIN

class UserLogin(BaseModel):

    username: str

    password: str


# TOKEN RESPONSE

class Token(BaseModel):

    access_token: str

    token_type: str


# TOKEN DATA

class TokenData(BaseModel):

    username: Optional[str] = None


# USER RESPONSE

class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    class Config:

        from_attributes = True