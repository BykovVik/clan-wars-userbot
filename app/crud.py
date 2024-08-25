from sqlalchemy.orm import Session
from .models import User, Clan

def get_user_by_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def get_clan_by_id(db: Session, id: int):
    return db.query(Clan).filter(Clan.id == id).first()

def get_all_clans(db: Session):
    return db.query(Clan).all()