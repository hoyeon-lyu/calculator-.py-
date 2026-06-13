import GUI, tokeni, json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class OverStackException(Exception):
    pass

class setting:
    SETTINGS = None
    LANG = None
    def printSettings(self):
        def cell(set_way=setting.SETTINGS,depth=0):
            for i in set_way:
                print("\t"*depth,end="")
                if type(set_way[i]) != dict:
                    print(f"{i} : {set_way[i]}")
                else: 
                    if depth > 20:
                        raise OverStackException("setting.json file structure got Overstacked.")
                    print(f"{i}:")
                    cell(set_way[i],depth + 1)
        print("\n======================\n")
        cell()
        print("\n======================\n")

    def setSettings(self):
        #여기에다가 텍스트 기반 선택지 구현.
        def cell(set_way=setting.SETTINGS["user_info"],temp=setting.SETTINGS["setting_info"]):
            options = list(set_way.keys())
            choice = prompt(
                "What do you wanna change to : ",
                completer = WordCompleter(options),
                bottom_toolbar = lambda:
                    f"Available options: {', '.join(options)}"
            )
            try:
                if type(set_way[choice]) == dict:
                    cell(set_way[choice],temp[choice])
                else:
                    flag = True
                    while flag:
                        flag = False
                        answer = prompt("You wanna change it?[Y/N]", bottom_toolbar = lambda:f"selected : {set_way[choice]}").lower()
                        if answer == "y":
                            if temp[choice]["type"] == "bool":
                                flag_1 = True
                                while flag_1:
                                    flag_1 = False
                                    value_f = prompt(
                                        "Select a option:",
                                        completer = WordCompleter(["True", "False"]),
                                        bottom_toolbar=lambda:f"Available options:{', '.join(["True", "False"])}"
                                    )
                                    if value_f.lower() == "true":
                                        value_f = True
                                    elif value_f.lower() == "false":
                                        value_f = False
                                    if value_f != True and value_f != False:
                                        flag_1 = True
                                        print("Please try again.")
                            elif temp[choice]["type"] == "str" and type(temp[choice]["options"]) == list:
                                flag_1 = True
                                while flag_1:
                                    flag_1 = False
                                    tag = False
                                    value_f = prompt(
                                        "Select a option:",
                                        completer = WordCompleter(temp[choice]["options"]),
                                        bottom_toolbar=lambda:f"Available options:{', '.join(temp[choice]["options"])}"
                                    )
                                    for i in temp[choice]["options"]:
                                        if value_f.lower() == i.lower():
                                            tag = True
                                    if tag == False:
                                        flag_1 = True
                                        print("Please try again.")
                            else:
                                value_f = input("Enter a value:")
                            set_way[choice] = value_f
                            print(f"Complete! now : ")
                            self.printSettings()
                            again = input("...Again?[Y/N]").lower()
                            if again == "y":
                                cell()
                            else:
                                print("Done!")
                                setting.SETTINGS["is_default"] = False
                        elif answer == "n":
                            print("Canceled.")
                        else:
                            flag = True
            except KeyError as e:
                print(e)
                print("Canceled.")

            with open("setting.json", "w", encoding="utf-8") as f:
                json.dump(setting.SETTINGS, f, indent=4)

        cell()

cst = setting()
#설정 파일을 불러온다.
with open("setting.json", "r", encoding="utf-8") as f:
    setting.SETTINGS = json.load(f)
    setting.LANG = setting.SETTINGS["user_info"]["language"]

#터미널 모드
class term_calc:

    def start(self):
        print("Hello! Your current information here!")
        cst.printSettings()
        #만약 설정파일이 수정되지 않은 상태라면, 설정을 변경할것인지 묻는다. 나중에 설정에서 변경할 수 있다.
        if setting.SETTINGS["is_default"]:
            flag = True
            while flag:
                flag = False
                answer = input("Setting's now default. Change the setting?[Y/N]").lower()
                if answer == "y":
                    cst.setSettings()
                elif answer == "n":
                    print("Skip the setting!")
                else:
                    print("Please try again.")
                    #do-while문을 간접적으로 구현한다.
                    flag = True

trmc = term_calc()
trmc.start()