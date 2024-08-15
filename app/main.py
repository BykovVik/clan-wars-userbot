from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .config import userbot, origins
from .database import create_all_tables, SessionLocal
from .shemas import UserCreate, UserRetrieve
from .models import User, Clan

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
        rating=data.rating)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Add Database connect   
def db_connect():
    try:
        create_all_tables()
        print("Tables created successfully")
    except Exception as e:
        print(e)


    