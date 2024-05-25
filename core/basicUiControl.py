import pyautogui
import sys
sys.path.append(".") #相对路径或绝对路径
from core import realManSim
import time
import numpy
import cv2
import math


class basicUiCtrl(object):
    
    yGain = numpy.tan(numpy.pi*35/180) #2D->2.5D 坐标转换
    
    def __init__(self,UiRegions,UiCoordi,states,logger) -> None:
        self.UiRegions = UiRegions
        self.UiCoordi = UiCoordi
        self.states = states
        self.picPath = self.states["picPath"]
        self.logger = logger

    def botUiLeftClick(self,UiDictName,idx):
        '''
        左键点击预存UI位置
        '''
        if len(self.UiCoordi[UiDictName])==2:
            realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][0],self.UiCoordi[UiDictName][1])
        else:
            realManSim.manSimMoveAndLeftClick(self.UiCoordi[UiDictName][idx][0],self.UiCoordi[UiDictName][idx][1])
    
    def botPicCheck(self,regionName, pic):
        '''
        检查指定区域图片是否匹配
        '''
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=self.UiRegions[regionName],
        )
        return re    
    
    
    def botcolorPicMatches(self,regionName, pic, tarColor, confidence):
        
        # 读取大图像
        Screen_img = pyautogui.screenshot(region=self.UiRegions[regionName])
        Screen_img = cv2.cvtColor(numpy.array(Screen_img), cv2.COLOR_RGB2BGR)
        base_img = cv2.cvtColor(Screen_img, cv2.COLOR_BGR2RGB)
        base_img = Screen_img
        template = self.picPath+pic
        # 读取模板图像
        template_img = cv2.imread(template, 1)
        # template_bgr = cv2.cvtColor(template_img, 0)
        # template_bgr = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2HSV)
        template_h, template_w = template_img.shape[:2] 

        ## debug
        # cv2.imshow('template_img', template_img)
        # cv2.moveWindow("template_img", 2000,0)
        # cv2.imshow('base_img', base_img)
        # cv2.moveWindow("base_img", 2000,500)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    
        # 确保模板图像不是空的
        if template_img is None:
            print("模板图像未找到，请检查路径")
            return False

        # 获取模板图像的大小
        template_size = template_img.shape[::-1]

        # 使用cv2.TM_CCOEFF_NORMED进行归一化相关匹配
        result = cv2.matchTemplate(base_img, template_img, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)    
        #找到匹配结果中超过阈值的位置
        locations = numpy.where(result >= confidence)
        locations = list(zip(*locations[::-1]))

        for loc in locations:
            x = int(loc[0])+self.UiRegions[regionName][0]
            y = int(loc[1])+self.UiRegions[regionName][1]            
            color = pyautogui.pixel(x,y) #获取指定位置的色值
            print('色值{}'.format(color))
            matchColor = pyautogui.pixelMatchesColor(int(x), int(y), tarColor, tolerance=10) #检测指定位置是否指定颜色 误差范围10
            if matchColor:
                print("匹配的颜色图片")
                return x,y

        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)        
        # if max_val>confidence:
        #     x = int(max_loc[0])+self.UiRegions[regionName][0]
        #     y = int(max_loc[1])+self.UiRegions[regionName][1]
        #     return (x,y)
        # else:
        #     print("未找到匹配图片")
        #     return None
        # 找到匹配结果中超过阈值的位置
        # locations = numpy.where(result >= confidence)
        # locations = list(zip(*locations[::-1]))
        
        # 在目标图像上绘制矩形框
        # cv2.imshow('Result', Screen_img)
        # cv2.moveWindow("Result", 2000,0)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        # 显示结果图像
        # for loc in locations:
        # top_left = max_loc
        # bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
        # cv2.rectangle(base_img, top_left, bottom_right, (74, 128, 128), 2)
        # cv2.imshow('Result', base_img)
        # cv2.moveWindow("Result", 2000,0)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    
    
    def botPicCheckAndClick(self,regionName, pic):
        '''
        检查指定区域图片是否匹配
        '''
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=self.UiRegions[regionName],
        )
        
        if re != None:
            x,y = re
            realManSim.manSimMoveAndLeftClick(x=x, y=y)
            time.sleep(1)
        else:
            print("没有在region:[%s], 找到图片[%s]" %(regionName,pic) )
            return False
        return True
    
    def botPicCustomCheck(self,custRegion, pic):
        '''
        检查指定区域图片是否匹配
        '''
        re = pyautogui.locateCenterOnScreen(
            self.picPath+pic,
            confidence=0.8,
            region=custRegion,
        )
        return re        
        
    #点击确定
    def clickOkButton(self):
        '''
        点击确定
        '''    
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

    #点击同意
    def clickAgreeButton(self):
        '''
        点击确定
        '''    
        time.sleep(1)
        ok = pyautogui.locateCenterOnScreen(
        "res/pic/agreeButton.bmp", region=self.UiRegions["center"], confidence=0.75
        )
        if ok != None:
            x, y = ok
            realManSim.manSimMoveAndLeftClick(x=x, y=y)
            return True
        else:
            return False        
        
   
    def finishTaskAcptRewards(self):
        '''
        提交任务
        '''    
        realManSim.manSimPressKey("G")
        time.sleep(2)
        realManSim.manSimMultiKey("shift","G") 
        time.sleep(2)
        realManSim.manSimPressKey("G")
        realManSim.manSimPressKey("G")
        time.sleep(2)
    
    
    def waitGameLoding(self):
        '''
        等待读条完成
        '''
        
        self.logger.info("wait game loading" )
        time.sleep(5)
        #等待进入loading 界面
        startTime = time.time()
        while(1):
            re = self.botPicCheck("loadingUiRegion","gameLoading.bmp")
            if re!=None:
                self.logger.info("game loading detected")
                time.sleep(3)
                break
            else:
                curTime = time.time()
                if curTime-startTime>50:
                    self.logger.error("stack in game loading stage, bot exist")
                    return False
                    
        #等待loading界面结束
        startTime = time.time()
        while(1):
            re = self.botPicCheck("inTownCheck","inTown.bmp")
            if re!=None:
                self.logger.info("game loading finished")
                time.sleep(3)
                break
            else:
                curTime = time.time()
                if curTime-startTime>50:
                    self.logger.error("stack in game loading stage, bot exist")
                    return False
    
    def waitBlackGameLoding(self):
        '''
        等待短暂切屏完成
        '''
        self.logger.info("wait short game loading, just black screen" )
        #等待进入loading 界面
        startTime = time.time()
        while(1):
            re = self.botPicCheck("inTownCheck","inTown.bmp")
            if re==None:
                self.logger.info("game loading detected")
                time.sleep(3)
                break
            else:
                curTime = time.time()
                if curTime-startTime>50:
                    self.logger.error("stack in game loading stage, bot exist")
                    return False

        #等待loading界面结束
        startTime = time.time()
        while(1):
            re = self.botPicCheck("inTownCheck","inTown.bmp")
            if re!=None:
                self.logger.info("game loading finished")
                time.sleep(1)
                break
            else:
                curTime = time.time()
                if curTime-startTime>50:
                    self.logger.error("stack in game loading stage, bot exist")
                    return False
        
        return True
        
    def cleanUi(self):
        '''
        退出菜单界面
        '''         
        realManSim.manSimPressKey("esc")
        time.sleep(1)
        re = self.botPicCheck("fullScreen","gameMenu.bmp")
        
        if re!=None:
            realManSim.manSimPressKey("esc")

        time.sleep(1)
        
        
        re = self.botPicCheck("fullScreen","ReminderItemClose.bmp")
        if re!=None:
            x,y = re
            realManSim.manSimMoveAndLeftClick(x=x, y=y)
            time.sleep(1)
        return    
    
    def miniMapTargetCal(self,target):
        '''
            根据小地图坐标计算屏幕中的鼠标坐标
        '''                     
        roleX = self.states["minimapRole"][0]
        roleY = self.states["minimapRole"][1]
        
        miniDifX = target[0]-roleX
        miniDifY = target[1]-roleY
        
        tarX = round(miniDifX*30)+self.UiCoordi["screenCenter"][0]
        tarY = round(miniDifY*30*self.yGain)+self.UiCoordi["screenCenter"][1]

        if tarX <self.UiCoordi["moveBoundary_TopLeft"][0]:
            tarX = self.UiCoordi["moveBoundary_TopLeft"][0]
        elif tarX >self.UiCoordi["moveBoundary_BottomRigth"][0]:
            tarX = self.UiCoordi["moveBoundary_BottomRigth"][0]
        
        if tarY <self.UiCoordi["moveBoundary_TopLeft"][1]:
            tarY = self.UiCoordi["moveBoundary_TopLeft"][1]
        elif tarY >self.UiCoordi["moveBoundary_BottomRigth"][1]:
            tarY = self.UiCoordi["moveBoundary_BottomRigth"][1]
    
        return (tarX,tarY)
    
# ## Test bench 
if __name__ == "__main__":
    print("start basicUiCtrl Test")
    basicUiCtrlObj = basicUiCtrl()
    # basicUiCtrlObj.cleanUi()
    basicUiCtrlObj.waitBlackGameLoding()
    