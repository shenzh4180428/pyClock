from machine import SPI, Pin, I2C
from libs import st7735_buf,ahtx0
from libs.easydisplay import EasyDisplay



########################
# 构建1.8寸LCD对象并初始化
########################

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(13), mosi=Pin(12))
dp = st7735_buf.ST7735(width=128, height=160, spi=spi, cs=9, dc=10, res=11, rotate=1, bl=46, invert=False, rgb=False)

global LCD
LCD = EasyDisplay(display=dp, font="/data/Fonts/text_lite_16px_2312.v3.bmf", show=False, color=0xFFFF, clear=False,color_type="RGB565")#show的参数必须设置为False，可以避免屏闪的问题

i2c = I2C(1, scl=Pin(17), sda=Pin(18))  # 默认I2C1是17和18Pin
global AHT
AHT = ahtx0.AHT20(i2c)

global UI_Change
UI_Change = 1