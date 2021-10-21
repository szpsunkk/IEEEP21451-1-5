import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
from screen import initText,drawText,showText

RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)


# default code

# init the setting

draw, image, disp,Font = initText()

### add text in (X,Y) which font is Font(1).

draw, image, disp = drawText("TT_TT", 50,50,Font[1],draw, image, disp)

draw, image, disp = drawText("00_00", 50,70,Font[2],draw, image, disp)

#show the text
showText(draw, image,disp)

print("yoo")



