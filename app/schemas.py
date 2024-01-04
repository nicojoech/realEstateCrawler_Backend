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


class TokenData(BaseModel):
    username: str


class CrawlerAgent(BaseModel):
    name: str
    min_area: float
    max_price: float
    number_of_rooms: int
    zip_code: str
    state: str
    rent: bool
    type: str

    class Config:
        from_attributes = True


class CrawlerAgentResponse(CrawlerAgent):
    id: int

