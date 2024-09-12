from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    user_id: int
    score: int
    penalties: int
    is_capitan: bool
    clan_id: Optional[int]

class UserRetrieve(BaseModel):
    id: int
    name: str
    user_id: int
    score: int
    penalties: int
    is_capitan: bool
    clan_id: Optional[int]

class UserClanUpdate(BaseModel):
    clan_id: int

class ClanCreate(BaseModel):
    title: str
    chat_id: int
    wins: int
    losses: int

class ClanRetrieve(BaseModel):
    id: int
    title: str
    chat_id: int
    wins: int
    losses: int