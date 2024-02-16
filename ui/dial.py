'''
实验名称：UI1
版本：v1.0
日期：2024.2
作者：shenzh
说明：极简时钟
'''

#导入相关模块
import time,math

import machine

from libs import global_var

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

def background():#画出表盘
    d.circle(80, 64, 60, 0x000000)
    for i in range(12):
        x0 = 80+round(60*math.sin(math.radians(i*30)))
        y0 = 64-round(60*math.cos(math.radians(i*30)))
        x1 = 80+round(50*math.sin(math.radians(i*30)))
        y1 = 64-round(50*math.cos(math.radians(i*30)))
        d.line(x0, y0, x1, y1, 0x000000)
    d.show()
    
def datetime_display(datetime):
    
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]
    
    #秒钟处理
    
    #清除上一帧
    x0 = 80+round(50*math.sin(math.radians(second*6-6)))
    y0 = 64-round(50*math.cos(math.radians(second*6-6)))
    d.line(x0, y0, 80, 64, 0xffffff)
    
    #显示
    x1 = 80+round(50*math.sin(math.radians(second*6)))
    y1 = 64-round(50*math.cos(math.radians(second*6)))
    d.line(x1, y1, 80, 64, 0x00ff00)
    
    #分钟处理
    
    #清除上一帧
    x0 = 80+round(40*math.sin(math.radians(minute*6-6)))
    y0 = 64-round(40*math.cos(math.radians(minute*6-6)))
    d.line(x0, y0, 80, 64, 0xffffff)
    
    #显示
    x1 = 80+round(40*math.sin(math.radians(minute*6)))
    y1 = 64-round(40*math.cos(math.radians(minute*6)))
    d.line(x1, y1, 80, 64, 0x00ff00)
        
    #时钟处理

    #清除上一帧
    x0 = 80+round(30*math.sin(math.radians(hour*30+int(minute/12)*6-6)))
    y0 = 64-round(30*math.cos(math.radians(hour*30+int(minute/12)*6-6)))
    d.line(x0, y0, 80, 64, 0xffffff)
    
    #显示
    x1 = 80+round(30*math.sin(math.radians(hour*30+int(minute/12)*6)))
    y1 = 64-round(30*math.cos(math.radians(hour*30+int(minute/12)*6)))
    d.line(x1, y1, 80, 64, 0x00ff00)

    d.show()

#显示图片
def UI_Display(datetime):

    if global_var.UI_Change: #首次画表盘
        
        global_var.UI_Change = 0        
        # d.fill(BLACK) #清屏
        d.fill(0xFFFFFF)
        time.sleep_ms(2000)
        background()

    
    datetime_display(datetime)