from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    user_id: int
    score: int
    penalties: int
    rating: int

class UserRetrieve(BaseModel):
    name: str
    user_id: int