from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str

    class Config:
        from_attributes = True


class UserSchemaResponse(UserSchema):
    id: int
