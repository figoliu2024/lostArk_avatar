from __future__ import print_function
import heapq
import matplotlib.pyplot as plt
import unittest
import numpy
import cv2
import math
from PIL import Image

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
        
class aStar(object):
    stepSize = 2 #步进
    cast = 10*stepSize
    dataPath = f"resources/1080/data/"
    wallCheckStep = 1 #周围环境检查
    
    def __init__(self) -> None:
        '''
        初始化一些数据结构：堆、集合帮助实现算法
        '''
        self.closed = set()
        self.openlist = []
        heapq.heapify(self.openlist)
        self.cells = []
        self.binMapData = []
        self.grid_width = 0
        self.grid_height = 0
        
    def init_set(self):
        self.closed = set()
        self.openlist = []
        heapq.heapify(self.openlist)
    
    def init_grid(self):
        '''
        初始化地图，导入cells
        '''
        
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.binMapData[y][x] == 0:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(cell(x, y, reachable))
                
    def load_map(self, mapName):
        mapPath = self.dataPath+mapName+".txt"
        self.binMapData = numpy.genfromtxt(mapPath, dtype=int, delimiter=',')
        self.grid_height = numpy.size(self.binMapData,0)
        self.grid_width = numpy.size(self.binMapData,1)
        self.init_grid()
    
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
        
    def caculate_heuristic(self, cell):
        '''
        计算启发式距离h值，这里采用曼哈顿距离
        '''
        return 10 * ( abs(self.end.x - cell.x) + abs(self.end.y - cell.y) )
        
    def get_adjacent_cell(self, cell):
        '''
        返回cell周围的cell，这里的周围指八个方向
        '''
        stepSize = self.stepSize
        adj_cells = []
        for dx, dy in [ (stepSize, 0), (0, stepSize), (-stepSize, 0), (0, -stepSize), (stepSize, -stepSize), (-stepSize, stepSize), (-stepSize, -stepSize), (stepSize, stepSize) ]:
            x2 = cell.x + dx
            y2 = cell.y + dy
            if x2>=0 and x2<self.grid_width and y2>=0 and y2<self.grid_height: #地图范围内
                adj_cells.append(self.get_cell(x2,y2))

        return adj_cells
    
    def next_cell_aroundJudge(self, cell):
        '''
        检查新的cell附近是否有墙
        '''       
        wallCheckStep = self.wallCheckStep
        for dx, dy in [ (wallCheckStep, 0), (0, wallCheckStep), (-wallCheckStep, 0), (0, -wallCheckStep), (wallCheckStep, -wallCheckStep), (-wallCheckStep, wallCheckStep), (-wallCheckStep, -wallCheckStep), (wallCheckStep, wallCheckStep) ]:
            x2 = cell.x + dx
            y2 = cell.y + dy
            curCell = self.get_cell(x2,y2)
            if not curCell.isReachable:
                return False
        
        return True
    
    def get_updated(self, adj, cell):
        '''
        用于每次更新cell信息
        '''
        adj.g = cell.g + self.cast
        adj.parent = cell
        adj.h = self.caculate_heuristic(adj)
        adj.f = adj.g + adj.h
    
    def save_path(self, cell):
        '''
        保存计算路径
        '''
        # cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))
        path.append((self.start.x, self.start.y))
        path.reverse()
        return path
    
    
    def destReach(self, cell):
        if abs(self.end.x-cell.x)<=self.stepSize and abs(self.end.y-cell.y)<=self.stepSize:
            return True
        else:
            return False

    
    def solve(self):
        '''
        代码核心，实现逻辑
        '''
        self.init_set()
        
        if not(self.get_cell(self.end.x,self.end.y).isReachable):
            # raise RuntimeError("end point not reachable")
            print("end point not reachable")
            return -1

        heapq.heappush(self.openlist, (self.start.f, self.start))
        while len(self.openlist):
            f, cell = heapq.heappop(self.openlist)
            self.closed.add(cell)
            # if cell is self.end:
            if self.destReach(cell):
                return self.save_path(cell)
            
            adj_cells = self.get_adjacent_cell(cell)
            for adj_cell in adj_cells:
                if adj_cell.isReachable and adj_cell not in self.closed:
                    
                    # if self.next_cell_aroundJudge(adj_cell):
                    if ( adj_cell.f, adj_cell ) in self.openlist:
                        if adj_cell.g > cell.g + self.cast:
                            self.get_updated(adj_cell, cell)
                    else:
                        self.get_updated(adj_cell, cell)
                        heapq.heappush(self.openlist, ( adj_cell.f, adj_cell ))
                        
        # raise RuntimeError("A* failed to find a solution")
        print("A* failed to find a solution")


    def draw_result(self,result_path, mapName):
        mapPath = self.dataPath+mapName+".png"
        bigMap = Image.open(mapPath)
        bigMapCv2 = cv2.cvtColor(numpy.array(bigMap), 0)

        routeLen = len(result_path)
        # print(routeLen)
        for idx in range(routeLen-1):
            cv2.line(bigMapCv2,result_path[idx],result_path[idx+1],(0,255,0),2)#绿色，3个像素宽度

        cv2.namedWindow("routeResult", 0)
        cv2.resizeWindow("routeResult", 720,450)
        cv2.moveWindow("routeResult", 2000,800)
        cv2.imshow('routeResult', bigMapCv2)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

def drawMap(binMapData, h, w):
    route = []
    for x in range(w):
        for y in range(h):
            if binMapData[y][x] == 255:
                tmp=(y,x)
                route.append(tmp)
    
    routes = numpy.array(route)            
    
    plt.scatter(routes[:,1],routes[:,0], marker='.' , c='g')

    plt.title("route show", fontdict={'size': 20})
    plt.axis([0,w,h,0])
    plt.show()


# 产生二值化地图
def binMapGen(mapPath):
    bigMap = Image.open(mapPath)
    # bigMap = cv2.imread(mapPath, 1)
    bigMapCv2 = cv2.cvtColor(numpy.array(bigMap), 0)
    bigMapCv2 = cv2.cvtColor(bigMapCv2, cv2.COLOR_BGR2GRAY)
    wallCheckStep = 1
    # global thresholding

    ret2,th2 = cv2.threshold(bigMapCv2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # edges = cv2.Canny(bigMapCv2,100,200)
    
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

                        
    numpy.savetxt("resources/temp/地图-永恩起始之地.txt", binMap, fmt = '%d', delimiter = ',')
    cv2.imshow('gray', bigMapCv2)
    cv2.imshow('binMap', binMap)
    cv2.imshow('binMap', binMap)
    cv2.waitKey()
    cv2.destroyAllWindows()
    


if __name__ == '__main__':
    yongEnMapPath = f"resources/1080/data/地图-永恩起始之地.txt"
    yongEnPath = f"resources/1080/data/地图-永恩起始之地.png"
    binMapData = numpy.genfromtxt(yongEnMapPath, delimiter=',')
    # cv2.imshow(yongEnMapPath, binMapData)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # yongEnPath = f"resources/1080/data/地图-永恩起始之地.png"
    # print('地图数据二值化处理')
    # edgeMap = binMapGen(yongEnPath)
    

    # binMapData = numpy.genfromtxt(yongEnMapPath, dtype=int, delimiter=',')
    # h = numpy.size(binMapData,0)
    # w = numpy.size(binMapData,1)
    # drawMap(binMapData, h, w)
    
    a = aStar()
    a.load_map("地图-永恩起始之地")
    # a.init_grid(w, h, binMapData)
    a.caculate_one_way((370, 340), (430, 600))
    # a.caculate_one_way((318,501),(456, 487))
    path = a.solve()
    print(path)
    if path != None:
        a.draw_result(path,"地图-永恩起始之地")
    else:
        exit()
