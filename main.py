# from pathlib import Path
from telethon import TelegramClient, events
import asyncio
import handlers
from datetime import datetime
import fetch
from config import *

lasttime_fetch_exec = None

client = TelegramClient(session_path, api_id, api_hash)

async def doFetch():
    me = await client.get_me()
    print('Task starts execute!\nUsername: {}, ID: {}\n'.format(me.username, me.id))
    chat = await client.get_entity(chat_id)
    messages = await client.get_messages(chat, limit=req_nodes_num*8)
    fetch.handleMessages(messages)
    lasttime_fetch_exec = datetime.now()

async def fetchTask():
    global lasttime_fetch_exec
    while True:
        await doFetch()
        await asyncio.sleep(fetch_task_interval)

def getCurrentTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@client.on(events.NewMessage(outgoing=True))
async def command_handler(event):
    # print("Message recevied: " + event.raw_text)
    time = getCurrentTime()
    headMsg = f"**{time}**\n"
    if '!status' in event.raw_text:
        print("Status Command >")
        if lasttime_fetch_exec is None:
            await event.edit("Status: Fetch haven't been executed")
        else:
            lastExec = lasttime_fetch_exec.strftime("%Y-%m-%d %H:%M:%S")
            await event.edit("{headMsg}Telefetch is running\nLast exec time: " + lastExec)
    if '!start' in event.raw_text:
        asyncio.ensure_future(fetchTask())
        await event.edit(f"{headMsg}The fetch task starts running!")
    if '!refetch' in event.raw_text:
        await event.edit(f"{headMsg}Refetching...")
        await fetch
        await event.edit(f"{headMsg}Succeed to redo the fetch task!")

if __name__ == "__main__":
    print("Telefetch starts to connect\n")
    client.start()
    client.run_until_disconnected()