from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .config import userbot, origins
from .database import create_all_tables, SessionLocal
from .shemas import UserCreate, UserRetrieve, ClanCreate, ClanRetrieve, UserClanUpdate
from .models import User, Clan
from .crud import get_user_by_user_id, get_all_clans, get_all_users, get_clan_by_id
from typing import List
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# before start up
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connect()
    yield
    print("Вышел из приложения")

# create app
app = FastAPI(lifespan=lifespan)

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Create db session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Counting the number of reactions
@app.get("/messages/{chat_id}/{message_id}")
async def get_reactions(chat_id: int, message_id: int):
    # Searching for the required message via the telegram API
    await userbot.start()
    messages = await userbot.get_messages(chat_id=chat_id, message_ids=message_id)
    await userbot.stop()

    if messages.reactions:
        count = [0 + c.count for c in messages.reactions.reactions]
        return {'reactions_count': sum(count)}
    else:
        return {'reactions_count': 0}
    
# User Registration
@app.post("/user/", response_model=UserRetrieve)
async def create_user(data: UserCreate, db: Session = Depends(get_db_session)):
    db_user = User(
        name=data.name,
        user_id=data.user_id,
        score=data.score,
        penalties=data.penalties,
        is_capitan=data.is_capitan,
        clan_id=data.clan_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User
@app.get("/user/{user_id}", response_model=UserRetrieve)
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = get_user_by_user_id(db, user_id)
    if db_user:
        return db_user
    return JSONResponse("User not found", status_code=404)

# Update User Clan
@app.patch("/user/{user_id}", response_description=UserClanUpdate)
async def update_user_clan(user_id: int, user_update:UserClanUpdate, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return JSONResponse("User not found", status_code=404)

    user.clan_id = user_update.clan_id
    db.commit()
    db.refresh(user)
    
    return user_update

# Get All Users
@app.get("/users-list/", response_model=List[UserRetrieve])
async def get_clans(db: Session = Depends(get_db_session)):
    users = get_all_users(db)
    if users:
        return users
    return JSONResponse("Users not found", status_code=404)

# Create Clan
@app.post("/clan/", response_model=ClanRetrieve)
async def create_clan(data: ClanCreate, db: Session = Depends(get_db_session)):
    db_clan = Clan(
        title=data.title,
        chat_id=data.chat_id,
        wins=data.wins,
        losses=data.losses
    )
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

# Get All Clans
@app.get("/clans-list/", response_model=List[ClanRetrieve])
async def get_clans(db: Session = Depends(get_db_session)):
    clans = get_all_clans(db)
    if clans:
        return clans
    return JSONResponse("Clans not found", status_code=404)

# Add Database connect   
def db_connect():
    try:
        create_all_tables()
        print("Tables created successfully")
    except Exception as e:
        print(e)


    