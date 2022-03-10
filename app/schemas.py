from typing import List, Optional

from pydantic import BaseModel, validator

from .security import get_password_hash

class FavCharacterBase(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str

class FavCharacterCreate(FavCharacterBase):
    pass

class FavCharacter(FavCharacterBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @validator('password', pre=True)
    def has_the_password(cls, v):
        return get_password_hash(v)

class User(UserBase):
    id: int
    favorite_char: List[FavCharacter] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

