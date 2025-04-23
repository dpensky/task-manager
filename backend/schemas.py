from pydantic import BaseModel
from typing import Optional


# ---------- User Schemas ----------

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Task Schemas ----------

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    is_completed: bool

    class Config:
        orm_mode = True
