from dotenv import load_dotenv
import os
from pyrogram import Client

load_dotenv()
userbot = Client('bot', os.getenv("API_ID"), os.getenv("API_HASH"), phone_number=os.getenv("PHONE"))

# origins
origins = [
    "http://localhost:3000",
]

