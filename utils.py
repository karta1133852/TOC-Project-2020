import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
from bs4 import BeautifulSoup


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

weapon_list_url = [
    "great_swords", "long_sword", "sword_shield", "dual_blades",
    "hammer", "hunting_horn", "lances", "gunlance",
    "switch_ace", "insect_glaive", "charge_blade", "light_bowgun", "heavy_bowgun", "bow"
]
weapon_cate_url = "https://www.mhchinese.wiki/weapons/c/"
mhw_wiki_url = "https://www.mhchinese.wiki"

def check_weapon_name(weapon_type, name):
    
    name = name.upper()
    name = name.replace("I", "Ⅰ")
    name = name.replace("[", "【")
    name = name.replace("]", "】")
    name = name.replace("[", "［")
    name = name.replace("]", "］")
    r = requests.get(weapon_cate_url + weapon_list_url[weapon_type])
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class" : "simple-table"})
        for div in table.findAll("div"): 
            div.decompose()
        for tag in table.findAll("a", {"class" : "weapon-link"}):
            if name == tag.get_text().strip():
                print(name)
                return tag.get("href")
    
    return ""

def get_weapon_details(url):

    result = ""
    url = mhw_wiki_url + url
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class" : "simple-table"})
        td_tags = table.findAll("td")
        result += "名稱：\t" + td_tags[0].string
        result += "\n稀有度：\tRare" + td_tags[1].string
        result += "\n攻擊：\t" + td_tags[3].string
        result += "\n屬性：\t"
        for span in td_tags[6].findAll("span"):
            result += span.string + " "
    
    return result


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
