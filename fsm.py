from transitions.extensions import GraphMachine

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
mhw_wiki_url = "https://www.mhchinese.wiki"

weapon_select_type = 0
current_url = ""

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
        return text.lower() == "返回"
    
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
        send_text_message(reply_token, "請輸入 " + weapon_list[weapon_select_type] + " 的名稱(可用'[]'代替'【】')")
    
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
