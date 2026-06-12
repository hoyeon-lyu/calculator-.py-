import GUI
import tokeni
import json

class OverStackException(Exception):
    pass

class setting:
    SETTINGS = None
    def getSettings(self):
        return setting.SETTINGS

    def printSettings(self):
        def cell(set_way=setting.SETTINGS,depth=0):
            for i in set_way:
                print("\t"*depth,end="")
                if type(set_way[i]) != dict:
                    print(f"{i} : {set_way[i]}")
                else: 
                    if depth > 10**2:
                        raise OverStackException("setting.json file structure got Overstacked.")
                    print(f"{i}:")
                    cell(set_way[i],depth + 1)
        cell()
    
    def setSettings(self):
        pass

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
        if setting.SETTINGS["user_info"]["isdefault"] == True:
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