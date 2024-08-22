from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .config import userbot, origins
from .database import create_all_tables, SessionLocal
from .shemas import UserCreate, UserRetrieve, ClanCreate, ClanRetrieve
from .models import User, Clan
from .crud import get_user_by_id, get_all_clans, get_all_users
from typing import List

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
@app.post("/users/", response_model=UserRetrieve)
async def create_user(data: UserCreate, db: Session = Depends(get_db_session)):
    db_user = User(
        name=data.name,
        user_id=data.user_id,
        score=data.score,
        penalties=data.penalties,
        rating=data.rating,
        clan_id=data.clan_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User
@app.get("/user/{user_id}", response_model=UserRetrieve)
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        return db_user
    return JSONResponse("User not found", status_code=404)

# Create Clan
@app.post("/clans/", response_model=ClanRetrieve)
async def create_clan(data: ClanCreate, db: Session = Depends(get_db_session)):
    db_clan = Clan(
        title=data.title,
        chat_id=data.chat_id,
        wins=data.wins,
        losses=data.losses,
        rating=data.rating
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

# Get All Users
@app.get("/users-list/", response_model=List[UserRetrieve])
async def get_clans(db: Session = Depends(get_db_session)):
    users = get_all_users(db)
    if users:
        return users
    return JSONResponse("Users not found", status_code=404)

# Add Database connect   
def db_connect():
    try:
        create_all_tables()
        print("Tables created successfully")
    except Exception as e:
        print(e)


    