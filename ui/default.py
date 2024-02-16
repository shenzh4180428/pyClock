'''
版本：v1.0
日期：2024.2
作者：shenzh
说明：天气时钟信息
分辨率：128*160
'''

#导入相关模块
import gc
from libs import global_var

#动态信息显示
message_num = 0

########################
# 构建1.5寸LCD对象并初始化
########################
d = global_var.LCD
# d = tftlcd.LCD15(portrait=1)

aht=global_var.AHT

#定义常用颜色
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
BLACK = 0x0000
WHITE= 0xFFFF
YELLOW = 0xFFE0
DEEPGREEN =0x01b369

#空气质量颜色
YOU = 0x9cca7f #优
LIANG = 0xf9da65 #良
QINGDU = 0xf29f39 #轻度
ZHONGDU = 0xdb555e #中度
ZDU = 0xba3779 #重度
YANZHONG = 0x880b20 #严重

week_list=['一','二','三','四','五','六','日']

air_quality=['优','良','轻度','中度','重度','严重']

'''
weather[9]:
[0]当日天气,[1]当日最高温,[2]当日最低温,[3]实时天气,[4]实时空气质量,[5]实时风向,[6]实时风力级数,[7]实时温度,[8]实时湿度,
'''    
def weather_display(city,weather):
   
    try:
        
        #城市信息,名称超出4个只显示前4个
        if len(city[0])<5:
            d.text(city[0],15-(len(city[0])-2)*10,8,size=16)

        else:
            d.text(city[0][:4],5,7)

    except:

        #如果城市中文无法显示，那么就显示城市编码。
        d.text(city[1],5, 7)

    #空气质量
    #优[0-50],良[50-100],轻度[100-150],中度[150-200],重度[200-300],严重[300-500]
    try:
        if 0 <= int(weather[4]) < 50: #优
            d.fill_rect(60, 5, 50, 24, YOU)
            d.text('优', 78, 9, bg_color=YOU)

        elif 50 <= int(weather[4]) < 100:#良
            d.fill_rect(60, 5, 50,  24, LIANG)
            d.text('良',78,9,bg_color=LIANG)

        elif 100 <= int(weather[4]) < 150:#轻度
            d.fill_rect(60, 5, 50, 24, QINGDU)
            d.text('轻度', 78, 9, bg_color=QINGDU)

        elif 150 <= int(weather[4]) < 200:#中度
            d.fill_rect(60, 5, 50, 24, ZHONGDU)
            d.text('中度', 78, 9, bg_color=ZHONGDU)

        elif 200 <= int(weather[4]) < 300:#重度
            d.fill_rect(60, 5, 50, 24, ZDU)
            d.text('重度', 78, 9, bg_color=ZDU)

        elif 300 <= int(weather[4]) <= 500:#严重
            d.fill_rect(60, 5, 50, 24, YANZHONG)
            d.text('严重', 78, 9, bg_color=YANZHONG)
    except:
        print("No air quality data!")



    #实时温度
    tmp = round(aht.temperature, 1)
    d.bmp("/data/picture/default/temp.bmp",5,90)
    d.rect(30, 92, 48, 10, WHITE)
    d.fill_rect(31, 93, int(tmp/50*48), 8, RED)
    #d.text('   ', 100, 177) #消除重影
    d.text(str(tmp), 80, 88, color=RED)
    d.text('℃',115,88,color=WHITE)



    #实时湿度
    humidity = round(aht.relative_humidity,1)
    d.bmp("/data/picture/default/humi.bmp",5,110)
    d.rect(30, 112, 48, 10, WHITE)
    d.fill_rect(31, 113, int(humidity/100*48), 8, DEEPGREEN)
    if humidity == 100:
        d.text(str(humidity), 88, 108, DEEPGREEN)
        print(humidity)
    else:
        #d.text('   ', 100, 100, BLACK) #消除100%的重影
        d.fill_rect(80,108,50,30,BLACK)
        d.text(str(humidity), 80, 108, DEEPGREEN)
    d.text('%',115,108,color=WHITE)

def message_display(weather,datetime):

    global message_num

    #实时天气
    if message_num == 0:
        #d.text('       ',5,40,color=0x000000,size=16) #清除显示残留
        d.fill_rect(5, 40, 155, 20, BLACK)  # 清除显示残留
        if len(weather[3]) < 5:  # 4个字以内
            d.text('实时天气 ', 5, 40, color=WHITE, size=16)
            d.text(weather[3], 160 - len(weather[3]) * 16, 40, color=WHITE, size=16)
        elif len(weather[3]) < 8:  # 7个字以内
            d.text(weather[3], 160 - len(weather[3]) * 16, 40, color=WHITE, size=16)
        else:  # 8个字以上,显示前7个
            d.text(weather[3][:7], 5, 40, color=WHITE, size=16)

        if weather[3] == '晴':
            if  7 <= datetime[4] < 19: #白天7点~19点
                d.bmp("/data/picture/default/weather/qing.bmp",120,2)
            else:
                d.bmp("/data/picture/default/weather/qing_night.bmp",120,2)

        elif weather[3] == '阴':
            if  7 <= datetime[4] < 19: #白天7点~19点
                d.bmp("/data/picture/default/weather/yin.bmp",120,2)
            else:
                d.bmp("/data/picture/default/weather/yin_night.bmp",120,2)

        elif weather[3] == '多云':
            d.bmp("/data/picture/default/weather/duoyun.bmp",120,2)

        elif weather[3] == '小雨':
            d.bmp("/data/picture/default/weather/xiaoyu.bmp",120,2)

        elif weather[3] == '中雨':
            d.bmp("/data/picture/default/weather/zhongyu.bmp",120,2)

        elif weather[3] == '大雨':
            d.bmp("/data/picture/default/weather/dayu.bmp",120,2)

        elif weather[3] == '暴雨':
            d.bmp("/data/picture/default/weather/dayu.bmp",120,2)

        elif weather[3] == '雷阵雨':
            d.bmp("/data/picture/default/weather/dayu.bmp",120,2)

        elif weather[3] == '阵雨':
            d.bmp("/data/picture/default/weather/zhongyu.bmp",120,2)

        elif weather[3] == '雾':
            d.bmp("/data/picture/default/weather/wu.bmp",120,2)

        elif weather[3] == '雨夹雪':
            d.bmp("/data/picture/default/weather/yujiaxue.bmp",120,2)

        elif weather[3] == '小雪':
            d.bmp("/data/picture/default/weather/xiaoxue.bmp",120,2)

        elif weather[3] == '中雪':
            d.bmp("/data/picture/default/weather/daxue.bmp",120,2)

        elif weather[3] == '大雪':
            d.bmp("/data/picture/default/weather/daxue.bmp",120,2)

        elif weather[3] == '扬沙':
            d.bmp("/data/picture/default/weather/sand.bmp",120,2)

        elif weather[3] == '浮尘':
            d.bmp("/data/picture/default/weather/sand.bmp",120,2)

        elif weather[3] == '沙尘暴':
            d.bmp("/data/picture/default/weather/sand.bmp",120,2)

        else: #未知天气
            d.bmp("/data/picture/default/weather/no.bmp",120,2)

    #今天天气
    elif message_num == 1:
        d.fill_rect(5,40,155,20,BLACK)#清除显示残留
        if len(weather[0])<5: #4个字以内
            d.text('今天天气 ',5,40,color=WHITE,size=16)
            d.text(weather[0], 160-len(weather[0])*16, 40, color=WHITE, size=16)
        elif len(weather[0])<8: #7个字以内
            d.text(weather[0],160-len(weather[0])*16,40,color=WHITE,size=16)
        else:#8个字以上,显示前7个
            d.text(weather[0][:7],5,40,color=WHITE,size=16)
    #风向
    elif message_num == 2:
        #d.text('       ',5,40,color=BLACK,bg_color=BLACK,size=16) #清除显示残留
        d.fill_rect(5, 40, 155, 20, BLACK)
        if '无' in weather[5]: #无持续风向

            d.text(weather[5],30,40,color=WHITE,size=16)

        else: #有风向

            d.text(weather[5],30,40,color=WHITE,size=16)
            d.text(weather[6],110, 40, color=WHITE, size=16)
            d.text('级',125,40,color=WHITE,size=16)

    #最低温度
    elif message_num == 3:
        #d.text('       ',5,40,color=WHITE,bg_color=0xffffff,size=16) #清除显示残留
        d.fill_rect(5, 40, 155, 20, BLACK)
        d.text('最低温度 ',5,40,color=WHITE,bg_color=BLACK,size=16)
        d.text(weather[1], 140-len(weather[1])*10, 40, color=WHITE, size=16)
        d.text('℃',148,40,color=WHITE,size=16)

    #最高温度
    elif message_num == 4:
        #d.text('       ',5,40,color=WHITE,size=16) #清除显示残留
        d.fill_rect(5, 40, 155, 20, BLACK)
        d.text('最高温度 ',5,40,color=WHITE,size=16)
        d.text(weather[2], 140-len(weather[2])*10, 40, color=WHITE, size=16)
        d.text('℃',148,40,color=WHITE,size=16)

    #动态信息显示选择
    message_num = message_num + 1
    if message_num == 5:
        message_num = 0

#全局做了清屏，此处不需要再做特殊处理
#月，日显示重影标志位
# month_node = 0
# day_node = 0

def datetime_display(datetime):

    #日期显示
    year = datetime[0]
    month = datetime[1]
    day = datetime[2]
    week = datetime[3]

    global month_node,day_node #月，日显示重影标志位
    d.fill_rect(0, 59, 160, 20, BLACK)
    #月显示
    if month > 9:
        d.text(str(month), 0, 59, color=WHITE, size=16)
        # month_node = 1
    else:
        #全局做了清屏，此处不需要再做特殊处理
        # if month_node == 1: #月份从双位数变换到单位数
        #     d.text('  ', 0, 59, color=WHITE, size=16) #消除月显示重影
        #     month_node = 0

        d.text(str(month), 8, 59, color=WHITE, size=16)

    d.text('月',18,60,color=WHITE,size=16)

    #日显示
    if day > 9:
        d.text(str(day), 33, 59, color=WHITE, size=16)
        # day_node = 1

    else:
        # 全局做了清屏，此处不需要再做特殊处理
        # if day_node == 1: #日从双位数变换到单位数
        #     d.text('  ', 33, 59, color=WHITE, size=16) #消除日显示重影
        #     day_node = 0

        d.text(str(day), 41, 59, color=WHITE, size=16)

    d.text('日',50,60,color=WHITE,size=16)

    #周显示
    d.text('周'+week_list[week],68,60,color=WHITE,size=16)
    
    #时间显示
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]


    if hour > 9:
        d.text(str(hour), 99, 59, size=16)
    else:
        d.text('0'+str(hour), 99, 59, size=16)

    d.text(':', 114, 59, size=16)

    if minute > 9:
        d.text(str(minute), 121, 59, size=16)
    else:
        d.text('0'+str(minute), 121, 59, size=16)

    d.text(':', 137, 59, size=16)

    if second > 9:
        d.text(str(second), 144, 59, size=16)
    else:
        d.text('0'+str(second), 144, 59, size=16)
    d.show()

#用于显示动画
second2 = 61

#显示图片
def UI_Display(city,weather,datetime):
    
    global second2,message_num
    
    if global_var.UI_Change: #首次显示
        
        global_var.UI_Change = 0
        message_num = 0
        
        d.fill(0) #清屏
        weather_display(city,weather)
        message_display(weather,datetime)

    datetime_display(datetime)

    #logo动态显示
    if second2 != datetime[6]:
        if gc.mem_free() < 15000: #内存不足
            gc.collect() #回收内存
        d.bmp("/data/picture/default/"+str(datetime[6]%4+1)+".bmp",130,88)
        second2 = datetime[6]
        
    #动态信息显示刷新时间5秒
    if datetime[6]%5 == 0: 
        
        message_display(weather,datetime)
    
    #天气信息显示刷新时间10分钟
    if datetime[5]%10 == 0 and datetime[6]==0:
        
        weather_display(city,weather)
