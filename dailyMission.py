import sys
sys.path.append(".") #相对路径或绝对路径
import conf
from core import botStates
import lib
import db
import time
import pyautogui
from core import realManSim
from core.chaosDungeon import chaosDungeon

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

    time.sleep(2)
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
    botStatesObj.basicUiCtrlObj.cleanUi()
    
    botStatesObj.logger.info("charctor:%s-> accept Lopang Daily tasks" %botStatesObj.statesConfig["currentCharacter"] )
    #打开日常任务界面
    realManSim.manSimMultiKey("alt","j") 
    
    #点击每日委托标签
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","dailyTaskTab.bmp")  
    if re!=None:
        x,y=re
        realManSim.manSimMoveAndLeftClick(x, y)
    
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
        botStatesObj.basicUiCtrlObj.cleanUi()
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
            botStatesObj.basicUiCtrlObj.cleanUi()
            return False
        #接受日常2
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskBL.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.statesConfig["currentCharacter"] )
            botStatesObj.basicUiCtrlObj.cleanUi()
            return False
        #接受日常3
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskXSR.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find lopang task" %botStatesObj.statesConfig["currentCharacter"] )
            botStatesObj.basicUiCtrlObj.cleanUi()
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

def rapportPlayMusic(botStatesObj):
    #演奏音乐
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","playMusic.bmp")
    if re == None:
        print("表现情感次数用完")
        realManSim.manSimPressKey("esc")
        return False
    x,y = re
    realManSim.manSimMoveAndLeftClick(x, y)
    time.sleep(1)
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","rapportTimesOver.bmp")
    if re != None:
        print("演奏音乐次数用完")
        realManSim.manSimPressKey("esc")
        return False
    
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","allowPlayMusic.bmp")
    if re != None:
        x,y = re
        realManSim.manSimMoveAndLeftClick(x, y)
        x,y = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","startPlayMusic.bmp")
        realManSim.manSimMoveAndLeftClick(x, y)
        time.sleep(15)  
        return True
    else:
        return False

def rapportShowEmoji(botStatesObj):
    #表现情感
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","showEmoji.bmp")
    if re == None:
        print("表现情感次数用完")
        realManSim.manSimPressKey("esc")
        return False
    x,y = re
    realManSim.manSimMoveAndLeftClick(x, y)
    time.sleep(1)
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","rapportTimesOver.bmp")
    if re != None:
        print("表现情感次数用完")
        realManSim.manSimPressKey("esc")
        return False
    
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","allowShowEmoji.bmp")
    if re != None:
        x,y = re
        x = int(x)
        y = int(y)
        color = pyautogui.pixel(x, y) #获取指定位置的色值
        print('色值{}'.format(color))
        matchColor = pyautogui.pixelMatchesColor(x, y, (162, 210, 224), tolerance=10) #检测指定位置是否指定颜色 误差范围3
        # print('色值是否匹配{}'.format(matchColor))
        if matchColor:
            realManSim.manSimMoveAndLeftClick(x, y)
            x,y = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","startShowEmoji.bmp")
            realManSim.manSimMoveAndLeftClick(x, y)
            time.sleep(15) 
            return True
        else:
            return False

#好感度日常
def doRapport(botStatesObj):   

    #npc 000
    re = botStatesObj.amapObj.bifrostRemarksGoTo("rapportNPC000.bmp")
    if re:
        realManSim.manSimPressKey("G")
        time.sleep(1)
        #演奏音乐
        if botStatesObj.statesConfig["doneMusicTimes"]<6:
            re = rapportPlayMusic(botStatesObj)
            if re:
                botStatesObj.statesConfig["doneMusicTimes"] = botStatesObj.statesConfig["doneMusicTimes"]+1
        else:
            botStatesObj.logger.info("all rapper MusicTimes times done!")
            
        if botStatesObj.statesConfig["doneMusicTimes"]<6:
            re = rapportPlayMusic(botStatesObj)
            if re:
                botStatesObj.statesConfig["doneMusicTimes"] = botStatesObj.statesConfig["doneMusicTimes"]+1
        else:
            botStatesObj.logger.info("all rapper MusicTimes times done!")
            
        #表现情感
        if botStatesObj.statesConfig["doneMusicTimes"]<6:
            re = rapportShowEmoji(botStatesObj) 
            if re:
                botStatesObj.statesConfig["doneEmojiTimes"] = botStatesObj.statesConfig["doneMusicTimes"]+1
            else:
                botStatesObj.logger.info("all rapper emoji times done!")
                
        if botStatesObj.statesConfig["doneMusicTimes"]<6:
            re = rapportShowEmoji(botStatesObj) 
            if re:
                botStatesObj.statesConfig["doneEmojiTimes"] = botStatesObj.statesConfig["doneMusicTimes"]+1
            else:
                botStatesObj.logger.info("all rapper emoji times done!")                
        botStatesObj.basicUiCtrlObj.cleanUi()    
        
    #npc 111 
    re = botStatesObj.amapObj.bifrostRemarksGoTo("rapportNPC111.bmp")
    if re:
        realManSim.manSimPressKey("G")
        time.sleep(1)
        #演奏音乐
        rapportPlayMusic(botStatesObj)
        rapportPlayMusic(botStatesObj)    
        #表现情感
        rapportShowEmoji(botStatesObj) 
        rapportShowEmoji(botStatesObj) 
        botStatesObj.basicUiCtrlObj.cleanUi()

    #npc 222
    re = botStatesObj.amapObj.bifrostRemarksGoTo("rapportNPC222.bmp")
    if re:
        realManSim.manSimPressKey("G")
        time.sleep(1)
        #演奏音乐
        rapportPlayMusic(botStatesObj)
        rapportPlayMusic(botStatesObj)    
        #表现情感
        rapportShowEmoji(botStatesObj) 
        rapportShowEmoji(botStatesObj) 
        botStatesObj.basicUiCtrlObj.cleanUi()    
    

def acceptBreakStoneDaily(botStatesObj):
    botStatesObj.basicUiCtrlObj.cleanUi()
    botStatesObj.logger.info("charctor:%s-> accept BreakStone Daily tasks" %botStatesObj.statesConfig["currentCharacter"] )
    #打开日常任务界面
    time.sleep(2)
    realManSim.manSimMultiKey("alt","j")           
    #点击每日委托标签
    re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","dailyTaskTab.bmp")  
    if re!=None:
        x,y=re
        realManSim.manSimMoveAndLeftClick(x, y)
    
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
        botStatesObj.logger.info("charctor[%s]-> already finished BreakStone Daily tasks, skip" %botStatesObj.statesConfig["currentCharacter"] )
        botStatesObj.basicUiCtrlObj.cleanUi()
        return False
    else:
        #接受解放奴隶任务并直接点击完成
        # re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskFreeSlaves.bmp")
        # if re != None:
        #     x,y = re
        #     x = x+832
        #     realManSim.manSimMoveAndLeftClick(x, y)
        #     time.sleep(1)
        #     #点击完成
        #     realManSim.manSimMoveAndLeftClick(x, y)
        #     time.sleep(1)
            
        #     botStatesObj.basicUiCtrlObj.clickOkButton()
        # else:
        #     botStatesObj.logger.error("charctor[%s]-> didn't find BreakStone task" %botStatesObj.statesConfig["currentCharacter"] )
        #     botStatesObj.basicUiCtrlObj.cleanUi()
        #     return False
        #接受日常2
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskWatchman.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find BreakStone task" %botStatesObj.statesConfig["currentCharacter"] )
            botStatesObj.basicUiCtrlObj.cleanUi()
            return False
        #接受日常3
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskPanel","taskDestinyEye.bmp")
        if re != None:
            x,y = re
            x = x+832
            realManSim.manSimMoveAndLeftClick(x, y)
        else:
            botStatesObj.logger.error("charctor[%s]-> didn't find BreakStone task" %botStatesObj.statesConfig["currentCharacter"] )
            botStatesObj.basicUiCtrlObj.cleanUi()
            return False

        botStatesObj.logger.info("charctor:%s-> accept BreakStone Daily tasks success :)" %botStatesObj.statesConfig["currentCharacter"] )
        realManSim.manSimPressKey("esc")  # 退出任务界面
        return True    

#执行突破石日常石    
def doBreakStoneDaily(botStatesObj):
    botStatesObj.logger.info("charctor:%s-> start BreakStone tasks" %botStatesObj.statesConfig["currentCharacter"] )
    realManSim.sleep(1000, 2000)
    re = acceptBreakStoneDaily(botStatesObj)
    realManSim.sleep(1000, 2000)    
    
    #任务接收失败
    if not re:
        botStatesObj.basicUiCtrlObj.cleanUi()
        return False
    
    #传送费顿——守望者任务
    botStatesObj.logger.info("charctor:%s-> bifrost Go To 费顿" %botStatesObj.statesConfig["currentCharacter"] )
    re = botStatesObj.amapObj.bifrostGoTo("feidun_Bifrost.bmp")
    if not re:
        return False


    watchColorLow=[70,9,255] #守望者触角颜色m
    watchColorUp =[110,255,255] #守望者触角颜色m
    
    outline=[50,50] #轮廓大小
    
    while(1):
        re = botStatesObj.colorScan(watchColorLow,watchColorUp,outline)
        
        startTime = time.time()
        botStatesObj.logger.info("charctor:%s-> 扫描守望者" %botStatesObj.statesConfig["currentCharacter"] )
        if re!=None:
            #找到守望者了
            botStatesObj.logger.info("charctor:%s-> 找到守望者" %botStatesObj.statesConfig["currentCharacter"] )
            x,y=re
            realManSim.manSimMoveTo(x,y)
            realManSim.manSimPressKey("F5")
            startTime = time.time()
            time.sleep(2)
            re=botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskWatchmanFinished.bmp")
            if re!=None:
                x,y = re
                taskJudgeRegion = [x-89,y-14,21,26]
                pic = "taskFinishedMark.bmp"
                re = pyautogui.locateCenterOnScreen(
                    botStatesObj.picPath+pic,
                    confidence=0.8,
                    region=taskJudgeRegion,
                )
                if re!=None:
                    botStatesObj.logger.info("charctor:%s-> 守望者任务完成" %botStatesObj.statesConfig["currentCharacter"] )
                    break
        else:
            curTime = time.time()
            if curTime-startTime>120:
                botStatesObj.logger.error("stack in game loading stage, bot exist")
                exit()
        
    # 纪念仪式任务

    # 传送至黑森林
    botStatesObj.logger.info("charctor:%s-> bifrost Go To 费顿" %botStatesObj.statesConfig["currentCharacter"] )
    re = botStatesObj.amapObj.bifrostGoTo("feidun_BifrostDestiTask.bmp")
    if not re:
        return False
   
    re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskDestinyEyeFinished.bmp")
    x,y = re
    x = x-77
    y = y+59
    custRegion = [x,y,35,40]
    startTime = time.time()
    while (1):
        realManSim.manSimPressKey("G")
        time.sleep(5)
        re = botStatesObj.basicUiCtrlObj.botPicCustomCheck(custRegion,"taskDestinyEyeStatus_stage1Finished.bmp")
        if re==None:
            #被打断，尝试攻击
            botStatesObj.chaosCombatObj.enemyDirect = botStatesObj.UiCoordi["screenCenter"]
            botStatesObj.chaosCombatObj.enemyDirect[0] = botStatesObj.chaosCombatObj.enemyDirect[0]-200
            botStatesObj.chaosCombatObj.enemyDirect[1] = botStatesObj.chaosCombatObj.enemyDirect[1]-200  
            botStatesObj.chaosCombatObj.castSkill("S")
            botStatesObj.chaosCombatObj.castSkill("F")
            botStatesObj.chaosCombatObj.castSkill("W")
            time.sleep(3)
            curTime = time.time()
            if curTime-startTime>50:
                botStatesObj.logger.error("stack in 金塞拉任务 阶段1, bot exist")
                exit()
        else:
            #拾取成功
            botStatesObj.logger.info("charctor:%s-> taskDestinyEyeStatus_stage1 Finished" %botStatesObj.statesConfig["currentCharacter"] )
            break
        

    realManSim.manSimPressKey("F1")
    time.sleep(3)
    botStatesObj.feidunMoveObj.runToblackForesetToSecondPoint()
    time.sleep(3)
    realManSim.manSimPressKey("R")
    re=botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskDestinyEyeFinished.bmp")
    x,y = re
    custRegion = [x-89,y-14,34,26]
    startTime = time.time()
    while (1):
        realManSim.manSimPressKey("G")
        time.sleep(5)
        re = botStatesObj.basicUiCtrlObj.botPicCustomCheck(custRegion,"taskFinishedMark.bmp")
        if re==None:
            #被打断，尝试攻击
            botStatesObj.chaosCombatObj.enemyDirect = botStatesObj.UiCoordi["screenCenter"]
            botStatesObj.chaosCombatObj.enemyDirect[0] = botStatesObj.chaosCombatObj.enemyDirect[0]-200
            botStatesObj.chaosCombatObj.enemyDirect[1] = botStatesObj.chaosCombatObj.enemyDirect[1]-100  
            botStatesObj.chaosCombatObj.castSkill("S")
            botStatesObj.chaosCombatObj.castSkill("F")
            botStatesObj.chaosCombatObj.castSkill("W")
            time.sleep(3)
            curTime = time.time()
            if curTime-startTime>50:
                botStatesObj.logger.error("stack in 金塞拉任务 阶段2 bot exist")
                exit()
        else:
            #拾取成功
            botStatesObj.logger.info("charctor:%s-> 金塞拉任务完成" %botStatesObj.statesConfig["currentCharacter"] )
            break
    
    while(1):   
        re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskDestinyEyeStatus.bmp")
        if re != None:
            x, y = re
            x = x+187
            realManSim.manSimMoveAndLeftClick(x, y)
            time.sleep(1)
            re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","blackHawkHotel.bmp")
            if re != None:
                x, y = re
                x = x
                realManSim.manSimMoveAndLeftClick(x, y)
                time.sleep(1)
                botStatesObj.basicUiCtrlObj.clickOkButton()
                time.sleep(3)
                re = botStatesObj.basicUiCtrlObj.waitGameLoding()
                if re:
                    #传送成功
                    break
                else:
                    botStatesObj.chaosCombatObj.castSkill("S")
                    botStatesObj.chaosCombatObj.castSkill("F")
                    botStatesObj.chaosCombatObj.castSkill("W")
                    print("被打打断")
            else:
                return False
            
    realManSim.manSimPressKey("F1")
    time.sleep(3)
    botStatesObj.feidunMoveObj.runToblackHawkHotelToFirstPoint()
    botStatesObj.feidunMoveObj.runToFirstCheckPoint()
    botStatesObj.feidunMoveObj.runToblackHawkHotelToSecondPoint()
    #提交任务
    botStatesObj.basicUiCtrlObj.finishTaskAcptRewards()
    #去往下个npc
    botStatesObj.feidunMoveObj.runToblackHawkHotelToThirdPoint()
    #提交任务
    botStatesObj.basicUiCtrlObj.finishTaskAcptRewards()
    botStatesObj.logger.info("charctor:%s-> BreakStone Daily tasks finished ! :)" %botStatesObj.statesConfig["currentCharacter"] )

#开始地牢日常
def doChaosDaily(botStatesObj):
    chaosDungeonObj = chaosDungeon()
    chaosDungeonObj.initChaosDungeon(botStatesObj)
    chaosDungeonObj.checkReloadSkill()
    chaosDungeonObj.doChaos_matchMode()
    chaosDungeonObj.doChaos_matchMode()
    

#开始所有日常
def startDaily(startRole):
    botStatesObj = botStates.botStates()
    botStatesObj.initBot()
    
    # save bot start time
    botStatesObj.statesConfig["botStartTime"] = int(time.time_ns() / 1000000)
    botStatesObj.logger.info("avator start daily task")
    
    x,y = botStatesObj.UiCoordi["screenCenter"]
    realManSim.manSimMoveAndLeftClick(x,y)
    # change to character 0
    # re = botStatesObj.isCharc0Check()
    # if not re:
    #     botStatesObj.switchCharacterTo(0)
    botStatesObj.statesConfig["currentCharacter"] = startRole
    botStatesObj.switchCharacterTo(botStatesObj.statesConfig["currentCharacter"])
    botStatesObj.statesConfig["finishedCharacter"] = startRole
    # start bot run daily
    while True:

        if botStatesObj.statesConfig["multiCharacterMode"] and botStatesObj.statesConfig["enableMultiCharacterMode"]:        
            # 多角色模式
            curChar = "charc"+str(botStatesObj.statesConfig["currentCharacter"])
            
            # guild dono
            if botStatesObj.Characters[curChar]["guildDonation"] and botStatesObj.statesConfig["enableGuildDonation"]:
                doGuildDonation(botStatesObj)
            # luopang daily
            if botStatesObj.Characters[curChar]["lopang"] and botStatesObj.statesConfig["enableLopang"]:
                doLopang(botStatesObj)
            # rapport
            if botStatesObj.Characters[curChar]["rapport"] and botStatesObj.statesConfig["enableRapport"]:
                doRapport(botStatesObj)          
            #breakStone
            if botStatesObj.Characters[curChar]["breakStone"] and botStatesObj.statesConfig["enableBreakStone"]:
                doBreakStoneDaily(botStatesObj)

            if botStatesObj.Characters[curChar]["chaos"] and botStatesObj.statesConfig["enableChaos"]:
                doChaosDaily(botStatesObj)                
            
                
            botStatesObj.statesConfig["finishedCharacter"] = botStatesObj.statesConfig["finishedCharacter"]+1
            
            if botStatesObj.statesConfig["finishedCharacter"] < botStatesObj.statesConfig["numberOfCharacters"]:
                #继续执行剩余角色               
                #切换至下个角色
                botStatesObj.statesConfig["currentCharacter"] = botStatesObj.statesConfig["currentCharacter"]+1
                botStatesObj.switchCharacterTo(botStatesObj.statesConfig["currentCharacter"])
            else:
                #退出
                botStatesObj.logger.info("All character dailiy tasks finished ")
                break
        else:
            #单角色
            curChar = "charc"+str(botStatesObj.statesConfig["currentCharacter"])
            
            # guild dono
            if botStatesObj.Characters[curChar]["guildDonation"] and botStatesObj.statesConfig["enableGuildDonation"]:
                doGuildDonation(botStatesObj)
            # luopang daily
            if botStatesObj.Characters[curChar]["lopang"] and botStatesObj.statesConfig["enableLopang"]:
                doLopang(botStatesObj)
            # rapport
            if botStatesObj.Characters[curChar]["rapport"] and botStatesObj.statesConfig["enableRapport"]:
                doRapport(botStatesObj)            
            
            
            #退出
            botStatesObj.logger.info("Current character dailiy tasks finished ")
            break    

    botStatesObj.logger.info("All daily task finished ")            

if __name__ == "__main__":
    startRole = 3
    startDaily(startRole)


#debug
    # botStatesObj = botStates.botStates()
    # botStatesObj.initBot()
    # acceptBreakStoneDaily(botStatesObj)
    # doRapport(botStatesObj)
    
    # rapportPlayMusic(botStatesObj)
    # acceptLopangDaily(botStatesObj)
    # doGuildDonation(botStatesObj)
    # realManSim.manSimPressKey("G")
    # time.sleep(1)
    # rapportShowEmoji(botStatesObj) 
    # doLopang(botStatesObj)
    #纪念仪式任务   
    # botStatesObj.chaosCombatObj.saveSkillBarNoCDImage()
    # botStatesObj.chaosCombatObj.loadSkill(botStatesObj.skill_Wardancer)
    # doBreakStoneDaily(botStatesObj)





    # 传送至黑森林
    # re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskDestinyEyeStatus.bmp")
    # if re != None:
    #     x, y = re
    #     x = x+187
    #     realManSim.manSimMoveAndLeftClick(x, y)
    #     time.sleep(1)
    #     re = botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","blackForestTransport.bmp")
    #     if re != None:
    #         x, y = re
    #         x = x-27
    #         realManSim.manSimMoveAndLeftClick(x, y)
    #         time.sleep(1)
    #         botStatesObj.basicUiCtrlObj.clickOkButton()
    #         time.sleep(3)
    #         botStatesObj.basicUiCtrlObj.waitGameLoding()
    #     else:
    #         return False