import numpy
import pyautogui
import cv2
import time
from time import gmtime, strftime
import random
# import win32gui
import yaml
import sys
import realManSim
import gameWindowLocate
import colorsys

class fishBot(object):
    
    #parameters
    with open("resources/keybindings.yaml", "r") as yamlfile:
        keybindings = yaml.safe_load(yamlfile)
        
    with open("resources/path.yaml", "r") as yamlfile:
        tmpConfig = yaml.safe_load(yamlfile)     
        picPath = tmpConfig['picPath']
        
    screenHeight = 1080
    # picPath = f"resources/{screenHeight}/pic/"
    fishGameReadyPath   = picPath+"fishGameReady.png"
    anchorPath          = picPath+"anchor.bmp"
    inFishGamePath      = picPath+"inFishGame.png"
    needRepairPath      = picPath+"needRepair.png"
    templatePath        = picPath+"template.bmp"
    templateInStarBitchPath = picPath+"templateInStarBitch.bmp"
    poplavokPath        = picPath+"poplavok.bmp"
    beiraPath           = picPath+"beira.bmp"
    inHomePath          = picPath+"inHome.bmp"
    lifeToolsRepairPath = picPath+"lifeToolsRepair.bmp"
    mainWindowIcon_path = picPath+"mainWindowIcon.bmp"
    
    fishGameWaitTime = 3 #10s
    fishGameDuartion = 5 #in 5s
    templateRegion = (920,440,80,100)
    fishGameBarRegion = (500,120,120,530)
    fishGameInGameRegion = (0, 0, 100, 100)
    fishGameReadyRegion = (860, 390, 200, 300)
    beiraStatusRegion = (4, 0,930, 27)
    
    barX = 508
    barYMin = 124
    barYMax = 540
    perfectColor_R = 215

    emptyColor = (84,79,90)
    beiraExistColor_H = 78
    
    vitXY = (800, 1000)


    lifeToolsRepair_x = 1034
    lifeToolsRepair_y = 890
    
    lifeToolsAll_x = 871
    lifeToolsAll_y = 760   

    remoteRepair_x = 1250
    remoteRepair_y = 700
    
    repairAll_x = 735
    repairAll_y = 805   

    repairOK_x = 920
    repairOK_y = 630
    
    fishPool_x = 872
    fishPool_y = 866

    
    # def __init__(self) -> None:
        

            
    def renewAllCoord(self, topLeftX, topLeftY):
        '''
        定位游戏窗口并更新所有区域坐标
        '''
        self.fishGameBarRegion      = list(self.fishGameBarRegion)
        self.fishGameInGameRegion   = list(self.fishGameInGameRegion)
        self.fishGameReadyRegion    = list(self.fishGameReadyRegion )
        self.templateRegion         = list(self.templateRegion      )
        self.beiraStatusRegion      = list(self.beiraStatusRegion)

        
        self.fishGameBarRegion[0]   = int(self.fishGameBarRegion[0]+topLeftX)
        self.fishGameBarRegion[1]   = int(self.fishGameBarRegion[1]+topLeftY)
        self.fishGameInGameRegion[0]= int(self.fishGameInGameRegion[0]+topLeftX)
        self.fishGameInGameRegion[1]= int(self.fishGameInGameRegion[1]+topLeftY)
        self.fishGameReadyRegion[0] = int(self.fishGameReadyRegion[0]+topLeftX)
        self.fishGameReadyRegion[1] = int(self.fishGameReadyRegion[1]+topLeftY)
        self.templateRegion[0]      = int(self.templateRegion[0]+topLeftX)
        self.templateRegion[1]      = int(self.templateRegion[1]+topLeftY)
        self.beiraStatusRegion[0]   = int(self.beiraStatusRegion[0]+topLeftX)
        self.beiraStatusRegion[1]   = int(self.beiraStatusRegion[1]+topLeftY)   
        

        self.barX       = int(self.barX  + topLeftX)
        self.barYMin    = int(self.barYMin + topLeftY)
        self.barYMax    = int(self.barYMax + topLeftY)
        self.vitXY      = self.vitXY + (topLeftX, topLeftY)
    
        self.remoteRepair_x = self.remoteRepair_x + topLeftX  
        self.remoteRepair_y = self.remoteRepair_y + topLeftY
        self.repairAll_x    = self.repairAll_x    + topLeftX 
        self.repairAll_y    = self.repairAll_y    + topLeftY    
        self.repairOK_x     = self.repairOK_x     + topLeftX 
        self.repairOK_y     = self.repairOK_y     + topLeftY 
        self.fishPool_x     = self.fishPool_x     + topLeftX 
        self.fishPool_y     = self.fishPool_y     + topLeftY 
        self.lifeToolsRepair_x = self.lifeToolsRepair_x+topLeftX
        self.lifeToolsRepair_y = self.lifeToolsRepair_y+topLeftY
        self.lifeToolsAll_x = self.lifeToolsAll_x+topLeftX
        self.lifeToolsAll_y = self.lifeToolsAll_y+topLeftY
         
    def castFishingRod(self, count):
        '''
        Function to cast fishing rod ingame
        '''
        print(strftime("%H:%M:%S", gmtime()), f"Casting fishing rod. Counter: {count}")

        # Cast fishing rod ingame
        realManSim.manSimPressKey(self.keybindings['fishing'])
        time.sleep( random.uniform(4.5, 6.5))

    
# 
    def playFishGame(self):
        '''
        function with play the Fish mini game
        '''
        print(strftime("%H:%M:%S", gmtime()), f"play the fish mini Game")
        
        realManSim.manSimPressKey(self.keybindings['castNet'])

        # wait the game begining until find the anchor
        time.sleep(5)    
        
        # judge success in game
        res = pyautogui.locateOnScreen(self.inFishGamePath,region=self.fishGameInGameRegion,confidence=0.9)
            
        if res:
            print(strftime("%H:%M:%S", gmtime()), f"start the fish mini game success")
        else:
            print(strftime("%H:%M:%S", gmtime()), f"fail start the fish mini game")
            return 
            
        startTime = time.time()
        findAnchor = False
        while(~findAnchor):
            res = pyautogui.locateOnScreen(self.anchorPath,region=self.fishGameBarRegion,confidence=0.7)
            if res:
                print(strftime("%H:%M:%S", gmtime()), f"find the anchor")
                findAnchor = True
                break
            else:
                cutTime = time.time()
                print(strftime("%H:%M:%S", gmtime()), f'not find the anchor time:{cutTime-startTime:.1f}s')
                if cutTime-startTime>self.fishGameWaitTime:
                    break
                
        #in mini game
        if findAnchor:
            # scan the fish game bar, find the center of the perfect bar
            # screen shot the game bar
            print(strftime("%H:%M:%S", gmtime()), "scan the fish game bar color")
            time.sleep(0.2)
            barImg = pyautogui.screenshot(region=(self.barX,self.barYMin,1,430))
            barMat = numpy.array(barImg)
            barMat_R = barMat[:,0,0]
            perIdx = numpy.argwhere(abs(barMat_R-self.perfectColor_R)<5)
            if perIdx.size==0:
                return 0
            else:
                perIdx.astype(int)
            minIdx = perIdx[0]
            maxIdx = perIdx[-1]
            maxYPer = maxIdx+self.barYMin
            minYPer = minIdx+self.barYMin
            perfectCenterY = (maxYPer[0]-minYPer[0])/2+minYPer[0]
            print("scan finised, minYPer:%d,maxYper:%d" %(minYPer[0], maxYPer[0]))    
            #ctrl anchor to the perfect
            startTime = time.time()
            gameOut = False
            while(~gameOut):
                res = pyautogui.locateOnScreen(self.anchorPath,region=self.fishGameBarRegion,confidence=0.7)
                if res:
                    anchorCenter = pyautogui.center(res)
                    anchorCenterY= anchorCenter[1]
                    print(anchorCenterY)
                    disTance = perfectCenterY-anchorCenterY
                    print('range = %d' %(disTance))
                    if disTance>=0:
                        print(strftime("%H:%M:%S", gmtime()), f"beyong perfect bar")
                    elif disTance<0 and disTance>=-20:
                        pyautogui.press(' ',1)
                        print(strftime("%H:%M:%S", gmtime()), f"press space 1 times")
                    else:
                        # manSimPressKey(' ')
                        pyautogui.press(' ',2)
                        print(strftime("%H:%M:%S", gmtime()), f"press space 2 times")
       
                else:
                    gameOut = True
                    break
                # time.sleep(0.01)    
        else:
            print(strftime("%H:%M:%S", gmtime()), f"fish mini game not found, exist")
            pyautogui.keyDown('esc')
            pyautogui.keyUp('esc')
            return
        
        if gameOut:
            print(strftime("%H:%M:%S", gmtime()), f"mini Game success !")
            time.sleep(5)
            
    
    def repairFishingRod_inHomeLand(self):
        '''
        Function with all steps to repair the fishing rod through the home land
        '''        
        print(strftime("%H:%M:%S", gmtime()), f"cast return home music.")
        
        pyautogui.keyDown(self.keybindings['homeReturnMusitc'])
        pyautogui.keyUp(self.keybindings['homeReturnMusitc'])
        startTime = time.time()
        while(1):
            #wait loding
            res = pyautogui.locateOnScreen(bot.inHomePath,confidence=0.9)
            if res:
                break
            else:
                curTime = time.time()
                if curTime-startTime>60:
                    print(strftime("%H:%M:%S", gmtime()), f"cast return home music failed.")
                    print(strftime("%H:%M:%S", gmtime()), f"recast return home music.")
                    pyautogui.keyDown(self.keybindings['homeReturnMusitc'])
                    pyautogui.keyUp(self.keybindings['homeReturnMusitc'])
                    startTime = time.time()                

        
        realManSim.manSimPressKey('g')
        time.sleep(1)
       
        # Small repair button offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on lifeToolsRepair.")
        realManSim.manSimLeftClick(self.lifeToolsRepair_x, self.lifeToolsRepair_y)
        realManSim.manSimWaitMedim()
        
        #多点击一次，skip掉秘书信息
        realManSim.manSimLeftClick(self.lifeToolsRepair_x, self.lifeToolsRepair_y)
        realManSim.manSimWaitMedim()
        
        time.sleep(1)
        # Repair All offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on Repair All button.")
        realManSim.manSimLeftClick(self.lifeToolsAll_x, self.lifeToolsAll_y)
        realManSim.manSimWaitMedim()

        realManSim.manSimLeftClick(self.lifeToolsAll_x, self.lifeToolsAll_y)
        realManSim.manSimWaitMedim()
        time.sleep(1)
        # Repair OK offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on OK button.")
        realManSim.manSimLeftClick(self.repairOK_x, self.repairOK_y)
        realManSim.manSimWaitMedim()

        # Press ESC
        print(strftime("%H:%M:%S", gmtime()), "Pressing ESC, closing repair window.")
        realManSim.manSimPressKey('esc')
        realManSim.manSimWaitMedim()
        
        # leave home land
        pyautogui.keyDown(self.keybindings['leaveMusic'])
        pyautogui.keyUp(self.keybindings['leaveMusic'])
        time.sleep(10)
        while(1):
            #wait loding
            res = pyautogui.locateOnScreen(bot.mainWindowIcon_path,confidence=0.9)
            if res:
                print(strftime("%H:%M:%S", gmtime()), "leave the Home success.")
                break
        time.sleep(3)

        realManSim.manSimWaitMedim()
        # move to pool
        print(strftime("%H:%M:%S", gmtime()), "mouse move to pool.")
        realManSim.manSimMoveTo(self.fishPool_x, self.fishPool_y)
        realManSim.manSimPressKey('b')

    
    def repairFishingRod(self):
        '''
        Function with all steps to repair the fishing rod through the pet inventory
        '''
        if self.keybindings['pet-inventory-modifier'] != None and self.keybindings['pet-inventory-modifier'] != '':
            print(strftime("%H:%M:%S", gmtime()), f"Opening pet inventory ({self.keybindings['pet-inventory-modifier'].upper()} + {self.keybindings['pet-inventory']}).")
            # Open pet inventory
            pyautogui.keyDown(self.keybindings['pet-inventory-modifier'])
            pyautogui.keyDown(self.keybindings['pet-inventory'])
            pyautogui.keyUp(self.keybindings['pet-inventory'])
            pyautogui.keyUp(self.keybindings['pet-inventory-modifier'])
        else:
            print(strftime("%H:%M:%S", gmtime()), f"Opening pet inventory ({self.keybindings['pet-inventory']}).")
            # Open pet inventory
            pyautogui.keyDown(self.keybindings['pet-inventory'])
            pyautogui.keyUp(self.keybindings['pet-inventory'])

        realManSim.manSimWaitMedim()

        # Small repair button offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on Pet Function: remote repair.")
        realManSim.manSimLeftClick(self.remoteRepair_x, self.remoteRepair_y)
        realManSim.manSimWaitMedim()

        # Repair All offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on Repair All button.")
        realManSim.manSimLeftClick(self.repairAll_x, self.repairAll_y)
        realManSim.manSimWaitMedim()

        # Repair OK offset
        print(strftime("%H:%M:%S", gmtime()), "Clicking on OK button.")
        realManSim.manSimLeftClick(self.repairOK_x, self.repairOK_y)
        realManSim.manSimWaitMedim()

        # Press ESC
        print(strftime("%H:%M:%S", gmtime()), "Pressing ESC, closing repair window.")
        realManSim.manSimPressKey('esc')
        realManSim.manSimWaitMedim()
        
        realManSim.manSimPressKey('esc')
        realManSim.manSimWaitMedim()
  
        # move to pool
        print(strftime("%H:%M:%S", gmtime()), "move to pool.")
        realManSim.manSimMoveTo(self.fishPool_x, self.fishPool_y)
        realManSim.manSimWaitMedim()
        
    def runFish(self):
        '''
        运行钓鱼程序
        '''
        counter = 1
        idletimer = 0
        flag = "pulled"
        # if needed, create your own template images
        template = cv2.imread(self.templatePath, 0)
        templateInStarBitch = cv2.imread(self.templateInStarBitchPath, 0)
        # poplavok = cv2.imread(self.poplavokPath, 0)
        
        print(strftime("%H:%M:%S", gmtime()), "Starting the bot in 3 seconds.")
        time.sleep(3)

        while(1):
            
            ## Repair if need
            res = pyautogui.locateOnScreen(self.needRepairPath,confidence=0.9)
            if  res:
                print(strftime("%H:%M:%S", gmtime()), f"Counter: {counter}. Repairing now.")
                if self.checkBeira():
                    self.repairFishingRod()
                else:
                    self.repairFishingRod_inHomeLand()
                    
                counter = counter + 1
                idletimer = 0
            
            
            idletimer = idletimer + 1
            if flag == "pulled":
                self.castFishingRod(counter)
                flag = "thrown"
                counter = counter + 1
                
            # screenshot creation
            image = pyautogui.screenshot(region=self.templateRegion)
            image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # search pattern on screen for exclamation point
            template_coordinates = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            loc = numpy.where( template_coordinates >= 0.6)

            templateStar_coordinates = cv2.matchTemplate(image, templateInStarBitch, cv2.TM_CCOEFF_NORMED)
            locStar = numpy.where( templateStar_coordinates >= 0.6)
            #debug
            # cv2.imshow('template', template)
            # cv2.imshow('image', image)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            # Based on the search results, either E is pressed or nothing happens and the cycle repeats
            if (len(loc[0]) > 0 or len(locStar[0]) > 0) and flag == "thrown":
                print(strftime("%H:%M:%S", gmtime()), "Found a fish.")
                idletimer = 0
                realManSim.manSimWaitShort()
                # Caught fish, press e ingame to reel it in
                realManSim.manSimPressKey(self.keybindings['fishing'])
                
                flag = "pulled"
                time.sleep(5)
                
                startTime = time.time()
                findGameReady = False
                while(~findGameReady):
                    res = pyautogui.locateOnScreen(self.fishGameReadyPath,region=self.fishGameReadyRegion,confidence=0.8)
                    if res:
                        print(strftime("%H:%M:%S", gmtime()), "fishGameReady pattern Found.")
                        findGameReady = True
                        break
                    else:
                        cutTime = time.time()
                        print(strftime("%H:%M:%S", gmtime()), f'fishGameReady pattern not Found:{cutTime-startTime:.1f}s')
                        if cutTime-startTime>self.fishGameWaitTime:
                            break
                    
                if findGameReady:
                    time.sleep(1)
                    self.playFishGame()   
                    
                realManSim.manSimWaitShort()

                
            # Repair if modulo 50 and either found a fish, or fully idle
            # if counter % 200 == 0 and (idletimer == 500 or flag == "pulled"):
            #     print(strftime("%H:%M:%S", gmtime()), f"Counter: {counter}. Repairing now.")
            #     repairFishingRod(screenWidth, screenHeight)
            #     counter = counter + 1
        
        

            # search pattern on screen for buoy
            # poplavok_coordinates = cv2.matchTemplate(image, poplavok, cv2.TM_CCOEFF_NORMED)
            # poplavok_loc = numpy.where( poplavok_coordinates >= 0.7)
            
            # if len(poplavok_loc[0]) == 0 and flag == "pulled":
            #     castFishingRod(counter)
            #     flag = "thrown"
            #     counter = counter + 1

            print(strftime("%H:%M:%S", gmtime()), f"Waiting for a fish. Idle timer: {idletimer}. Recast at 500.")

            if idletimer == 80:
                print(f"Idle timer reached 200. Recasting now.")
                idletimer = 0

                flag = "pulled"
            
                if flag == "pulled":
                    matchColor = pyautogui.pixelMatchesColor(self.vitXY[0],self.vitXY[1], self.emptyColor, tolerance=10) #检测指定位置是否指定颜色
                    if matchColor:
                        #exist 
                        pyautogui.hotkey('alt','f4')
                        print(strftime("%H:%M:%S", gmtime()), f"vit empty exist game.")
                        sys.exit(0)    

                # Recast
                self.castFishingRod(counter)
                flag = "thrown"
                counter = counter + 1
            
    def checkBeira(self):
        center = pyautogui.locateCenterOnScreen(self.beiraPath,region=self.beiraStatusRegion,confidence=0.9)
        pix = pyautogui.pixel(int(center[0]), int(center[1]))
        pix_HSV = colorsys.rgb_to_hsv(pix[0]/255,pix[1]/255,pix[2]/255)
        pix_H = int(pix_HSV[0]*255)
        # pix_cv2 = cv2.cvtColor(numpy.array([pix[0],pix[1],pix[2]]), 0)
        # pix_HSV = cv2.cvtColor(numpy.array([pix[0],pix[1],pix[2]]),cv2.COLOR_RGB2HSV)
        # res = pyautogui.pixelMatchesColor(int(center[0]), int(center[1]), self.beiraExistColor, tolerance=10)
        
        diff_H = abs(pix_H-self.beiraExistColor_H)
        colorsys
        if diff_H<5:
            print(f"Beira buff exist")
            return True
        else:
            print(f"Beira buff not exist")
            return False
            

##--------------- fishBot class End


##------------------ debug script------------------------------
if __name__ == '__main__':
    print("run fish Bot Only ......")
    windowObj = gameWindowLocate.gameWindow()
    windowObj.scanScreenAndLocate()
    bot = fishBot()
    bot.renewAllCoord(windowObj.topLeftX,windowObj.topLeftY)
    # 
    # time.sleep(2)
    # bot.repairFishingRod_inHomeLand()
    bot.runFish()
    # realManSim.manSimPressKey('b')
    # res = pyautogui.locateOnScreen(bot.inHomePath,confidence=0.9)
    # print(res)
    # bot.checkBeira()

    
    
    