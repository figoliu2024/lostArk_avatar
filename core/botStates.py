
import sys
sys.path.append(".") #相对路径或绝对路径
from core import gameWindowLocate
from core import realManSim
from core import gaodeNavig
from core import basicUiControl as BUCPy
from core import battle

from conf.config import defaultStatesConfig
from conf.config import defaultUiRegions
from conf.config import defaultUiCoordi
from conf.config import defaultCharacters
# from conf.config import deFaultAbilities
from conf.skillLists import defaultSkillBarRegions
from conf.quickMovePoint import defaultLoPang_points

from conf import skillLists

 
import logging
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image

## 机器人类
class botStates(object):

    def __init__(self) -> None:
        self.statesConfig = defaultStatesConfig
        self.UiRegions = defaultUiRegions
        self.UiCoordi = defaultUiCoordi
        self.Characters = defaultCharacters
        self.loPang_points = defaultLoPang_points
        # self.breakStone_points = defaultBreakStone_points
        self.skillBarRegions = defaultSkillBarRegions
        
        
        #初始化状态
        self.windowObj = gameWindowLocate.gameWindow()
        self.amapObj = gaodeNavig.amap()
        self.lopangMoveObj = gaodeNavig.lopangMove()
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关 
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.picPath = "./res/pic/"
        
        
    def initBot(self):
        
        result = self.windowObj.scanScreenAndLocate()


        # if not result:
        #     #未检测到游戏，尝试启动游戏（预登陆webgame）
        #     self.logger.debug("未检测到游戏，尝试启动游戏（必须预先登陆webgame）")
        #     self.windowObj.startLostArk()
        #     time.sleep(3)
        #     result = self.windowObj.scanScreenAndLocate()
        #     if not result:
        #         self.logger.error('未检测到游戏，尝试启动游戏失败，退出脚本！！！')
        #         exit()
        
        self.statesConfig["windowTopLeft"] = [self.windowObj.topLeftX,self.windowObj.topLeftY]
        print(self.statesConfig["windowTopLeft"])
        # 刷新所有UI的 region
        for k in self.UiRegions:
            tmpX = self.UiRegions[k][0]+self.statesConfig["windowTopLeft"][0]
            tmpY = self.UiRegions[k][1]+self.statesConfig["windowTopLeft"][1]
            self.UiRegions[k]= [tmpX,tmpY,self.UiRegions[k][2],self.UiRegions[k][3]]
            #debug
            # print(k, self.UiRegions[k])

        
        # 刷新所有UI的 coordi
        for k in self.UiCoordi:
            cellSize = len(self.UiCoordi[k])
            if cellSize>2:
                for idx in range(cellSize):
                    tmpX = self.UiCoordi[k][idx][0]+self.statesConfig["windowTopLeft"][0]
                    tmpY = self.UiCoordi[k][idx][1]+self.statesConfig["windowTopLeft"][1]
                    self.UiCoordi[k][idx][0] = tmpX 
                    self.UiCoordi[k][idx][1] = tmpY
            else:
                tmpX = self.UiCoordi[k][0]+self.statesConfig["windowTopLeft"][0]
                tmpY = self.UiCoordi[k][1]+self.statesConfig["windowTopLeft"][1]
                self.UiCoordi[k][0] = tmpX 
                self.UiCoordi[k][1] = tmpY
            #debug
            # print(k, self.UiCoordi[k])
            # print(k, self.UiCoordi[k])
        # self.curStates["windowTopLeft_y"] = self.windowObj.topLeftY
        
        # 刷新所有quickMovePoint点
        for k in self.loPang_points:
            cellSize = len(self.loPang_points[k])
            for idx in range(cellSize):
                tmpX = self.loPang_points[k][idx][0]+self.statesConfig["windowTopLeft"][0]
                tmpY = self.loPang_points[k][idx][1]+self.statesConfig["windowTopLeft"][1]
                self.loPang_points[k][idx][0] = tmpX 
                self.loPang_points[k][idx][1] = tmpY

        # for k in self.breakStone_points:
        #     cellSize = len(self.breakStone_points[k])
        #     for idx in range(cellSize):
        #         tmpX = self.breakStone_points[k][idx][0]+self.statesConfig["windowTopLeft"][0]
        #         tmpY = self.breakStone_points[k][idx][1]+self.statesConfig["windowTopLeft"][1]
        #         self.breakStone_points[k][idx][0] = tmpX 
        #         self.breakStone_points[k][idx][1] = tmpY        
        # 加载基本控制库
        self.basicUiCtrlObj = BUCPy.basicUiCtrl(self.UiRegions, self.UiCoordi, self.statesConfig, self.logger)
        
        # 加载导航参数库
        self.amapObj.initAmap(self.UiRegions, self.UiCoordi, self.basicUiCtrlObj, self.statesConfig)
        
        # 加载罗庞任务移动对象
        self.lopangMoveObj.initLopangMove(self.UiRegions, self.UiCoordi, self.basicUiCtrlObj, self.loPang_points)
        
        # 刷新动作条库
        for k in self.skillBarRegions:
            tmpX = self.skillBarRegions[k][0]+self.statesConfig["windowTopLeft"][0]
            tmpY = self.skillBarRegions[k][1]+self.statesConfig["windowTopLeft"][1]
            self.skillBarRegions[k]= [tmpX,tmpY,self.skillBarRegions[k][2],self.skillBarRegions[k][3]]
            
        # 载入角色技能库
        self.charcSkill = skillLists.Wardancer
        
        # 加载战斗模块
        self.chaosCombatObj = battle.chaosCombat
        # self.skill_Artist    = skillLists.Artist
        # self.skill_Arcanist  = skillLists.Arcanist
        
        
    def offlineCheck(self):
        dc = pyautogui.locateOnScreen(
            "./res/pic/dc.png",
            region=self.UiRegions["center"],
            confidence=self.statesConfig["confidenceForGFN"],
        )
        ok = pyautogui.locateCenterOnScreen(
            "./res/pic/ok.png", region=self.statesConfig["center"], confidence=0.75
        )

        if dc != None or ok != None:
            currentTime = int(time.time_ns() / 1000000)
            dc = pyautogui.screenshot()
            dc.save("./log/dc_" + str(currentTime) + ".png")
            self.logger.error("disconnection detected...currentTime : {} dc:{} ok:{} ".format(
                    currentTime, dc, ok,))
            self.statesConfig["gameOfflineCount"] = self.statesConfig["gameOfflineCount"] + 1
            return True
        else:
            return False
        
    def inTownCheck(self):
        inTown = pyautogui.locateCenterOnScreen(
            "../res/pic/inTown.bmp",
            region = self.UiRegions["inTownCheck"],
            confidence=0.75,
            )
        return inTown
    
    def inChaosCheck(self):
        inChaos = pyautogui.locateCenterOnScreen(
            "../res/pic/inChaos.png",
            region = self.UiRegions["inChaosCheck"],
            confidence=0.75,
            )
        return inChaos   
    
    # def botUiLeftClick(self,UiDictName,idx):
    #     if len(self.UiCoordi[UiDictName])==2:
    #         realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][0],self.UiCoordi[UiDictName][1])
    #     else:
    #         realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][idx][0],self.UiCoordi[UiDictName][idx][1])
    
    # def botPicCheck(self,regionName, pic):
    #     re = pyautogui.locateCenterOnScreen(
    #         self.picPath+pic,
    #         confidence=0.8,
    #         region=self.UiRegions[regionName],
    #     )
    #     return re
    

    
    #切换角色至charcNo
    def switchCharacterTo(self,charcNo):
        realManSim.manSimPressKey("esc")
        self.basicUiCtrlObj.botUiLeftClick("fastLoginOtherCharc",0)
        self.basicUiCtrlObj.botUiLeftClick("charPositions",charcNo)
        self.basicUiCtrlObj.botUiLeftClick("login",0)
        self.basicUiCtrlObj.botUiLeftClick("login",0)
        realManSim.sleep(1000,2000)
        re = self.basicUiCtrlObj.botPicCheck("center","ok.bmp")
        if re != None:
            x, y = re
            realManSim.manSimMoveAndLeftClick(x, y)
            self.basicUiCtrlObj.waitGameLoding()
            self.basicUiCtrlObj.logger.info("切换角色至:charc%d成功" %charcNo)
        else:
            #已经切换至目标角色
            self.basicUiCtrlObj.logger.info("当前已经是:charc%d,无需切换" %charcNo)
            self.basicUiCtrlObj.cleanUi()
            self.basicUiCtrlObj.cleanUi()

        match charcNo:
            case 0:
                self.charcSkill = skillLists.Wardancer 
            case 1: 
                self.charcSkill = skillLists.Artist
            case 4:
                self.charcSkill = skillLists.Arcanist
            case _:
                #其他未支持角色
                self.charcSkill = skillLists.Wardancer
                
                
        return True

        
    #检查当前角色是否是0号    
    def isCharc0Check(self):

        realManSim.manSimPressKey("esc")
        isCharc0 = pyautogui.locateCenterOnScreen(
            "res/pic/charNameBaiyuekui.bmp", #改成第一个角色名
            confidence=0.8,
            region=self.UiRegions["quickCharacterCheck"],
        )
        realManSim.manSimPressKey("esc")
        # print(isCharc0)
        if isCharc0 != None:
            self.statesConfig["currentCharacter"] = 0
            print("is charc0")
            return True
        else:
            print("not charc0")
            return False
        
    #寻找特定颜色
    def colorScan(self, targetColor,outline):
        '''
        扫描特定颜色并按照颜色大小判断
        '''
        #设定颜色HSV范围
        colorLower = np.array([targetColor[0]-10,targetColor[1]-10,  targetColor[2]])
        colorUpper = np.array([targetColor[0]+10,255,  targetColor[2]])
        #截图
        img = pyautogui.screenshot(region=self.UiRegions["fullScreen"])    
            
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
        #将图像转化为HSV格式
        img_hls = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HLS)
        # #去除颜色范围外的其余颜色
        mask = cv2.inRange(img_hls, colorLower, colorUpper)
        
        _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            #cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高
            boxes = [cv2.boundingRect(c) for c in contours]
            for box in boxes:
                x, y, w, h = box
                if w>outline[0] and h>outline[1]:
                #绘制矩形框对轮廓进行定位
                    monsterX = int(x+w/2)
                    monsterY = int(y+h/2)
                    #将绘制的图像展示
                    # cv2.rectangle(img_cv2, (x, y), (x+w, y+h), (0, 0, 233), 2)
                    # cv2.namedWindow("monster scan result", 0)
                    # cv2.resizeWindow("monster scan result", 960,540)
                    # cv2.moveWindow("monster scan result", 2000,0)
                    # cv2.imshow('monster scan result', img_cv2)
                    # if cv2.waitKey(25) & 0xFF == ord('q'):
                    #     cv2.destroyAllWindows()
                        
                    return [monsterX,monsterY]  
        
        #debug
        # cv2.namedWindow("HSV window", 0)
        # cv2.resizeWindow("HSV window", 960,540)
        # cv2.moveWindow("HSV window", 2000,0)
        # cv2.imshow("HSV window", mask)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        return None       


def getPixlHSV():
    while (1):
        pos = pyautogui.position()# 获取鼠标当前的位置
        color = pyautogui.pixel(pos[0],pos[1]) #获取指定位置的色值
        print('RGB色值{}'.format(color))
        
        cv2Pix = np.uint8([[color]])
        cv2Pix = cv2.cvtColor(cv2Pix, cv2.COLOR_RGB2BGR)
        color_hsv = cv2.cvtColor(cv2Pix, cv2.COLOR_BGR2HSV)
        print('color_hsv色值{}'.format(color_hsv))
        time.sleep(1)        

        
if __name__ == '__main__':
    botStatesObj = botStates()
    botStatesObj.initBot()
    
    #测试gaodeNavig功能
    # botStatesObj.amapObj.loadBigMap("lopang")
    # while (1):
    #     loc = botStatesObj.amapObj.miniMapMatch()
    #     if loc==-1:
    #         print('location failed')
    #     else:
    #         botStatesObj.amapObj.drawLocateResult(loc)
    #         print(loc)
    
    re = botStatesObj.basicUiCtrlObj.botPicCheck("EvnaTaskFinishedCheck","taskDestinyEyeStatus.bmp")
    if re != None:
        x, y = re
        realManSim.manSimMoveAndLeftClick(x, y)

    # 测试找色功能
    # h = 90
    # s = 19
    # v = 255
    # while (1):
    #     targetColor=[h,s,v]
    #     outline=[50,50]
    #     re = botStatesObj.colorScan(targetColor,outline)

    #     print(re)
        # time.sleep(1)
    # re = botStatesObj.isCharc0Check()
    # if ~re:
    #     botStatesObj.switchCharacterTo(0)
        
    # ok = pyautogui.locateCenterOnScreen(
    #     "res/pic/ok.bmp", region=botStatesObj.UiRegions["center"], confidence=0.75
    # )
    # print(ok)
# 日志  
    # botStatesObj.logger.debug('这是 logger debug message')
    # botStatesObj.logger.info('这是 logger info message')
    # botStatesObj.logger.warning('这是 logger warning message')
    # botStatesObj.logger.error('这是 logger error message')
    # botStatesObj.logger.critical('这是 logger critical message')
