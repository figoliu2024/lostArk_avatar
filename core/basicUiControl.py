import pyautogui
from core import realManSim
import time


class basicUiCtrl(object):
    
    
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
   
    def waitGameLoding(self):
        '''
        等待读条完成
        '''
        startTime = time.time()
        self.logger.info("wait game loading" )
        time.sleep(10)
        while(1):
            #wait loding
            re = self.botPicCheck("loadingUiRegion","gameLoading.bmp")
            if re:
                startTime = time.time()
            else:
                re2 = self.botPicCheck("inTownCheck","inTown.bmp")
                if re2!=None:
                    break
                else:
                    curTime = time.time()
                    if curTime-startTime>30:
                        self.logger.error("stack in game loading stage, bot exist")
                        exit()
        self.logger.info("game loading finished")
        time.sleep(3)
    
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
        return    
               
    
# ## Test bench 
if __name__ == "__main__":
    print("start basicUiCtrl Test")
    