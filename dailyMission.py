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
    botStatesObj.logger.info("charctor:%s-> start guildDono" %botStatesObj.statesConfig["currentCharacter"] )
    #打卡工会界面
    realManSim.manSimMultiKey("alt","u") 
    time.sleep(2)
    ok = pyautogui.locateCenterOnScreen(
        "res/pic/ok.bmp", region=botStatesObj.UiRegions["center"], confidence=0.75
    )
    if ok != None:
        x, y = ok
        realManSim.manSimMoveAndLeftClick(x=x, y=y)

    time.sleep(2)
    
    #点击公会捐赠
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["donoTap"][0],botStatesObj.UiCoordi["donoTap"][1])
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["guildDono"][0],botStatesObj.UiCoordi["guildDono"][1])
    realManSim.manSimMoveAndLeftClick(botStatesObj.UiCoordi["donoSilver"][0],botStatesObj.UiCoordi["donoSilver"][1])
    realManSim.manSimPressKey("esc")  # 退出捐赠
    time.sleep(2)
    
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

    time.sleep(2)
    realManSim.manSimPressKey("esc")  # 退出捐赠
    time.sleep(2)
    botStatesObj.logger.info("charctor:%s-> finish guildDono" %botStatesObj.statesConfig["currentCharacter"] )
    
#接受日常
def acceptLopangDaily(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> accept Lopang Daily tasks" %botStatesObj.statesConfig["currentCharacter"] )
    #打开日常任务界面
    realManSim.manSimMultiKey("alt","j") 
    
    #检查是否在收藏夹标签
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","favoritesTaskLists.bmp")
    if re==None:
        #切换至收藏夹标签
        re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","allTaskLists.bmp")
        x,y = re
        realManSim.manSimMoveAndLeftClick(x, y)
        re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","favoritesTaskListsInTab.bmp")
        x,y = re
        realManSim.manSimMoveAndLeftClick(x, y)
        time.sleep(2)
    
    #判断角色是否已经完成日常
    re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskStatuePanel","taskCompleted.bmp")
    if re != None:
        #角色已经完成了，直接跳过
        botStatesObj.logger.info("charctor[%s]-> already finished Lopang Daily tasks, skip" %botStatesObj.statesConfig["currentCharacter"] )
        return False
    else:
        #接受日常1
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskARTY.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.statesConfig["currentCharacter"] )
            return False
        #接受日常2
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskBL.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.statesConfig["currentCharacter"] )
            return False
        #接受日常3
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskXSR.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.statesConfig["currentCharacter"] )
            return False

        botStatesObj.logger.info("charctor:%s-> accept Lopang Daily tasks success :)" %botStatesObj.statesConfig["currentCharacter"] )
        realManSim.manSimPressKey("esc")  # 退出任务界面
        return True


#执行lopang快递任务
def doLopang(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> start Lopang express" %botStatesObj.statesConfig["currentCharacter"] )
    realManSim.sleep(1000, 2000)
    re = acceptLopangDaily(botStatesObj)
    realManSim.sleep(1000, 2000)
    
    #已经送过快递
    if not re:
        realManSim.manSimPressKey("ESC")
        return False
    
    #传送lopang
    botStatesObj.logger.info("charctor:%s-> bifrost Go To lopang island" %botStatesObj.statesConfig["currentCharacter"] )
    re = botStatesObj.amapObj.bifrostGoTo("loPang_Bifrost.bmp")
    if not re:
        return False
    #位于lopang岛，开始接快递
    realManSim.manSimPressKey("G")
    botStatesObj.lopangMoveObj.runToStartPoint()
    botStatesObj.lopangMoveObj.runToBenongTerminal()
    realManSim.manSimPressKey("G")
    botStatesObj.lopangMoveObj.runToARTYTerminal()
    realManSim.manSimPressKey("G")
    
    re = botStatesObj.amapObj.bifrostGoTo("XSR_Bifrost.bmp")
    if not re:
       return False
    realManSim.manSimPressKey("G")
    time.sleep(2)
    realManSim.manSimMultiKey("shift","G") 
    time.sleep(2)
    realManSim.manSimPressKey("G")
    realManSim.manSimPressKey("G")
    time.sleep(2)
    
    # 班船旅行至阿尔泰因
    re = botStatesObj.amapObj.linerGoTo("harbor_ARTY.bmp")
    if not re:
        return False
        
    # ARTY开始上马
    realManSim.manSimPressKey("F1")
    time.sleep(3)
    botStatesObj.lopangMoveObj.runToBakadi()
    realManSim.manSimPressKey("G")
    time.sleep(2)
    realManSim.manSimMultiKey("shift","G") 
    time.sleep(2)
    realManSim.manSimPressKey("G")
    realManSim.manSimPressKey("G")
    time.sleep(2)    
    
    # 班船旅行至贝隆
    re = botStatesObj.amapObj.linerGoTo("harbor_benong.bmp")
    if not re:
        return False
    
    botStatesObj.lopangMoveObj.runToTayerna()
    realManSim.manSimPressKey("G")
    time.sleep(2)
    realManSim.manSimMultiKey("shift","G") 
    time.sleep(2)
    realManSim.manSimPressKey("G")
    realManSim.manSimPressKey("G")
    time.sleep(2)       
    
    # 快递任结束 
    botStatesObj.logger.info("charctor:%s-> Lopang express completed success ..." %botStatesObj.statesConfig["currentCharacter"] )
    
    
    

#开始日常
def startDaily(guildDonoEnable, lopangEnable):
    botStatesObj = botStates.botStates()
    botStatesObj.initBot()
    
    # save bot start time
    botStatesObj.statesConfig["botStartTime"] = int(time.time_ns() / 1000000)
    botStatesObj.logger.info("avator start daily task")
    
    x,y = botStatesObj.UiCoordi["screenCenter"]
    realManSim.manSimMoveAndLeftClick(x,y)
    # change to character 0
    re = botStatesObj.isCharc0Check()
    if not re:
        botStatesObj.switchCharacterTo(0)
    
    # start bot run daily
    while True:
        if botStatesObj.statesConfig["multiCharacterMode"]:        
            curChar = "charc"+str(botStatesObj.statesConfig["currentCharacter"])
            
            # guild dono
            if botStatesObj.Characters[curChar]["guildDonation"] and guildDonoEnable:
                doGuildDonation(botStatesObj)
            # luopang daily
            if botStatesObj.Characters[curChar]["lopang"] and lopangEnable:
                doLopang(botStatesObj)
                
            botStatesObj.statesConfig["finishedCharacter"] = botStatesObj.statesConfig["finishedCharacter"]+1
            
            # 多角色模式
            if botStatesObj.statesConfig["finishedCharacter"] < botStatesObj.statesConfig["numberOfCharacters"]:
                #继续执行剩余角色               
                #切换至下个角色
                botStatesObj.statesConfig["currentCharacter"] = botStatesObj.statesConfig["currentCharacter"]+1
                botStatesObj.switchCharacterTo(botStatesObj.statesConfig["currentCharacter"])
            else:
                #退出
                botStatesObj.logger.info("All character guild dono finished ")
                break

    botStatesObj.logger.info("All daily task finished ")            

if __name__ == "__main__":
    guildDonoEnable = True
    lopangEnable = True
    startDaily(guildDonoEnable, lopangEnable)


#debug
    # botStatesObj = botStates.botStates()
    # botStatesObj.initBot()
    
    # acceptLopangDaily(botStatesObj)
    # doGuildDonation(botStatesObj)
    
    # doLopang(botStatesObj)

