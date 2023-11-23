# from pathlib import Path
from telethon import TelegramClient, events
import asyncio
import handlers
from datetime import datetime
import fetch
from config import *

lasttime_fetch_exec = None

client = TelegramClient(session_path, api_id, api_hash)

async def fetchTask():
    global lasttime_fetch_exec
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
    print(event.raw_text)
    if '/status' in event.raw_text:
        print("Status Command >")
        if lasttime_fetch_exec is None:
            await event.respond("Haven't exec")
        else:
            lastExec = lasttime_fetch_exec.strftime("%Y-%m-%d %H:%M:%S")
            await event.respond("Last exec time: " + lastExec)
    if '/start' in event.raw_text:
        asyncio.ensure_future(fetchTask())

if __name__ == "__main__":
    print("Telefetch start to connect\n")
    client.start()
    client.run_until_disconnected()