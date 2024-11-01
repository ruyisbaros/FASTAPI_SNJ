from datetime import datetime

from pydantic import BaseModel, EmailStr


#### POST #######
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


##### User ########
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    def __getitem__(self, key):
        return self.__dict__[key]


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
