# from pathlib import Path
from telethon import TelegramClient, events
from urllib.parse import quote
import requests
import re
import handlers
from config import *

client = TelegramClient(session_path, api_id, api_hash)

def handleMessages(messages):
    linkNum = 0
    linkCollection = ""
    for msg in messages:
        if linkNum >= req_nodes_num:
            break
        match = re.search('`([^`]+)`', msg.text)
        if not match:
           continue
        text = match.group(1)
        if text.startswith("ss://"):
            print("A SS node")
        elif text.startswith("vmess://"):
            print("A VMess node")
        elif text.startswith("trojan://"):
            print("A trojan node")
        else:
            # Unknown message
            continue
        
        linkCollection += text + "|"
        linkNum += 1
    # Finish
    # Urlencode the query param
    linkCollection = quote(linkCollection[:-1])
    clashCfg = convert2Clash(linkCollection)
    if clashCfg == "":
        return
    with open(outputFoldername + 'clash_config.yaml', 'w') as file:
        file.write(clashCfg)

def convert2Clash(text):
    api = converter_api + "/sub?target=clash&url=" + text
    res = requests.get(api)
    if res.status_code != 200:
         print("Error: " + res.status_code)
         return ""
    return res.text

async def main():
    me = await client.get_me()
    print('Login succeed!\nUsername: {me.username}, ID: {me.id}\n'.format())
    chat = await client.get_entity(chat_id)
    messages = await client.get_messages(chat, limit=req_nodes_num*8)
    handleMessages(messages)
    # client.add_event_handler(handlers.command_handler, events.NewMessage(outgoing=True, pattern="^!"))
    
with client:
    client.loop.run_until_complete(main())
    