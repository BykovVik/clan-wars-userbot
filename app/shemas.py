from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    user_id: int
    score: int
    penalties: int
    rating: int
    clan_id: Optional[int]

class UserRetrieve(BaseModel):
    name: str
    user_id: int
    clan_id: Optional[int]

class UserClanUpdate(BaseModel):
    clan_id: int

class ClanCreate(BaseModel):
    title: str
    chat_id: int
    wins: int
    losses: int
    rating: int

class ClanResponce(BaseModel):
    id: int
    title: str
    chat_id: int
    wins: int
    losses: int
    rating: int

class ClanRetrieve(BaseModel):
    title: str
    chat_id: int