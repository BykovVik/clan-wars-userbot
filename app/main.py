from fastapi import FastAPI
from app.config import userbot

app = FastAPI()

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
    




    