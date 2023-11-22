import asyncio
from telethon import events

async def chat_update_handler(event):
    client = event.client


async def command_handler(event):
    # Say "!pong" whenever you send "!ping", then delete both messages
    eID = event.id
    client = event.client
    text = event.text[1:]
    if text == "status":
        event.respond(eID + "Status: 123456")
    elif text == "refre":
         event.respond("Refresh Finished!")
    elif text == "bind":
        event.respond("Binded to " + text)