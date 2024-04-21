import pyautogui
from core import realManSim
import time 
from PIL import Image
import yaml

## 窗口类
class gameWindow(object):
    #parameters
    # screenWidth = 1920
    # screenHeight = 1080
    # mainWindowIcon_path = f"resources/{screenHeight}/pic/mainWindowIcon.bmp"
    # webGameIcon_path    = f"resources/{screenHeight}/pic/webGame.bmp" 
    # startInWebGamePath  = f"resources/{screenHeight}/pic/startInWebGame.bmp"
    # serverInPath        = f"resources/{screenHeight}/pic/serverIn.bmp"
    # warDancerPath       = f"resources/{screenHeight}/pic/warDancer.bmp"
    # startGamePath       = f"resources/{screenHeight}/pic/startGame.bmp"
    # shutdownOfferPath   = f"resources/{screenHeight}/pic/shutdownOffer.bmp"
    # serverChoisePath    = f"resources/{screenHeight}/pic/serverChoise.bmp"
    # disconnectPath      = f"resources/{screenHeight}/pic/disconnect.bmp"
    


    
    error_time = 600
    const_serverCoordis  = [1862, 64]
    
    def __init__(self) -> None:
        with open("res/picPath.yaml", "r") as yamlfile:
            self.picPath = yaml.safe_load(yamlfile)     
        self.topLeftX = 0
        self.topLeftY = 0

    def scanScreenAndLocate(self):
        ## parameters setting===========================================
        # locate the lost ark window

        # picture src path
   ##------------------ test window------------------------------
        # img = Image.open(self.mainWindowIcon_path)
        # img.show()
        res = pyautogui.locateOnScreen(self.picPath['mainWindowIcon_path'],confidence=0.9)
        if res:
            windowIconCenter = pyautogui.center(res)
            print("search the window Icon, x:%d, y:%d" %(windowIconCenter[0], windowIconCenter[1]))    

            self.topLeftX   = int(windowIconCenter[0]-38)
            self.topLeftY   = int(windowIconCenter[1]-14)
            print("lost ark window initial!")  
            return True
        else:
            print("did not find lostArk Window")
            return False

    def click_icon(self, icon_path):
        time.sleep(0.5)
        res = pyautogui.locateOnScreen(icon_path,confidence=0.9)
        if res:
            iconCenter = pyautogui.center(res)
            realManSim.manSimLeftClick(iconCenter[0], iconCenter[1])
            return True
        else:
            return False

    def findWebGame(self):
        res = pyautogui.locateOnScreen(self.webGameIcon_path,confidence=0.9)
        if res:
            iconCenter = pyautogui.center(res)
            print("found the window Icon, x:%d, y:%d" %(iconCenter[0], iconCenter[1]))    
            print("restart Lost Ark")  
            realManSim.manSimLeftClick(iconCenter[0], iconCenter[1])
            time.sleep(1)
            return True
        else:
            print("did not find webGame ICON")
            return False    
    def checkDisconnect(self):
        res = pyautogui.locateOnScreen(self.disconnectPath,confidence=0.9)
        if res:
            return True
        else:
            return False

    def changeServer(self):
        #切换服务器
        res = self.click_icon(self.serverChoisePath) 
        time.sleep(1)
        print("scan server 2")
        x = self.const_serverCoordis[0]+self.topLeftX
        y = self.const_serverCoordis[1]+self.topLeftY
        matchRes = pyautogui.pixelMatchesColor(x, y, (145, 208, 79), tolerance=3) #检测指定位置是否指定颜色 误差范围3
        if matchRes:
            print("change to server 2")
            realManSim.manSimLeftClick(x, y)
            print("wait for reload")
            time.sleep(1)
            while(1):
                if self.scanScreenAndLocate():
                    break

    def startLostArk(self):
        
        res = self.click_icon(self.startInWebGamePath)
        # res = True
        if res:
            raise_time = time.time()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(raise_time)), "-> raising Lost Ark.")
            while (1):
                res = self.click_icon(self.serverInPath)
                if res:
                    time.sleep(15)
                    res = self.click_icon(self.warDancerPath)
                    time.sleep(5)         
                    res = self.click_icon(self.startGamePath) 
                    while(1):
                        if self.scanScreenAndLocate():
                            break
                    time.sleep(3)       
                    res = self.click_icon(self.shutdownOfferPath) 
                    pyautogui.moveTo(1920/2, 1080/2, duration=0.3)
                    
                    cur_time = time.localtime()
                    print(time.strftime("%Y-%m-%d %H:%M:%S", cur_time), "->: raise Lost Ark Success ...")
                    return True
                else:
                    cur_time = time.time()
                    if cur_time-raise_time>self.error_time:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time)), "->ERROR: raising Lost Ark failed, bot stop!!!.")
                        exit()
                    else:
                        time.sleep(5)
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_time)), "->: wait Lost Ark raise ...")
        else:    
            return False
        
    def shutDownLostArk(self):
        print('shut down lost Ark in 10 sec')
        time.sleep(10)
        pyautogui.hotkey('alt','f4')
 

## funcions===============================================
def trySanAndMoveTo(pic, ScanRegion, confid):
    res = pyautogui.locateOnScreen(pic,region=ScanRegion,confidence=confid)
    tarGetCenter = pyautogui.center(res)
    pyautogui.moveTo((tarGetCenter[0], tarGetCenter[1]))
    print("targetPic Center is, x:%d, y:%d" %(tarGetCenter[0], tarGetCenter[1]))    

##------------------ debug script------------------------------
if __name__ == '__main__':
    windowObj = gameWindow()
    # matchRes = pyautogui.pixelMatchesColor(1862, 64, (145, 208, 79), tolerance=3) #检测指定位置是否指定颜色 误差范围3
    # res = windowObj.click_icon(windowObj.shutdownOfferPath)
    if windowObj.scanScreenAndLocate():
        res = windowObj.changeServer()
        print(res)
    #初始化状态
    # if not windowObj.scanScreenAndLocate():
    #     #未检测到游戏，重新启动游戏
    #     res = windowObj.findWebGame()
    #     if res:
    #         res = windowObj.startLostArk()
            
            
    #     else:
    #         exit()
    #     if windowObj.scanScreenAndLocate():
    #         print('detect lost Ark window')
    #         print('shut down lost Ark in 3 sec')
    #         windowObj.shutDownLostArk()
    # else:
    #     windowObj.shutDownLostArk()


# rodBroken test
# toolsStateRegion = (lostWindow.topLeftX+1369, lostWindow.topLeftY+14, 70, 90)
# trySanAndMoveTo(rodBrokenPath,toolsStateRegion,0.8)