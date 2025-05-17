from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=100)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    username: str
    is_admin: bool

    class Config:
        from_attributes = True
