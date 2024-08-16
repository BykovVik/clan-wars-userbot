from sqlalchemy.orm import Session
from .models import User
from .shemas import UserCreate

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()