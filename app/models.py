from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """
    Сreating a users table in the database
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(BigInteger)
    score = Column(Integer)
    penalties = Column(Integer)
    rating = Column(Integer)
    clan_id = Column(Integer, ForeignKey("clans.id"), nullable=True)
    clan = relationship("Clan", back_populates="users")

class Clan(Base):
    """
    Сreating a clans table in the database
    """

    __tablename__ = "clans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    chat_id = Column(BigInteger)
    users = relationship("User", back_populates="clan")
    wins = Column(Integer)
    losses = Column(Integer)
    rating = Column(Integer)