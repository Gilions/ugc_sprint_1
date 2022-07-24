from pydantic import BaseModel


class Event(BaseModel):
    movie_timestamp: int
    movie_id: str
    user_id: int

class UserValues(BaseModel):
    key: str
    value: str
