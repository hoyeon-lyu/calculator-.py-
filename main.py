import GUI
import tokeni
import json

with open("setting.json", "r", encoding="utf-8") as f:
    setting = json.load(f)

class term_calc:
    def setting(self):
        pass
    def start(self):
        print("Hello! Your current information here!")
        print(json.dumps(setting, indent = 4))
        if setting["user_info"]["isdefault"] == True:
            answer = input("Setting's now default. Change the setting?[Y/N]").lower()
            if answer == "y":
                setting()
            elif answer == "n":
                print("Skip the setting!")

#I'm going to edit this things tomorrow. exam's next week...