'''
实验名称：相册
版本：v1.0
日期：2024.2
作者：shenzh
说明：相册幻灯片。图片尺寸160*128，BMP文件放到 /data/picture/photo_album/ 目录下。
'''

#导入相关模块
import time,os
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

picture_list = []
picture_num = 0

#显示图片
def UI_Display(datetime):
    
    global picture_num,picture_list
    
    if global_var.UI_Change: #首次画表盘
        
        global_var.UI_Change = 0        
        d.fill(0) #清屏
        
        picture_list = os.listdir("/data/picture/photo_album/") #获取所有图片信息
        d.bmp("/data/picture/photo_album/"+picture_list[0],0,0)
        d.show()
    
    #相册照片刷新新时间10秒
    if datetime[6]%10 == 0:
        
        picture_num = picture_num + 1
        
        if picture_num == len(picture_list):
            
            picture_num =0
            
        d.bmp("/data/picture/photo_album/"+picture_list[picture_num],0,0)
        d.show()
        

        

        

        
        
        