from telethon import utils
from telegram import client

async def get():
    person = await client.get_entity('jayden')
    print(utils.get_peer_id(person))


with client:
    client.loop.run_until_complete(get())