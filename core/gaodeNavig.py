import sys
sys.path.append(".") #相对路径或绝对路径

import numpy
import pyautogui
import cv2
import time
import yaml
from PIL import Image
import core.aStarFigo as aStarFigo
from core import realManSim
from core import botStates as botPy
from lib import libMathFigo


class cell(object):
    def __init__(self, x, y, reachable:bool) -> None:
        self.x = x
        self.y = y
        self.isReachable = reachable
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        self.parent = None
        self.weight = 0
        
    def __lt__(self, other):
        return self.f < other.f

class amap(object):
    #配置参数
    mapPath = "res/map/"
    picPath = "./res/pic/" 
    errorCheckTimes = 1
    confid = 0.2 #定位置信度
    roleLabelColor = (125,0,125)
    roleShift_x = 97
    roleShift_y = 83
    lw = 1
    
    def __init__(self) -> None:
        '''
        初始化一些数据结构：堆、集合帮助实现算法
        '''
        self.aStarObj  = aStarFigo.aStar()
        self.cells = []
        self.grid_width = 0
        self.grid_height = 0

    def initAmap(self,UiRegions,UiCoordi):
        '''
        amap对象初始化
        '''
        print ("initiation Amap")
        self.UiRegions = UiRegions
        self.UiCoordi = UiCoordi


  
    def loadBigMap(self, mapName):
        '''
        读取大地图截图
        '''
        #读取彩色地图截图
        self.mapName = mapName
        curMapFullPath = self.mapPath+self.mapName+".bmp"
        bigMapRGB = Image.open(curMapFullPath)
        bigMapRGB = cv2.cvtColor(numpy.array(bigMapRGB), cv2.COLOR_RGB2BGR)
        bigMapCv2 = cv2.cvtColor(numpy.array(bigMapRGB), 0)
        self.bigMapRGB = bigMapCv2
        self.bigMapCv2 = cv2.cvtColor(bigMapCv2, cv2.COLOR_BGR2GRAY)
        #读取二值化地图
        saveMapPath = self.mapPath+self.mapName+".txt"
        self.bigMapData = numpy.genfromtxt(saveMapPath,delimiter = ',')
        self.grid_height = numpy.size(self.bigMapData,0)
        self.grid_width = numpy.size(self.bigMapData,1)
        self.init_grid()
    
    def init_grid(self):
        '''
        初始化地图,导入cells
        '''
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.bigMapData[y][x] == 0:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(cell(x, y, reachable))
    
        
    def miniMapMatch(self):
        '''
        小地图坐标匹配
        '''
        estNum = self.errorCheckTimes
        estVec = numpy.zeros((estNum,2), dtype=int)
        for idx in range(estNum):
            miniMapRGB = pyautogui.screenshot(region=self.UiRegions["minimap"])
            miniMap_cv2 = cv2.cvtColor(numpy.array(miniMapRGB), 0)
            miniMap_cv2 = cv2.cvtColor(numpy.array(miniMap_cv2), cv2.COLOR_RGB2BGR)
            miniMap_cv2 = cv2.cvtColor(miniMap_cv2, cv2.COLOR_BGR2GRAY)
            x, y = miniMap_cv2.shape[0:2]
            miniMapZoom2_cv2 = cv2.resize(miniMap_cv2, (int(y / 1.5), int(x / 1.5)))
            res = cv2.matchTemplate(self.bigMapCv2, miniMapZoom2_cv2, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val>self.confid:
                max_loc = (max_loc[0]+self.roleShift_x, max_loc[1]+self.roleShift_y)
            else:
                print('miniMap match failed')
                return -1
            estVec[idx]=max_loc
        # estVec[idx] = routeBot.locateObj.miniMapMatch()
        curLoc = numpy.mean(estVec,axis=0)
        curLoc = curLoc.astype(int)
        return (curLoc[0],curLoc[1])

    def get_cell(self, x, y):
        '''
        因为输入cells信息时为一维信息，这里需要通过width和height检索到相应位置的cell
        '''
        return self.cells[ x * self.grid_height + y ]

    def caculate_one_way(self, start, end):
        '''
        在地图确定不变的情况下，每次传入不同的起点和终点
        '''
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def drawLocateResult(self, loc):
        '''
        二值化地图定位结果打印
        大地图上画矩形显示定位坐标结果 
        '''  
        # loc = (loc[0]+roleShift_x, loc[1]+roleShift_y)
        top_left = (loc[0] - self.lw, loc[1] - self.lw)
        bottom_right = (loc[0] + self.lw, loc[1] + self.lw)
        
        # # 展示结果
        tmpbinMapData = self.bigMapRGB
        cv2.rectangle(tmpbinMapData, top_left, bottom_right, self.roleLabelColor, 2)
        # cv2.imshow('locate result', bigMapCv2)
        cv2.namedWindow("locate result", 0)
        cv2.resizeWindow("locate result", 700,450)
        cv2.moveWindow("locate result", 2000,0)
        cv2.imshow('locate result', tmpbinMapData)
        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

    def picCheck(self,regionName, pic):
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=self.UiRegions[regionName],
        )
        return re

    #彩虹桥传送
    def bifrostGoTo(self,destName):
        self.botUiLeftClick("bifrost",0)
        
        re = self.botPicCheck("fullScreen",destName)
        if re != None:
            x,y = re
            x = x+328
            realManSim.manSimMoveAndLeftClick(x, y)
            re = self.clickOkButton()
            if re:
                self.waitGameLoding()
                return True
            else:
                self.logger.error("charctor[%s]-> failed transfer to island lopang " %self.states["currentCharacter"] )
                return False
        else:
            self.logger.error("charctor[%s]-> didn't find lopang bifrost point" %self.states["currentCharacter"] )
            return False

class lopangMove(object):
    def __init__(self) -> None:
        self.picPath = "./res/pic/"      
    
    def initLopangMove(self,UiRegions,UiCoordi,loPang_points):
        '''
        lopang对象初始化
        '''
        print ("initiation lopangMove")
        self.UiRegions = UiRegions
        self.UiCoordi = UiCoordi
        self.loPang_points = loPang_points
        self.rolePosition = self.UiCoordi["screenCenter"]
    
    def pointPicCheck(self,regionName, pic):
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=self.UiRegions[regionName],
        )
        return re
    
    def runToStartPoint(self):
        '''
        去往第一个检查点
        '''
        time.sleep(1)
        re = self.pointPicCheck("fullScreen", "loPang_startPoint.bmp")
        if re != None:
            x,y = re
            realManSim.manSimMoveAndRightClick(x, y)
            time.sleep(2)
            print("move to start check point success..")
        else:
            print("check start point failed, bot exist!!")
            exit()        
    
    def runToBenongTerminal(self):
        print("move from start Point to Benong Terminal..")
        for k in self.loPang_points["startPointToBenong"]:
            x = k[0]
            y = k[1]
            print("move to the [x:%d y:%d] "%(x,y))
            realManSim.manSimMoveAndRightClick(x, y)
            time.sleep(2)
            
            
        re = self.pointPicCheck("fullScreen", "benongTerminal.bmp")
        
        if re != None:
            dist = libMathFigo.eucliDist(re,self.rolePosition)
            print("Distance from role to Benong Terminal is: %d" %dist)
            if dist<360:
                print("move from start Point to Benong Terminal success..")
            else:
                x,y = re
                realManSim.manSimMoveAndRightClick(x, y+269)
                print("try last time move to Benong Terminal success..")
                time.sleep(2)     
        else:
            print("check start Benong Terminal failed, bot exist!!")
            exit()               

    def runToARTYTerminal(self):
        print("move from start Point to ARTY Terminal..")
        for k in self.loPang_points["BenongToARTY"]:
            x = k[0]
            y = k[1]
            print("move to the [x:%d y:%d] "%(x,y))
            realManSim.manSimMoveAndRightClick(x, y)
            time.sleep(2)
            
        re = self.pointPicCheck("fullScreen", "ARTYTerminal.bmp")
        
        if re != None:
            dist = libMathFigo.eucliDist(re,self.rolePosition)
            print("Distance from role to ARTY Terminal is: %d" %dist)
            if dist<360:
                print("move from start Point to ARTY Terminal success..")
            else:
                x,y = re
                realManSim.manSimMoveAndRightClick(x, y+269)
                print("try last time move to ARTY Terminal success..")
                time.sleep(2)     
        else:
            print("check ARTY Terminal failed, bot exist!!")
            exit()               
        
# bmp地图转化为产生二值化地图
def binMapGen(mapPath, outMapName):
    print ("transfer map pic to Bin Data")
    bigMap = Image.open(mapPath)
    # bigMap = cv2.imread(mapPath, 1)
    bigMapCv2 = cv2.cvtColor(numpy.array(bigMap), 0)
    bigMapCv2 = cv2.cvtColor(bigMapCv2, cv2.COLOR_BGR2GRAY)
    wallCheckStep = 1
    # global thresholding

    ret2,th2 = cv2.threshold(bigMapCv2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  
    ret, mask_all = cv2.threshold(src=bigMapCv2,             # 要二值化的图片
                    thresh=130,           # 全局阈值
                    maxval=255,           # 大于全局阈值后设定的值
                    type=cv2.THRESH_BINARY)# 设定的二值化类型，
    
    #扩大不可通过区域
    grid_height = numpy.size(mask_all,0)
    grid_width  = numpy.size(mask_all,1)
    binMap = numpy.zeros((grid_height,grid_width))+int(255)
    for x in range(grid_width):
        for y in range(grid_height):
                if mask_all[y][x]==0:
                    for dx, dy in [ (wallCheckStep, 0), (0, wallCheckStep), (-wallCheckStep, 0), (0, -wallCheckStep), (wallCheckStep, -wallCheckStep), (-wallCheckStep, wallCheckStep), (-wallCheckStep, -wallCheckStep), (wallCheckStep, wallCheckStep) ]:
                        x2 = x + dx
                        y2 = y + dy      
                        if x2>=0 and x2<grid_width and y2>=0 and y2<grid_height: #地图范围内
                            binMap[y2][x2]=0

                        
    numpy.savetxt("res/map/"+outMapName, binMap, fmt = '%d', delimiter = ',')
    cv2.imshow('gray', bigMapCv2)
    cv2.imshow('binMap', binMap)
    cv2.imshow('binMap', binMap)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    
# ## Test bench 
if __name__ == "__main__":

    # luopangPath = f"res/map/lopang.bmp"
    # binMapGen(luopangPath,"luopang.txt")
    botStatesObj = botPy.botStates()
    lopangMoveObj = lopangMove()
    
    botStatesObj.initBot()
    
    # lopangMoveObj.initLopangMove(botStatesObj.UiRegions, botStatesObj.UiCoordi, botStatesObj.loPang_points)
    # realManSim.manSimPressKey("G")
    # lopangMoveObj.runToStartPoint()
    # lopangMoveObj.runToBenongTerminal()
    # realManSim.manSimPressKey("G")
    # lopangMoveObj.runToARTYTerminal()
    # realManSim.manSimPressKey("G")
    
    re = botStatesObj.bifrostGoTo("XSR_Bifrost.bmp")
    realManSim.manSimPressKey("G")
    realManSim.manSimMultiKey("shift","G") 
    realManSim.manSimPressKey("G")
    
    #班船旅行脚本