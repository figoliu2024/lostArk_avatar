import sys
sys.path.append(".") #相对路径或绝对路径
import conf
from core import botStates
import lib
import db
import time
import pyautogui
from core import realManSim


def doGuildDonation(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> start guildDono" %botStatesObj.states["currentCharacter"] )
    #打卡工会界面
    realManSim.manSimMultiKey("alt","u") 
    ok = pyautogui.locateCenterOnScreen(
        "res/pic/ok.bmp", region=botStatesObj.UiRegions["center"], confidence=0.75
    )
    if ok != None:
        x, y = ok
        realManSim.manSimMoveAndLeftClick(x=x, y=y)

    time.sleep(1)
    
    #点击公会捐赠
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["donoTap"][0],botStatesObj.UiCoordi["donoTap"][1])
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["guildDono"][0],botStatesObj.UiCoordi["guildDono"][1])
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["donoSilver"][0],botStatesObj.UiCoordi["donoSilver"][1])
    realManSim.manSimPressKey("esc")  # 退出捐赠
    time.sleep(1)
    
    #支援研究
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["researchTap"][0],botStatesObj.UiCoordi["researchTap"][1])

    supportResearch = pyautogui.locateCenterOnScreen(
        "res/pic/supportResearch.bmp",
        confidence=0.8,
        region=botStatesObj.UiRegions["researchCheck"],
    )

    if supportResearch != None:
        x, y = supportResearch
        realManSim.manSimMoveAndLeftClick(x=x, y=y)

        canSupportResearch = pyautogui.locateCenterOnScreen(
            "res/pic/canSupportResearch.bmp",
            confidence=0.8,
            region=botStatesObj.UiRegions["supportResearchCheck"],
        )

        if canSupportResearch != None:
            x, y = canSupportResearch
            realManSim.manSimMoveAndLeftClick(x=x, y=y)
            realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["supportConf"][0],botStatesObj.UiCoordi["supportConf"][1])
        else:
            realManSim.manSimPressKey("esc")  # 退出捐赠
            time.sleep(0.8)

    time.sleep(1)
    realManSim.manSimPressKey("esc")  # 退出捐赠
    time.sleep(1)
    botStatesObj.logger.info("charctor:%s-> finish guildDono" %botStatesObj.states["currentCharacter"] )
    
#接受日常
def acceptLopangDaily(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> accept Lopang Daily tasks" %botStatesObj.states["currentCharacter"] )
    #打开日常任务界面
    realManSim.manSimMultiKey("alt","j") 
    #判断角色是否已经完成日常
    re = botStatesObj.botPicCheck("EvnaTaskStatuePanel","taskCompleted.bmp")
    if re != None:
        #角色已经完成了，直接跳过
        botStatesObj.logger.info("charctor[%s]-> already finished Lopang Daily tasks, skip" %botStatesObj.states["currentCharacter"] )
        return False
    else:
        #接受日常1
        re = botStatesObj.botPicCheck("EvnaTaskPanel","taskARTY.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.states["currentCharacter"] )
            return False
        #接受日常2
        re = botStatesObj.botPicCheck("EvnaTaskPanel","taskBL.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.states["currentCharacter"] )
            return False
        #接受日常3
        re = botStatesObj.botPicCheck("EvnaTaskPanel","taskXSR.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.states["currentCharacter"] )
            return False

        botStatesObj.logger.info("charctor:%s-> accept Lopang Daily tasks success :)" %botStatesObj.states["currentCharacter"] )
        realManSim.manSimPressKey("esc")  # 退出任务界面
        return True


#执行lopang快递任务
def doLopang(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> start Lopang express" %botStatesObj.states["currentCharacter"] )
    realManSim.sleep(1000, 2000)
    acceptLopangDaily(botStatesObj)
    realManSim.sleep(1000, 2000)
    botStatesObj.logger.info("charctor:%s-> bifrost Go To lopang island" %botStatesObj.states["currentCharacter"] )
    re = botStatesObj.bifrostGoTo("loPang_Bifrost.bmp")
    if not re:
        return False
    
    #位于lopang岛，开始接快递
    realManSim.manSimPressKey("G")
    
    
    
    

#开始日常
def startDaily():
    botStatesObj = botStates.botStates()
    botStatesObj.initBot()
    
    # save bot start time
    botStatesObj.states["botStartTime"] = int(time.time_ns() / 1000000)
    botStatesObj.logger.info("avator start daily task")
    
    x,y = botStatesObj.UiCoordi["screenCenter"]
    realManSim.manSimMoveAndLeftClick(x,y)
    # change to character 0
    re = botStatesObj.isCharc0Check()
    if not re:
        botStatesObj.switchCharacterTo(0)
    
    # start bot run daily
    while True:
        if botStatesObj.states["multiCharacterMode"]:        
            curChar = "charc"+str(botStatesObj.states["currentCharacter"])
            # guild dono
            if botStatesObj.Characters[curChar]["guildDonation"]:
                doGuildDonation(botStatesObj)
                botStatesObj.states["finishedCharacter"] = botStatesObj.states["finishedCharacter"]+1
            # luopang daily
            #多角色模式
            if botStatesObj.states["finishedCharacter"] < botStatesObj.states["numberOfCharacters"]:
                #继续执行剩余角色               
                #切换至下个角色
                botStatesObj.states["currentCharacter"] = botStatesObj.states["currentCharacter"]+1
                botStatesObj.switchCharacterTo(botStatesObj.states["currentCharacter"])
            else:
                #退出
                botStatesObj.logger.info("All character guild dono finished ")
                break

    botStatesObj.logger.info("All daily task finished ")            

if __name__ == "__main__":

    startDaily()


#debug
    # botStatesObj = botStates.botStates()
    # botStatesObj.initBot()
    
    # acceptLopangDaily(botStatesObj)
    # doGuildDonation(botStatesObj)
    
    # doLopang(botStatesObj)

