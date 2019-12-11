from transitions.extensions import GraphMachine

from linebot import LineBotApi, WebhookParser
from utils import *

weapon_list = [
    "大劍", "太刀", "片手劍", "雙劍",
    "大錘", "狩獵笛", "長槍", "銃槍",
    "斬擊斧", "操蟲棍", "充能斧", "輕弩", "重弩", "弓"
]

weapon_list_url = [
    "great_swords", "long_sword", "sword_shield", "dual_blades",
    "hammer", "hunting_horn", "lances", "gunlance",
    "switch_ace", "insect_glaive", "charge_blade", "light_bowgun", "heavy_bowgun", "bow"
]

weapon_cate_url = "https://www.mhchinese.wiki/weapons/c/"
moster_cate_url = "https://www.mhchinese.wiki/monsters"
mhw_wiki_url = "https://www.mhchinese.wiki"

weapon_select_type = 0
current_url = ""
monster_size = 0

monster_option_actions = [
        MessageTemplateAction(
            label = "弱點/肉質",
            text = "弱點"
        ),
        MessageTemplateAction(
            label = "特徵",
            text = "特徵"
        ),
        MessageTemplateAction(
            label = "素材",
            text = "素材"
        ),
        MessageTemplateAction(
            label = "返回",
            text = "返回"
        )
    ]

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_weapon_cate(self, event):
        text = event.message.text
        return text.lower() == "武器"
    
    def on_enter_weapon_cate(self, event):
        print("I'm entering weapon_cate")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入武器類別")
    
    def is_going_back_previous(self, event):
        text = event.message.text
        if text.lower() == "返回":
            reply_token = event.reply_token
            send_text_message(reply_token, "請選擇功能")
            # TODO template
            return True
    
    def is_going_to_weapon_select(self, event):
        text = event.message.text
        result = False
        global weapon_list
        for s in weapon_list:
            if s == text.lower():
                result = True;
                global weapon_select_type
                weapon_select_type = weapon_list.index(s)
        return result

    def on_enter_weapon_select(self, event):
        print("I'm entering weapon_select")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入 " + weapon_list[weapon_select_type] + " 的名稱(可用'[]'代替'【】')：")
    
    def is_going_to_weapon_details(self, event):
        text = event.message.text
        global current_url
        current_url = check_weapon_name(weapon_select_type, text)
        if current_url == "":
            reply_token = event.reply_token
            send_text_message(reply_token, "輸入錯誤，請重新輸入！")
            return False
        else:
            return True
        
    def on_enter_weapon_details(self, event):
        print("I'm entering weapon_details")
        
        result = get_weapon_details(current_url)
        reply_token = event.reply_token
        send_text_message(reply_token, result)
        
        self.go_back()
    
    def is_going_to_monster(self, event):
        text = event.message.text
        return text.lower() == "魔物"
        
    def on_enter_monster(self, event):
        print("I'm entering monster")
        
        reply_token = event.reply_token
        actions = [
            MessageTemplateAction(
                label = "大型魔物",
                text = "大型"
            ),
            MessageTemplateAction(
                label = "小型魔物",
                text = "小型"
            )
        ]
        send_templete_message_button(reply_token, "選擇", "請選擇類別", actions)
    
    def is_going_to_monster_size(self, event):
        text = event.message.text
        if text.lower() == "大型":
            monster_size = 0
            return True
        elif text.lower() == "小型":
            monster_size = 1
            return True
        return False
        
    def on_enter_monster_size(self, event):
        print("I'm entering monster_size")
        
        reply_token = event.reply_token
        if monster_size == 0:
            send_text_message(reply_token, "請輸入大型魔物名稱：")
        else:
            send_text_message(reply_token, "請輸入小型魔物名稱：")
    
    def is_going_to_monster_info(self, event):
        text = event.message.text
        global current_url
        current_url = check_monster_name(text, monster_size)
        if current_url == "":
            reply_token = event.reply_token
            send_text_message(reply_token, "輸入錯誤，請重新輸入！")
            return False
        else:
            return True
    
    def on_enter_monster_info(self, event):
        print("I'm entering monster_details")
        
        reply_token = event.reply_token
        result = get_monster_info(current_url)
        line_bot_api = LineBotApi(channel_access_token)
        line_bot_api.reply_message(reply_token, [get_text_message(result), get_templete_message_button("選擇", "請選擇詳細資料", monster_option_actions)])
    
    def is_going_to_monster_finish(self, event):
        text = event.message.text
        if text == "返回":
            return True
        else:
            reply_token = event.reply_token
            details_type = 0
            if text == "弱點":
                details_type = 0
            elif text == "特徵":
                details_type = 4
            elif text == "素材":
                details_type = 5
            result = get_monster_details(details_type)
            line_bot_api = LineBotApi(channel_access_token)
            line_bot_api.reply_message(reply_token, [get_text_message(result), get_templete_message_button("選擇", "請選擇詳細資料", monster_option_actions)])
            return False
        
    def on_enter_monster_finish(self, event):
        print("I'm entering monster_finish")
        self.go_back()
    
