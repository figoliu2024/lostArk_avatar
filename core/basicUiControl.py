import pyautogui
from core import realManSim



class basicUiCtrl(object):
    def __init__(self,UiRegions,UiCoordi) -> None:
        self.UiRegions = UiRegions
        self.UiCoordi = UiCoordi

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
        
        
# ## Test bench 
if __name__ == "__main__":
    print("start basicUiCtrl Test")
    