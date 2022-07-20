from pydantic import BaseModel


class Event(BaseModel):
    ip: str
    user_agent: dict
    movie_timestamp: int
    movie_id: str
    user_id: str


