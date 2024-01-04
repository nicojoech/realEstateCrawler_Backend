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


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    userId: int


class TokenData(BaseModel):
    username: str


class CrawlerAgent(BaseModel):
    name: str
    min_area: str
    max_price: str
    number_of_rooms: int
    zip_code: str
    state: str
    inUse: bool = False
    user_id: int

    class Config:
        from_attributes = True


class CrawlerAgentResponse(CrawlerAgent):
    id: int

