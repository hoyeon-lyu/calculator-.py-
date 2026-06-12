import GUI, tokeni, json
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class OverStackException(Exception):
    pass

class setting:
    SETTINGS = None

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
        def cell(set_way=setting.SETTINGS["user_info"]):
            options = list(set_way.keys())
            choice = prompt(
                "What do you wanna change to : ",
                completer = WordCompleter(options),
                bottom_toolbar = lambda:
                    f"Available options: {', '.join(options)}"
            )
            try:
                if type(set_way[choice]) == dict:
                    cell(set_way[choice])
                else:
                    flag = True
                    while flag:
                        flag = False
                        answer = prompt("You wanna change it?[Y/N]", bottom_toolbar = lambda:f"selected : {set_way[choice]}").lower()
                        if answer == "y":
                            value_f = input("Enter a value : ")
                            set_way[choice] = value_f
                            print(f"Complete! now : ")
                            self.printSettings()
                            again = input("...Again?[Y/N]").lower()
                            if again == "y":
                                cell()
                            else:
                                print("Done!")
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

#터미널 모드
class term_calc:

    def start(self):
        print("Hello! Your current information here!")
        cst.printSettings()
        #만약 설정파일이 수정되지 않은 상태라면, 설정을 변경할것인지 묻는다. 나중에 설정에서 변경할 수 있다.
        if setting.SETTINGS["user_info"]["isdefault"]:
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