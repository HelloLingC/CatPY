# from pathlib import Path
from telethon import TelegramClient, events
import asyncio
import handlers
from datetime import datetime
import fetch
from config import *

lasttime_fetch_exec = 0

client = TelegramClient(session_path, api_id, api_hash)

async def fetchTask():
    while True:
        me = await client.get_me()
        print('Task starts execute!\nUsername: {}, ID: {}\n'.format(me.username, me.id))
        chat = await client.get_entity(chat_id)
        messages = await client.get_messages(chat, limit=req_nodes_num*8)
        fetch.handleMessages(messages)
        lasttime_fetch_exec = datetime.now()
        await asyncio.sleep(fetch_task_interval)

@client.on(events.NewMessage(outgoing=True))
async def command_handler(event):
    if '/status' in event.raw_text:
        lastExec = lasttime_fetch_exec.strftime("%Y-%m-%d %H:%M:%S")
        print("Status Command >")
        await event.respond("Last exec time: " + lastExec)

asyncio.ensure_future(fetchTask())

client.start()
client.run_until_disconnected()
    