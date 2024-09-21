import os
from telethon import utils
from telethon import TelegramClient, events, sync, types, functions
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

client = TelegramClient('session', api_id, api_hash)

async def get_messages(name, limit):
    async with client:
        person = await client.get_entity(str(name))
        id = utils.get_peer_id(person)
        messages = []
        async for message in client.iter_messages(id, limit=int(limit), from_user=id):
            messages.append((message.id, message.text))
        return messages

async def get_details(name, limit):
    messages = await get_messages(name, limit)
    return {"messages": messages}