import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *

import requests
from bs4 import BeautifulSoup


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_templete_message_button(reply_token, title, text, actions):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text="Buttons template",
        template=ButtonsTemplate(
            title=title,
            text=text,
            actions=actions
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def get_text_message(text):
    return TextSendMessage(text=text)
    
def get_templete_message_button(title, text, actions):
    message = TemplateSendMessage(
        alt_text="Buttons template",
        template=ButtonsTemplate(
            title=title,
            text=text,
            actions=actions
        )
    )
    return message

weapon_list_url = [
    "great_swords", "long_sword", "sword_shield", "dual_blades",
    "hammer", "hunting_horn", "lances", "gunlance",
    "switch_ace", "insect_glaive", "charge_blade", "light_bowgun", "heavy_bowgun", "bow"
]
weapon_cate_url = "https://www.mhchinese.wiki/weapons/c/"
moster_cate_url = "https://www.mhchinese.wiki/monsters"
mhw_wiki_url = "https://www.mhchinese.wiki"

soup = None

def check_weapon_name(weapon_type, name):
    
    name = name.upper()
    name = name.replace("III", "Ⅲ")
    name = name.replace("II", "Ⅱ")
    name = name.replace("I", "Ⅰ")
    name = name.replace("[", "【")
    name = name.replace("]", "】")
    name = name.replace("［", "【")
    name = name.replace("］", "】")
    
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
        result += "名稱：" + td_tags[0].string
        result += "\n稀有度：Rare " + td_tags[1].string
        result += "\n攻擊：" + td_tags[3].string
        result += "\n屬性："
        for span in td_tags[6].findAll("span"):
            result += span.string + " "
    
    return result

def check_monster_name(name, size): # size = 0:大型魔物 1:小型魔物
    
    r = requests.get(moster_cate_url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        lists = soup.findAll("ul", {"class" : "link-list"})
        for tag in lists[size].findAll("a"):
            if name == tag.string:
                print(name)
                return tag.get("href")
    
    return ""

def get_monster_info(url):

    result = ""
    url = mhw_wiki_url + url
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        global soup
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        td_tag = table.findAll("td")
        result += "種類：" + td_tag[0].string
        result += "\n簡介：" + td_tag[1].get_text()
        table = soup.findAll("table", {"class" : "simple-table"})
        """result += "\n弱點：\n"
        table[0]
        result += "\n素材：\n"
        tr_tags = table[4].findAll("tr")
        for i in range(1, len(tr_tags)):
            result += ""
        """
    return result

def get_monster_details(type):
    result = ""
    
    
    return result


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
