import time
import win32gui, win32ui, win32con, win32api
import numpy as np
import matplotlib.pyplot as plt
import cv2
import datetime
import gc
import pyHook
import pythoncom
import multiprocessing

from common.check_bomb import find_can_bomb_point,check64
from common.img_process import classify_hist_with_split,cat_img
from common.game_action import *

# import the module
from pymouse import PyMouse
m = PyMouse()



    
hArr = [545,662,780,899,1018,1137,1253,1373]
vArr = [140,261,378,495,618,737,851,973]






#我方数组
leftList = [{
    "x":319,
    "y":189,
    "name":"huozhadan",
    "target":True,
    "castImg":None,
    "order":1
},{
    "x":319,
    "y":442,
    "name":"huozhadan",
    "target":True,
    "castImg":None,
    "order":2
},{
    "x":319,
    "y":699,
    "name":"taiyangniao",
    "target":True,
    "castImg":None,
    "order":3
},{
    "x":319,
    "y":952,
    "name":False,
    "target":True,
    "castImg":None,
    "order":4
}]
#权重数组
weightMap = {
    'w':6,
    'y':3,
    'g':2,
    'n':3,
    'p':5,
    'r':5,
    'b':4,
    0:0,
    None:0
}

init_left(leftList)



    
    
#移动一步
def moveOnce():
    #截屏
    imgPath = "game2.jpg"
    window_capture(imgPath)
    img = cv2.imread(imgPath)
    
    if check_prepare(img):
        #准备中
        return True
    elif check_fight(img):
        #战斗中
        check_right(img)
        if not is_all_right_dead(img):
            #敌方未全灭
            check_left(img)
            colorArr = check64(img,hArr,vArr)
            if not colorArr:
                return False
            moveInfo = find_can_bomb_point(colorArr,weightMap)
            if moveInfo:
                print("moveInfo",moveInfo)
                x1 = moveInfo["x1"]
                y1 = moveInfo["y1"]
                x2 = moveInfo["x2"]
                y2 = moveInfo["y2"]
                if moveInfo["weight"] <= 10 and moveInfo["color"]!="w":
                    
                    casting(2)
                    casting(0)
                    casting(1)
                    #casting(1)
                    
                    
                    
                    
                    
                    m.click(hArr[x1],vArr[y1])
                    time.sleep(0.1)
                
                mouse_drag(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                print(hArr[x1],vArr[y1],hArr[x2],vArr[y2])
                time.sleep(2)
            del moveInfo,colorArr
        else:
            print("敌方全灭")
    else:
        continue_click()
        
    del img,imgPath
    print ("\nbegin collect...")
    _unreachable = gc.collect()
    print ("unreachable object num:%d" ,(_unreachable))
    #print ("garbage object num:%d" ,(len(gc.garbage))   #gc.garbage是一个list对象，列表项是垃圾收集器发现的不可达（即垃圾对象）、但又不能释放(不可回收)的对象，通常gc.garbage中的对象是引用对象还中的对象。因Python不知用什么顺序来调用对象的__del__函数，导致对象始终存活在gc.garbage中，造成内存泄露 if __name__ == "__main__": test_gcleak()。如果知道一个安全次序，那么就可以打破引用焕，再执行del gc.garbage[:]从而清空垃圾对象列表

    
        
        



    

    






#window操作========================================================================================================
#鼠标拖拽
def mouse_drag(x,y,x2,y2):
    # instantiate an mouse object
    screen_size = m.screen_size()
    m.move(x, y)    #鼠标移动到  
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
    time.sleep(0.05)
    SW = screen_size[0]
    SH = screen_size[1]
    mw = int(x2 * 65535 / SW) 
    mh = int(y2 * 65535 / SH)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE + win32con.MOUSEEVENTF_MOVE, mw, mh, 0, 0)    
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
#截屏
def window_capture(filename):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
	#ReleaseDC函数
    #函数功能：函数释放设备上下文环境（DC）供其他应用程序使用。函数的效果与设备上下文环境类型有关。它只释放公用的和设备上下文环境，对于类或私有的则无数。
    #函数原型：int ReleaseDC(HWND hWnd, HDC hdc)；
    #参数：
    #hWnd：指向要释放的设备上下文环境所在的窗口的句柄。
    #hDC：指向要释放的设备上下文环境的句柄。
    #返回值：返回值说明了设备上下文环境是否释放；如果释放成功，则返回值为1；如果没有释放成功，则返回值为0。
    #注释：每次调用GetWindowDC和GetDC函数检索公用设备上下文环境之后，应用程序必须调用ReleaseDC函数来释放设备上下文环境。
    #应用程序不能调用ReleaseDC函数来释放由CreateDC函数创建的设备上下文环境，只能使用DeleteDC函数。
    win32gui.ReleaseDC(hwnd,hwndDC)

    


    

def worker(isLoop):
    while True:
        print("循环中",isLoop)
        if isLoop:
            print("loop循环中",isLoop)
            moveOnce()
        time.sleep(1)
        
        
mainProgress = None
def onKeyboardEvent(event):
    global isLoop
    global mainProgress
    # 监听键盘事件
    #最近使用PyUserInput的KeyboardEvent的时候遇到了KeyboardSwitch() missing 8的情况;
    #该问题具体表现在当你focus的那个进程的窗口title带中文, 就会出现上面那个错误, 如果都是英文或者其他ascii字符则不会;

    print ("MessageName:", event.MessageName)
    print ("Message:", event.Message)
    print ("Time:", event.Time)
    print ("Window:", event.Window)
    print ("WindowName:", event.WindowName)
    print ("Ascii:", event.Ascii, chr(event.Ascii))
    print ("Key:", event.Key)
    print ("KeyID:", event.KeyID)
    print ("ScanCode:", event.ScanCode)
    print ("Extended:", event.Extended)
    print ("Injected:", event.Injected)
    print ("Alt", event.Alt)
    print ("Transition", event.Transition)
    print ("---")
    
    if event.Key=="S":
        isLoop = True
        mainProgress = multiprocessing.Process(target = worker, args = (isLoop,))
        mainProgress.start()
        print("设置isLoop",isLoop)
    elif  event.Key=="F":
        print("mainProgress进程",mainProgress)
        if mainProgress:
            isLoop = False
            mainProgress.terminate()
            print("设置isLoop",isLoop)
        
    
    # 同鼠标事件监听函数的返回值df
    return True



def main():

    
    
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    
        
    # 进入循环，如不手动关闭，程序将一直处于监听状态dd
    pythoncom.PumpMessages()
    
    
    
    
    
  
if __name__ == "__main__":
    main()