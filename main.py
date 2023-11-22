# from pathlib import Path
from telethon import TelegramClient, events
from urllib.parse import urlencode
import requests
import handlers
from config import *

client = TelegramClient(session_path, api_id, api_hash)

def handleMessages(messages):
    linkNum = 0
    linkCollection = ""
    for msg in messages:
        if linkNum >= req_nodes_num:
            break
        text = msg.text
        if text.startwith("ss://"):
            print("A SS node")
        elif text.startwith("vmess://"):
            print("A VMess node")
        elif text.startwith("trojan://"):
            print("A trojan node")
        else:
            # Unknown message
            continue
        
        linkCollection += "{text}|"
        linkNum += 1
    # Finish
    linkCollection = urlencode(linkCollection[:-1])
    clashCfg = convert2Clash(linkCollection)
    if clashCfg == "":
        return
    with open(outputFoldername + 'clash_config.yaml', 'w') as file:
        file.write(clashCfg)

def convert2Clash(text):
    api = converter_api + "/sub?target=clash&url={text}"
    res = requests.get(api)
    if res.status_code != 200:
         print("Error: {resstatus_code}")
         return ""
    return res.text

async def main():
    me = await client.get_me()
    print("Login succeed!\nUsername: {me.username}, ID: {me.id}\n")
    chat = await client.get_entity(chat_id)
    messages = await client.get_message(chat, limit=req_nodes_num*8)

    # client.add_event_handler(handlers.command_handler, events.NewMessage(outgoing=True, pattern="^!"))
    
with client:
    client.loop.run_until_complete(main())
    