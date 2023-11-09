from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    password: str

    class Config:
        orm_mode = True
