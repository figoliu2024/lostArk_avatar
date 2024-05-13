import sys
sys.path.append(".") #相对路径或绝对路径

import numpy
import pyautogui
import cv2
import time
import yaml
from PIL import Image
from core import realManSim
from core import botStates as botPy
from lib import libMathFigo
from core import basicUiControl as BUCPy




class chaosCombat(object):
    #配置参数
    mapPath = "res/map/"
    picPath = "./res/pic/" 
    
    
    def __init__(self) -> None:
        self.charcSkill = None
        self.skillBarNoCDImage = {
            "Q": None,
            "W": None,
            "E": None,
            "R": None,
            "A": None,
            "S": None,
            "D": None,
            "F": None,
            "V": None,
        }
            
        
    def initChaosCombat(self,statesConfig,UiCoordi,basicUiCtrlObj,skillBarRegions):
        '''
        chaosCombat对象初始化
        '''        
        print ("initiation chaosCombat")
        self.statesConfig = statesConfig
        self.basicUiCtrlObj = basicUiCtrlObj
        self.skillBarRegions = skillBarRegions
        self.UiCoordi = UiCoordi
        
        self.enemyDirect = self.UiCoordi["screenCenter"]
        
    def loadSkill(self, charcSkill):
        '''
        chaosCombat加载当前角色技能表
        '''   
        self.charcSkill = charcSkill
    
    
    def saveSkillBarNoCDImage(self):
        '''
        chaosCombat加载当前角色技能栏无CD时状态
        '''   
        for key in self.skillBarRegions:
            img = pyautogui.screenshot(region=self.skillBarRegions[key])
            self.skillBarNoCDImage[key] = img
            
        #debug
        # img.show()
            
    
    def checkCD(self, key):
        '''
        检查技能是否在CD
        '''   
        re = pyautogui.locateOnScreen(self.skillBarNoCDImage[key], confidence=0.9, region=self.skillBarRegions[key])
        if re==None:
            return False
            #debug
            # print("skill [%s] is in CD" %key)
        else:
            return True
            
        
    def castSkill(self, key):
        
        startTime = time.time()
        while(1):
            if self.checkCD(key):
                if self.charcSkill[key]["directional"] == True:
                    realManSim.manSimMoveTo(self.enemyDirect[0], self.enemyDirect[1])

                if self.charcSkill[key]["cast"] == True:
                    #多次连击
                    start_ms = int(time.time_ns() / 1000000)
                    now_ms = int(time.time_ns() / 1000000)
                    while now_ms - start_ms < self.charcSkill[key]["castTime"]:
                        now_ms = int(time.time_ns() / 1000000)
                        realManSim.manSimPressKey(key)
                        time.sleep(0.2)
                elif self.charcSkill[key]["hold"] == True:
                    #按住不动
                    start_ms = int(time.time_ns() / 1000000)
                    now_ms = int(time.time_ns() / 1000000)
                    pyautogui.keyDown(key)
                    while now_ms - start_ms < self.charcSkill[key]["holdTime"]:
                        now_ms = int(time.time_ns() / 1000000)
                        time.sleep(0.1)
                    pyautogui.keyUp(key)
                else:
                    #瞬发
                    realManSim.manSimPressKey(key)
                    start_ms = int(time.time_ns() / 1000000)
                    now_ms = int(time.time_ns() / 1000000)
                    while now_ms - start_ms < self.charcSkill[key]["castTime"]:
                        now_ms = int(time.time_ns() / 1000000)
                        time.sleep(0.2)
            else:
                return False
                #in CD
            curTime = time.time()
            if curTime-startTime>10:
                print("stack in game cast skill [%s]" %key)
                return False                


# ## Test bench 
if __name__ == "__main__":
    botStatesObj = botPy.botStates()
    botStatesObj.initBot()
    botStatesObj.chaosCombatObj.saveSkillBarNoCDImage()
    
    botStatesObj.chaosCombatObj.loadSkill(botStatesObj.skill_Wardancer)
    
    while(1):
        for key in botStatesObj.chaosCombatObj.skillBarRegions:
            botStatesObj.chaosCombatObj.castSkill(key)
            # botStatesObj.chaosCombatObj.checkCD(key)
            # time.sleep(1)