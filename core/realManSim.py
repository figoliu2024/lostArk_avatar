import pyautogui
import time
import random
import pydirectinput

# function：sim real man press the keyboard2
def manSimPressKey(keyStr):
    pyautogui.keyDown(keyStr)
    time.sleep( random.uniform( 0.1, 0.3))
    pyautogui.keyUp(keyStr)
    
def manSimLeftClick(x,y):
    pyautogui.click(x, y, clicks=0, button='left')
    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.click(x, y, clicks=1, button='left')
    
def manSimRigthClick(x,y):
    # pyautogui.click(x, y, clicks=0, button='right')
    # time.sleep(random.uniform(0.01, 0.))
    pyautogui.click(x, y, clicks=1, button='right')


def manSimMoveAndLeftClick(x,y):
    manSimMoveTo(x,y)
    pyautogui.click(x, y, clicks=0, button='left')
    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.click(x, y, clicks=1, button='left')
    
def manSimMoveAndRightClick(x,y):
    manSimMoveTo(x,y)
    pyautogui.click(x, y, clicks=0, button='right')
    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.click(x, y, clicks=1, button='right')
    
    
#组合按键函数
def manSimMultiKey(downKey,pressKey):
    pydirectinput.keyDown(downKey)
    sleep(100, 200)
    pydirectinput.press(pressKey)
    sleep(100, 200)
    pydirectinput.keyUp(downKey)
    sleep(1000, 1200)


def leftClick_locatePic(picPath):
    # pyautogui.click(x, y, clicks=0, button='right')
    # time.sleep(random.uniform(0.01, 0.))
    center = pyautogui.locateCenterOnScreen(picPath,confidence=0.8)
    pyautogui.click(center)

    
def manSimWaitShort():
    time.sleep(random.uniform(0.01, 0.05))
    
def manSimWaitMedim():
    time.sleep(random.uniform(1.0, 1.5))
    
def manSimWaitlong():
    time.sleep(random.uniform(3.0, 5.0))
    
def manSimMoveTo(x,y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.01, 0.2))  
    
def sleep(min, max):
    sleepTime = random.randint(min, max) / 1000.0
    if sleepTime < 0:
        return
    time.sleep(sleepTime)