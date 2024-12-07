from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    telegram_user_id: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr

class User(BaseModel):
    id: int
    telegram_user_id: str
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool

    class Config:
        from_attributes = True
