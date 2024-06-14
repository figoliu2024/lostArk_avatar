import sys
sys.path.append(".") #相对路径或绝对路径

import numpy
import pyautogui
import cv2
import time
import random
# import yaml
from PIL import Image
import core.aStarFigo as aStarFigo
from core import realManSim
from core import botStates as botPy
from lib import libMathFigo
from core import basicUiControl as BUCPy
from core import botStates
from conf import skillLists

class chaosDungeon(object):
   
    
    targetColor=[180,116,200]   #小地图上小怪颜色
    destSliceColorLow=[0,0,220]  #小地图上命运片段颜色
    destSliceColorUp =[20,18,255]
    bossColor = [1,52,175]      #小地图上boss颜色
    destSliceOutline=[1,1] #小地图怪框大小门限
    
    
    teamHpColorLow = [85,180,160]
    teamHpColorUp  = [95,255,200]
    teamHpOutline  = [30,2]
    
    teamColorLow = [100,80,150]
    teamColorUp = [109,200,255]
    teamOutline = [4,4]
    
    chaosTowerColorLow= [170,76,190]
    chaosTowerColorUp = [190,200,255]
    chaosTowerOutline = [2,2]
    
    redHpColor =[61,5,0] #屏幕上的血条颜色
    curClass = [] #当前职业
    
    usedpPotions = 0 #已使用的血瓶数量
    
    def __init__(self) -> None:
        '''
        初始化一些数据结构：堆、集合帮助实现算法
        '''
        
    def initChaosDungeon(self,botStatesObj):
        '''
        chaosDungeon对象初始化
        '''        
        print ("initiation chaosCombat")
        self.botStatesObj = botStatesObj
        # self.basicUiCtrlObj = basicUiCtrlObj
        # self.botStatesObj.chaosCombatObj = chaosCombatObj
        # self.UiCoordi = UiCoordi


    def enterChaosDugeonIn_matchMode(self):
        '''
        匹配进入 chaosDungeon
        '''     
        realManSim.manSimMultiKey("alt","q")
        time.sleep(1)
        re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","playIndexRecomm.bmp")
        time.sleep(1)
        re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","dungenEntrance.png")
        if not re:
            return False
        
        re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","gotoCatalog.bmp")
        if not re:
            return False
        
        re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","applyForMatch.bmp")
        if not re:
            return False
        
        #检查是否还有进入次数
        time.sleep(1)
        re = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","noChaosEnterTimes.bmp")
        if re!=None:
            print("地牢次数用完，退出脚本")
            return False
        
        startTime = time.time()
        while(1):
            #等待匹配进入
            re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","agreeToEnterIn.bmp")
            if re:
                print("点击进入游戏")
                time.sleep(1)
                re = self.botStatesObj.basicUiCtrlObj.botPicCheck("inTownCheck","inTown.bmp")
                if re==None:
                    break
            else:
                curTime = time.time()
                if curTime-startTime>300:
                    print("stack in game match, bot exist")
                    exit()
        
        # #等待游戏进入chaosDugeon
        self.botStatesObj.basicUiCtrlObj.waitBlackGameLoding()
        
        #检查是否在地牢
        time.sleep(2)
        re = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","inChaosCheck.bmp")
        if re==None:
            print("进入地下城失败")
            return False
        else:
            print("进入地下城成功！")
            return True
    
    def checkDeath(self):
        '''
        检查死亡，并且点击复活
        '''    
        re = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","roleDeath.bmp")
        if re!=None:
            print("角色死亡，等待5s点击复活!")
            time.sleep(5)
            re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","roleDeath.bmp")
            time.sleep(5)
            
    
    def checkAndPickDestinySlice(self):
        '''
        检查命运片段，并移动过去拾取
        '''    
        locations = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","destinySlice.bmp")
        if locations != None:
            x,y = locations
            realManSim.manSimMoveAndRightClick(x,y)
            time.sleep(2)
            realManSim.manSimPressKey("G")
        # else:
            # loc = botStatesObj.minimapColorScan(self.destSliceColorLow,self.destSliceColorUp,self.destSliceOutline)
            # if loc !=None:
            #     (tarX,tarY) = self.botStatesObj.basicUiCtrlObj.miniMapTargetCal(loc)
            #     realManSim.manSimMoveAndRightClick(tarX,tarY)
            #     time.sleep(2)
            #     realManSim.manSimPressKey("G")
                
        #没事就按
        # realManSim.manSimPressKey("G")
        # time.sleep(0.1)
    
    def checkMoveToNextFloor(self):
        '''
        组队状态，检查是否移动至下一个空间
        '''           
        locations = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","chaosMoveToNextFloor.bmp")
        if locations != None:
            self.botStatesObj.basicUiCtrlObj.clickAgreeButton()
            re = self.botStatesObj.basicUiCtrlObj.waitBlackGameLoding()
            if not re:
                # exit()
                re = self.botPicCheck("inTownCheck","inTown.bmp")
                if re!=None:
                    self.logger.info("game loading finished")
                    time.sleep(1)
            return True
        
        return False
    
    def checkChaosFinished(self):
        '''
        组队状态，检查是否地牢结束
        '''           
        locations = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","chaosFinishedConfirm.bmp")
        if locations != None:
            x,y =locations
            time.sleep(1)
            realManSim.manSimMoveAndLeftClick(x,y)
            time.sleep(5)
            realManSim.manSimPressKey("ESC")
            time.sleep(1)
            self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("chaosStateRegion","defolderChaosStates.bmp")
            time.sleep(1)
            self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("chaosStateRegion","chaosQuit.bmp")
            time.sleep(1)
            self.botStatesObj.basicUiCtrlObj.clickOkButton()
            re = self.botStatesObj.basicUiCtrlObj.waitBlackGameLoding()
            if not re:
                exit()
            return True
        
        return False
    
    
    def doBossAttack(self):
        '''
        检查到boss出现，开始执行boss阶段
        '''   
        #先放大招
        
        
        locations = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","chaosMoveToNextFloor.bmp")
        if locations != None:
            print("开始boss战")
            self.botStatesObj.chaosCombatObj.castSkill("V")
            while(1):
                #检查boss是否还在
                locations = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen","chaosMoveToNextFloor.bmp")
                if locations != None:
                    #尝试定位boss位置
                    
                    #无脑攻击
                    self.botStatesObj.chaosCombatObj.comboListCast()
                else:
                    print("boss被消灭")
                    break
    
    def randomMove(self):
        '''
        随机小范围移动下
        '''   
        x = self.botStatesObj.UiCoordi["screenCenter"][0]+random.randint(-10, 10)
        y = self.botStatesObj.UiCoordi["screenCenter"][1]+random.randint(-8, 8)
        realManSim.manSimMoveAndRightClick(x,y)
    
    
    def moveToTeam(self):
        '''
        屏幕上找蓝色队友血条并靠近
        '''    
        re = self.botStatesObj.colorScan(self.teamHpColorLow,self.teamHpColorUp,self.teamHpOutline)
        if re!= None:
            print("朝队友移动")
            (tarX,tarY) = re 
            realManSim.manSimMoveAndRightClick(tarX,tarY)
            time.sleep(1.5)
            
            return re

    def moveToMiniMapTeam(self):
        '''
        小地图上上找蓝色队又并靠近
        '''    
        re = self.botStatesObj.minimapColorScan(self.teamColorLow,self.teamColorUp,self.teamOutline)
        if re!= None:
            print("朝队友移动")
            (tarX,tarY) = self.botStatesObj.basicUiCtrlObj.miniMapTargetCal(re)
            (tarX,tarY) = re 
            realManSim.manSimMoveAndRightClick(tarX,tarY)
            time.sleep(1.5)
            return re
            # self.botStatesObj.chaosCombatObj.enemyDirect = (tarX,tarY)            
    
    def checkHp_drinkPotions(self):
        '''
        小地图上上找蓝色队又并靠近
        '''   
        hp=self.botStatesObj.chaosCombatObj.checkHealHP()
        if self.usedpPotions<10:
            #防止bug导致无限喝水，直接放生
            match hp:
                case "lowHp":
                    realManSim.manSimPressKey("1")
                    print("血量低于30，开始喝大药水")
                    self.usedpPotions = self.usedpPotions+1
                case "midHp":
                    realManSim.manSimPressKey("5")
                    print("血量低于50，开始喝霄药水")
                    self.usedpPotions = self.usedpPotions+1
                case "highHp":
                    print("血量低于80，不干啥")
                case _:
                    print("血量高于80，不干啥")
    
    def doChaosFloor1_matchMode(self):
        '''
        执行第一阶段chaos战斗
        '''    
        self.usedpPotions = 0
        print("开始chaos阶段: floor 1")
        # enemyBarColor_RGB = (237,59,7) #血条颜色
        randCastTime = time.time()
        randMoveTime = time.time()
        self.botStatesObj.chaosCombatObj.enemyDirect = self.botStatesObj.UiCoordi["screenCenter"]
        while(1):
            #检查是否死了
            self.checkDeath()
                    
            ##攻击目标
            self.botStatesObj.chaosCombatObj.comboListCast()
            
            #检查是否掉落率命运片段
            self.checkAndPickDestinySlice()
           
            #检查是否进入下个门
            re = self.checkMoveToNextFloor()
            if re:
                print("进入下个chaos阶段: floor 2")
                break
            
            #定时朝队友移动下
            curTime = time.time()
            if curTime-randMoveTime>4:
                re = self.moveToTeam()
                if re!=None:
                    tarX,tarY = re
                    self.botStatesObj.chaosCombatObj.enemyDirect = (tarX,tarY)
                else:
                    print("屏幕队友血条丢失")
                    re = self.moveToMiniMapTeam()
                    if re!=None:
                        print("小地图找到队友")
                        tarX,tarY = re
                        self.botStatesObj.chaosCombatObj.enemyDirect = (tarX,tarY)
                    
                randMoveTime = time.time()
            
            #定时扔大招或特殊技能
            if curTime-randCastTime>20:
                #检查血量喝血瓶
                self.checkHp_drinkPotions()
                
                
                match self.curClass:
                    case "Wardancer":
                        realManSim.manSimPressKey("F")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")
                    case "Artist":
                        realManSim.manSimPressKey("X")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")
                    case "Arcanist":
                        realManSim.manSimPressKey("Z")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("X")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")
                    case _:
                        print("not support current class")
                randCastTime = time.time()
            
    def doChaosFloor2_matchMode(self):
        '''
        执行第二阶段chaos战斗
        '''    
        print("开始chaos阶段: floor 2")


    def doChaosFloor3_matchMode(self):
        '''
        执行第3阶段chaos战斗
        '''    
        self.usedpPotions = 0
        print("开始chaos阶段: floor 3")
        # enemyBarColor_RGB = (237,59,7) #血条颜色
        randCastTime = time.time()
        randMoveTime = time.time()
        self.botStatesObj.chaosCombatObj.enemyDirect = self.botStatesObj.UiCoordi["screenCenter"]
        role = self.botStatesObj.UiCoordi["screenCenter"]
        while(1):
            #检查tower位置并移动
            re = self.botStatesObj.minimapColorScan(self.chaosTowerColorLow,self.chaosTowerColorUp,self.chaosTowerOutline)
            if re!= None:
                (tarX,tarY) = self.botStatesObj.basicUiCtrlObj.miniMapTargetCal(re)
                distance = libMathFigo.eucliDist((tarX,tarY) ,role)
                if distance > 10:
                    realManSim.manSimMoveAndRightClick(tarX,tarY)
                    time.sleep(1)
            else:
                #优先检查队友位置
                re = self.botStatesObj.colorScan(self.teamHpColorLow,self.teamHpColorUp,self.teamHpOutline)
                if re!=None:
                    distance = libMathFigo.eucliDist(re,role)
                    print(distance)
                    if distance > 200:
                        tarX,tarY = re
                        realManSim.manSimMoveAndRightClick(tarX,tarY)
                        time.sleep(1)
                    else:
                        ##攻击目标
                        self.botStatesObj.chaosCombatObj.comboListCast()
                else:
                    #小地图跟踪队友位置
                    print("队友血条丢失，尝试小地图跟踪")
                    re = self.botStatesObj.minimapColorScan(self.teamColorLow,self.teamColorUp,self.teamOutline)
                    if re!= None:
                        (tarX,tarY) = self.botStatesObj.basicUiCtrlObj.miniMapTargetCal(re)
                        distance = libMathFigo.eucliDist((tarX,tarY) ,role)
                        if distance > 100:
                            realManSim.manSimMoveAndRightClick(tarX,tarY)
                            time.sleep(1)
                    else:
                        ##攻击目标
                        self.botStatesObj.chaosCombatObj.comboListCast()

                    
            #检查是否死了
            self.checkDeath()
            
            #检查是否掉落率命运片段
            self.checkAndPickDestinySlice()
            
            #定时扔大招或特殊技能
            curTime = time.time()
            if curTime-randCastTime>10:
                #检查血量喝血瓶
                self.checkHp_drinkPotions()
                match self.curClass:
                    case "Wardancer":
                        realManSim.manSimPressKey("V")
                    case "Artist":
                        realManSim.manSimPressKey("X")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")
                    case "Arcanist":
                        realManSim.manSimPressKey("Z")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("X")
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")                        
                    case _:
                        time.sleep(0.5)
                        realManSim.manSimPressKey("V")     
                        print("not support current class")
                randCastTime = time.time()
           
            #检查是否完成地牢
            re = self.checkChaosFinished()
            if re:
                print("地牢完成，退出")
                break
          

    def doChaos_matchMode(self):
        '''
        执行chaos匹配模式
        '''        
        
        # 1.申请进入chaos
        while (1):
            re = self.enterChaosDugeonIn_matchMode()
            if re:
                break
            else:
                self.botStatesObj.basicUiCtrlObj.cleanUi()
                return False
        
        # 2.执行阶段1
        self.doChaosFloor1_matchMode()
        
        # 3.执行阶段2
        self.doChaosFloor1_matchMode()  
        
        ## 4.执行阶段3
        self.doChaosFloor3_matchMode()  
        
        print("chaos Finished")
        
    def checkReloadSkill(self):
        '''
        检查当前角色职业并加载技能表
        '''   
        realManSim.manSimPressKey("p")
        time.sleep(1)
        re = self.botStatesObj.basicUiCtrlObj.botPicCheckAndClick("fullScreen","equipTab.bmp")
        time.sleep(1)
        for className in self.botStatesObj.statesConfig["supportClass"]:
            pic = className+".bmp"
            loc = self.botStatesObj.basicUiCtrlObj.botPicCheck("fullScreen",pic)
            if loc!=None:
                self.botStatesObj.chaosCombatObj.loadSkill( getattr(skillLists,className))
                self.curClass = className
                print("当前职业是：【%s】" % className)
                time.sleep(1)
                realManSim.manSimPressKey("p")
                break
            
        
        
# ## Test bench 
if __name__ == "__main__":
    botStatesObj = botStates.botStates()
    botStatesObj.initBot()
    chaosDungeonObj = chaosDungeon()   
    chaosDungeonObj.initChaosDungeon(botStatesObj)
    chaosDungeonObj.checkReloadSkill()
    chaosDungeonObj.doChaos_matchMode()
    chaosDungeonObj.doChaos_matchMode()
    # chaosDungeonObj.checkChaosFinished()
    
    
    # while(1):
    #     chaosDungeonObj.botStatesObj.chaosCombatObj.comboListCast()
           
    # outline=[1,1] #小地图怪框大小门限
   
    # chaosDungeonObj.checkChaosFinished()
    # teamColor = [143,112,126]
    
    # while (1):S
    #     re = chaosDungeonObj.botStatesObj.minimapColorScan(teamColor,outline)
        # chaosDungeonObj.checkAndPickDestinySlice()
    # botStatesObj.basicUiCtrlObj.cleanUi()
    
    # while (1):
    #     re = botStatesObj.chaosDungeonObj.enterChaosDugeonInMatchMode()
    #     if re:
    #         break
    #     else:
    #         botStatesObj.basicUiCtrlObj.cleanUi()
            
    # botStatesObj.chaosDungeonObj.doChaosFloor1_matchMode()
    # botStatesObj.chaosDungeonObj.checkAndPickDestinySlice()

    # botStatesObj.basicUiCtrlObj.waitBlackGameLoding()
    
    
                
    
    ## 检查
    #debug
    # color = pyautogui.pixel(int(x),int(y)) #获取指定位置的色值
    # print('色值{}'.format(color))
    # matchColor = pyautogui.pixelMatchesColor(x, y, enemyBarColor_RGB, tolerance=10) #检测指定位置是否指定颜色 误差范围10

 ## 定位小怪物坐标
            #优先定位屏幕中央最近的
            # locations = self.botStatesObj.basicUiCtrlObj.botcolorPicMatches("center","enemyHPbar.bmp",self.redHpColor,0.85)
            
            # if locations != None:
                # x,y = locations
                # color = pyautogui.pixel(int(x),int(y)) #获取指定位置的色值
                # print('色值{}'.format(color))
                
                # self.botStatesObj.chaosCombatObj.enemyDirect[0] = x
                # self.botStatesObj.chaosCombatObj.enemyDirect[1] = y
            # else:
            #     re = self.botStatesObj.minimapColorScan(self.targetColor,self.outline)
                # if re!= None:                    
                    # (tarX,tarY) = self.botStatesObj.basicUiCtrlObj.miniMapTargetCal(re)
                    # self.botStatesObj.chaosCombatObj.enemyDirect[0] = tarX
                    # self.botStatesObj.chaosCombatObj.enemyDirect[1] = tarY   
                    # self.botStatesObj.chaosCombatObj.enemyDirect = self.botStatesObj.UiCoordi["screenCenter"]
                # else:
                    #未找到目标
                    # self.botStatesObj.chaosCombatObj.enemyDirect = self.botStatesObj.UiCoordi["screenCenter"]