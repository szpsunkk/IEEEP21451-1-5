#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont
from screen import getInformation,initText,drawText,showText
from server_plc import read_plc,ReadTemperature_humidity,pow

RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)


# default code

# init the setting

draw, image, disp,Font = initText()

#draw, image, disp = drawText("00_00", 50,70,Font[2],draw, image, disp)
value = read_plc(0x83, 6, 1)
val = pow(value)
val =  char(val)
val_tem = ReadTemperature_humidity(1)
val_hum = ReadTemperature_humidity(2)
#showText(draw, image,disp)
#time.sleep(30)
### add text in (X,Y) which font is Font(1).
flag = True
draw, image, disp = drawText(u"当前楼层：",20,40,Font[0],draw,image,disp)

draw, image, disp = drawText(val,160,40,Font[0],draw,image,disp)
draw, image, disp = drawText(u"当前温度：",20,80,Font[0],draw,image,disp)
draw, image, disp = drawText("33",160,80,Font[0],draw,image,disp)
draw, image, disp = drawText(u"当前湿度：",20,120,Font[0],draw,image,disp)
draw, image, disp = drawText("22",160,120,Font[0],draw,image,disp)


while(flag):
    text, X, Y= getInformation()
    #for i in range(len(X)):
    #    draw, image, disp = drawText((text[i] ,X[i],Y[i],Font[1],draw, image, disp)
    #draw,image, disp = drawText("123123123",80,80,Font[1],draw,image,disp)
    
    for i in range(len(X)):
        draw, image, disp = drawText(text[i],X[i],Y[i],Font[0],draw,image,disp)
    

    showText(draw, image, disp)
    #draw, image, disp = drawText("7843454",30,30,Font[0],draw,image,disp)
    #showText(draw, image, disp)
    print("yoo")
    flag = False
    #time.sleep(10)


