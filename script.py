# import pyautogui
import pyautogui
import time
import xlrd
import pyperclip
import os

current_directory = os.path.dirname(os.path.abspath(__file__))


# 定义鼠标事件
# pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159

def mouseClick(clickTimes, lOrR, img, reTry):
    # 按指定次数查找
    if reTry >= 1:
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes,
                                interval=0.2, duration=0.2, button=lOrR)
                return
            print("未找到匹配图片 {}, {}次查找".format(img, i))
            i += 1
            time.sleep(1.5)
        quit()

    # 重复查找图片
    elif reTry == -1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes,
                                interval=0.2, duration=0.2, button=lOrR)
            print("未找到匹配图片 {}, 1秒后重试".format(img))
            time.sleep(1)


# 定义键盘事件

def keyboard(key, timer=1):
    time.sleep(timer)
    keyList = key.split('+')
    keyLength = len(keyList)

    if keyLength == 1:
        # 按下并松开（轻敲）回车键
        pyautogui.press(key)
    elif keyLength == 2:
        # 组合按键（Ctrl+V），粘贴功能，按下并松开'ctrl'和'v'按键
        pyautogui.hotkey(keyList[0], keyList[1]),
    elif keyLength == 3:
        pyautogui.hotkey(keyList[0], keyList[1], keyList[2])
    elif keyLength > 3:
        print('按键组合数量不能大于3')


# 数据检查
# cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮
# ctype     空：0
#           字符串：1
#           数字：2
#           日期：3
#           布尔：4
#           error：5

def dataCheck(sheet1):
    checkCmd = True
    # 行数检查
    if sheet1.nrows < 2:
        print("没数据啊哥")
        checkCmd = False
    # 每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or cmdType.value not in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
            print('第', i+1, "行,第1列数据有毛病")
            checkCmd = False
            break

        # 第2列 内容检查
        cmdValue = sheet1.row(i)[1]
        # 读图点击类型指令，内容必须为字符串类型
        if cmdType.value in [1.0, 2.0, 3.0]:
            if cmdValue.ctype != 1:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 输入类型，内容不能为空
        if cmdType.value == 4.0:
            if cmdValue.ctype == 0:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 等待类型，内容必须为数字
        if cmdType.value == 5.0:
            if cmdValue.ctype != 2:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 6.0:
            if cmdValue.ctype != 2:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False
        # 点击键盘指令，内容不能为空 keyboard
        if cmdType.value == 7.0:
            if cmdValue.ctype == 0:
                print('第', i+1, "行,第2列数据有毛病")
                checkCmd = False

        i += 1
    return checkCmd

# 任务
# 项目启动不是根目录的时候，可以拼接 current_directory+'\\'+img


def mainWork(img):
    i = 1
    while i < sheet1.nrows:
        # 取本行指令的操作类型
        cmdType = sheet1.row(i)[0]
        if cmdType.value == 1.0:
            # 取图片名称
            img = sheet1.row(i)[1].value
            reTry = 3
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1, "left", img, reTry)
            print("单击左键", img)
        # 2代表双击左键
        elif cmdType.value == 2.0:
            # 取图片名称
            img = sheet1.row(i)[1].value

            # 取重试次数
            reTry = 3
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(2, "left", img, reTry)
            print("双击左键", img)
        # 3代表右键
        elif cmdType.value == 3.0:
            # 取图片名称
            img = sheet1.row(i)[1].value
            # 取重试次数
            reTry = 3
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1, "right", img, reTry)
            print("右键", img)
        # 4代表输入
        elif cmdType.value == 4.0:
            inputValue = sheet1.row(i)[1].value
            pyperclip.copy(inputValue)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            print("输入:", inputValue)
        # 5代表等待
        elif cmdType.value == 5.0:
            # 取图片名称
            waitTime = sheet1.row(i)[1].value
            time.sleep(waitTime)
            print("等待", waitTime, "秒")
        # 6代表滚轮
        elif cmdType.value == 6.0:
            # 取滚动值
            scroll = sheet1.row(i)[1].value
            pyautogui.scroll(int(scroll))
            print("滚轮滑动", int(scroll), "距离")
        # 7代表键盘事件
        elif cmdType.value == 7.0:
            # 取按键值
            keyWorld = sheet1.row(i)[1].value
            print("键值", keyWorld)

            keyboard(keyWorld)
        i += 1


if __name__ == '__main__':
    # 打开文件
    # file = 'cmd.xls'
    # 注意：1.必须是 '.xls' 后缀的 excel；2.项目启动不是根目录的时候，需要使用绝对路径拼接
    file = current_directory+'\cmd.xls'
    wb = xlrd.open_workbook(filename=file)

    # 通过索引获取表格sheet页
    sheet1 = wb.sheet_by_index(0)
    print('begin~')
    # 数据检查
    checkCmd = dataCheck(sheet1)
    if checkCmd:
        key = input('选择功能: 1.做一次 2.循环到死 \n')
        if key == '1':
            # 循环拿出每一行指令
            mainWork(sheet1)
        elif key == '2':
            while True:
                mainWork(sheet1)
                time.sleep(0.1)
                print("等待0.1秒")
    else:
        print('输入有误或者已经退出!')
