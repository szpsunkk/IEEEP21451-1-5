#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch4
from PIL import Image, ImageDraw, ImageFont

RST = 27
DC= 25
BL = 18
bus = 0
device = 0 

logging.basicConfig(level= logging.DEBUG)

"""
try:
    disp = LCD_2inch4.LCD_2inch4()
    disp.Init()
    disp.clear()
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    logging.info("line")
    #time.sleep(3)

    logging.info("rectangle")
    #draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
    
    image = Image.open('../pic/LCD_2inch4.jpg') 
    image = image.rotate(0)
    disp.ShowImage(image)
    time.sleep(1)
    
    logging.info("weixue")
    Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    text= "IEEE1451-1-5"
    draw.text((5, 200),text, fill = "BLUE",font=Font1)
    logging.info("111")
    #time.sleep(3)
    disp.ShowImage(image1)
    time.sleep(30)
except IOError as e:
    logging.info(e)



"""



def initText():
    
    """
    Output the text.

    inputText: the text
    locationX: the X coordinate of the text
    locationY: the Y coordinate of the text
    """


    disp = LCD_2inch4.LCD_2inch4()
    disp.Init()
    disp.clear()
    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    logging.info("draw text")


    Font0 = ImageFont.truetype("../Font/Font00.ttf",30)
    Font1 = ImageFont.truetype("../Font/Font01.ttf",30)
    Font2 = ImageFont.truetype("../Font/Font02.ttf",30)
    
    Font = []
    Font.append(Font0)
    Font.append(Font1)
    Font.append(Font2)
    #draw.text((10,18), "IEEE1451-1-5 NCAP Information",fill = "BLACK",font = Font1)
    
    #draw.text((10,50), u"总电梯台数:",fill = "BLACK",font = Font0)
    #draw.text((110,50), "100",fill = "BLACK",font = Font0)
    #draw.text((10,70), u"当前电梯台数:",fill = "BLACK",font = Font0)
    #draw.text((110,70), u"80",fill = "BLACK",font = Font0)
    #Font = "Font"+str(font) 
   # draw.text((locationX,locationY),inputText, fill = "BLACK", font =Font0 )

    return draw,image,disp,Font


def drawText(inputText,X,Y,font,draw, image, disp):
    draw.text((X,Y), inputText, fill= "BLACK",font = font)

    return draw, image, disp

def showText(draw,image,disp):
    image = image.rotate(180)
    disp.ShowImage(image)
    #time.sleep(300)
    disp.module_exit()
    logging.info("continue:")

def getInformation():

    #draw, image, disp, Font = initText()
    """
    itemText = input("input the text:")
    text = itemText.split(",")
    itemX = input("input the X:")
    x = itemX.split(",")
    X = [eval(i) for i in x]
    itemY = input("input the Y:")
    y = itemY.split(",")
    Y = [eval(i) for i in y]
    #text = ["hello","world"]
    #X = [11,22]
    #Y = [33,55]
    return text,X,Y
    """

    text = ["IEEE1451-1-5"]
    return text,[20],[1]
if __name__ == "__main__":
    draw, image, disp, Font = displayText()
    draw, image, disp = drawText("HELLO",70,70,Font[0],draw, image, disp)
    showImage(draw,image,disp)
    print("yoo!")



