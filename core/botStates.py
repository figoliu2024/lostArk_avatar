
import sys
sys.path.append(".") #相对路径或绝对路径
from core import gameWindowLocate
from core import realManSim
from core import gaodeNavig

from conf.config import defaultStatesConfig
from conf.config import defaultUiRegions
from conf.config import defaultUiCoordi
from conf.config import defaultCharacters
from conf.config import deFaultAbilities
from conf.quickMovePoint import defaultLoPang_points
 
import logging
import time
import pyautogui

## 机器人类
class botStates(object):

    def __init__(self) -> None:
        self.states = defaultStatesConfig
        self.UiRegions = defaultUiRegions
        self.UiCoordi = defaultUiCoordi
        self.Characters = defaultCharacters
        self.loPang_points = defaultLoPang_points
        
        #初始化状态
        self.windowObj = gameWindowLocate.gameWindow()
        self.amapObj = gaodeNavig.amap()
        
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
        
        self.states["windowTopLeft"] = [self.windowObj.topLeftX,self.windowObj.topLeftY]
        print(self.states["windowTopLeft"])
        # 刷新所有UI的 region
        for k in self.UiRegions:
            tmpX = self.UiRegions[k][0]+self.states["windowTopLeft"][0]
            tmpY = self.UiRegions[k][1]+self.states["windowTopLeft"][1]
            self.UiRegions[k]= [tmpX,tmpY,self.UiRegions[k][2],self.UiRegions[k][3]]
            #debug
            # print(k, self.UiRegions[k])

        
        # 刷新所有UI的 coordi
        for k in self.UiCoordi:
            cellSize = len(self.UiCoordi[k])
            if cellSize>2:
                for idx in range(cellSize):
                    tmpX = self.UiCoordi[k][idx][0]+self.states["windowTopLeft"][0]
                    tmpY = self.UiCoordi[k][idx][1]+self.states["windowTopLeft"][1]
                    self.UiCoordi[k][idx][0] = tmpX 
                    self.UiCoordi[k][idx][1] = tmpY
            else:
                tmpX = self.UiCoordi[k][0]+self.states["windowTopLeft"][0]
                tmpY = self.UiCoordi[k][1]+self.states["windowTopLeft"][1]
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
                tmpX = self.loPang_points[k][idx][0]+self.states["windowTopLeft"][0]
                tmpY = self.loPang_points[k][idx][1]+self.states["windowTopLeft"][1]
                self.loPang_points[k][idx][0] = tmpX 
                self.loPang_points[k][idx][1] = tmpY

        
        # 加载导航参数库
        self.amapObj.initAmap(self.UiRegions, self.UiCoordi)
        
        
        # 载入角色技能库
                  
        
    def offlineCheck(self):
        dc = pyautogui.locateOnScreen(
            "./res/pic/dc.png",
            region=self.UiRegions["regions"]["center"],
            confidence=self.states["confidenceForGFN"],
        )
        ok = pyautogui.locateCenterOnScreen(
            "./res/pic/ok.png", region=self.states["regions"]["center"], confidence=0.75
        )

        if dc != None or ok != None:
            currentTime = int(time.time_ns() / 1000000)
            dc = pyautogui.screenshot()
            dc.save("./log/dc_" + str(currentTime) + ".png")
            self.logger.error("disconnection detected...currentTime : {} dc:{} ok:{} ".format(
                    currentTime, dc, ok,))
            self.states["gameOfflineCount"] = self.states["gameOfflineCount"] + 1
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
    
    def botUiLeftClick(self,UiDictName,idx):
        if len(self.UiCoordi[UiDictName])==2:
            realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][0],self.UiCoordi[UiDictName][1])
        else:
            realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][idx][0],self.UiCoordi[UiDictName][idx][1])
    
    def botPicCheck(self,regionName, pic):
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=self.UiRegions[regionName],
        )
        return re
    

    
    #切换角色至charcNo
    def switchCharacterTo(self,charcNo):
        realManSim.manSimPressKey("esc")
        self.botUiLeftClick("fastLoginOtherCharc",0)
        self.botUiLeftClick("charPositions",charcNo)
        self.botUiLeftClick("login",0)
        self.botUiLeftClick("login",0)
        realManSim.sleep(1000,2000)
        re = self.botPicCheck("center","ok.bmp")
        if re != None:
            x, y = re
            realManSim.manSimMoveAndLeftClick(x, y)

        self.waitGameLoding()
        self.logger.info("切换角色至:charc%d成功" %charcNo)
        return True

    
    #点击确定
    def clickOkButton(self):
        time.sleep(1)
        ok = pyautogui.locateCenterOnScreen(
        "res/pic/ok.bmp", region=self.UiRegions["center"], confidence=0.75
        )
        if ok != None:
            x, y = ok
            realManSim.manSimMoveAndLeftClick(x=x, y=y)
            return True
        else:
            return False
        
        
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
            self.states["currentCharacter"] = 0
            print("is charc0")
            return True
        else:
            print("not charc0")
            return False
        
    # #彩虹桥传送
    # def bifrostGoTo(self,destName):
    #     self.botUiLeftClick("bifrost",0)
        
    #     re = self.botPicCheck("fullScreen",destName)
    #     if re != None:
    #         x,y = re
    #         x = x+328
    #         realManSim.manSimMoveAndLeftClick(x, y)
    #         re = self.clickOkButton()
    #         if re:
    #             self.waitGameLoding()
    #             return True
    #         else:
    #             self.logger.error("charctor[%s]-> failed transfer to island lopang " %self.states["currentCharacter"] )
    #             return False
    #     else:
    #         self.logger.error("charctor[%s]-> didn't find lopang bifrost point" %self.states["currentCharacter"] )
    #         return False
    
if __name__ == '__main__':
    botStatesObj = botStates()
    botStatesObj.initBot()
    
    #测试gaodeNavig功能
    botStatesObj.amapObj.loadBigMap("lopang")
    while (1):
        loc = botStatesObj.amapObj.miniMapMatch()
        if loc==-1:
            print('location failed')
        else:
            botStatesObj.amapObj.drawLocateResult(loc)
            print(loc)
    
    # re = botStatesObj.botPicCheck("center","ok.bmp")
    # if re != None:
    #     x, y = re
    #     realManSim.manSimMoveAndLeftClick(x, y)

    
    
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
