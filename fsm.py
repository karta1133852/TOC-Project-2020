from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
  
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
    
    weapon_url = "https://www.mhchinese.wiki/weapons/c/"
    
    weapon_select_type = 0
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_weapon_cate(self, event):
        text = event.message.text
        return text.lower() == "武器"
    
    def on_enter_weapon_cate(self, event):
        print("I'm entering weapon_cate")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入武器類別")
        # self.go_back()

    def on_exit_weapon_cate(self):
        print("Leaving weapon_cate")

    def is_going_to_weapon_select(self, event):
        text = event.message.text
        result = False
        global weapon_list
        for i in weapon_list:
            if weapon_list[i] == text.lower():
                result = True;
                global weapon_select_type
                weapon_select_type = i
        return result

    def on_enter_weapon_select(self, event):
        print("I'm entering weapon_select")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入" + weapon_list[weapon_select_type] + "名稱(可用'[]'代替'【】')")
        # self.go_back()

    def on_exit_weapon_select(self):
        print("Leaving weapon_select")

