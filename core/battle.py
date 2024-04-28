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
            
        
    def initChaosCombat(self,statesConfig,basicUiCtrlObj,skillBarRegions):
        '''
        chaosCombat对象初始化
        '''        
        print ("initiation chaosCombat")
        self.statesConfig = statesConfig
        self.basicUiCtrlObj = basicUiCtrlObj
        self.skillBarRegions = skillBarRegions
        
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
            img = pyautogui.screenshot(region=key)
            self.skillBarNoCDImage[key] = img
        
        
            
    
    def checkCDandCast(self):
        '''
        释放技能
        '''   


# ## Test bench 
if __name__ == "__main__":
    botStatesObj = botPy.botStates()
    botStatesObj.initBot()
    