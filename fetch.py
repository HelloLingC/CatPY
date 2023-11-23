import requests
import re
from urllib.parse import quote
from config import *



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
    api = converter_api + "/clash&append_type=true&url=" + text
    res = requests.get(api)
    if res.status_code != 200:
         print("Error: " + res.status_code)
         return ""
    # TODO
    modText = res.text.replace("t.me/ConfigsHub", "US 美國 1x")
    return modText
