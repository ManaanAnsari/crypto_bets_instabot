#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 14:29:43 2021

@author: li
"""


from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os
from insta_upload import upload_post
from cloud_api import upload_signal,delete_signals

# makes an image
def make_signal_image(market,tp,sl,BTCETH='BTC'):
    FONT_USER_INFO = ImageFont.truetype("./arial.ttf", 90, encoding="utf-8")
    FONT_TEXT = ImageFont.truetype("./arial.ttf", 110, encoding="utf-8")
    WIDTH = 2376
    HEIGHT = 2024
    COLOR_BG = 'white'
    COLOR_NAME = 'black'
    COLOR_TAG = (64, 64, 64)
    COLOR_TEXT = 'black'
    COORD_PHOTO = (250, 200)
    COORD_NAME = (600, 185)
    COORD_TAG = (600, 305)
    COORD_TEXT = (250, 510)
    LINE_MARGIN = 15
    
    user_name = "Binance Signal"
    user_tag = "@crypto_bets_"
    text = " Long Signal \n Buy Binance "+BTCETH+"/USDT Fut @ "+str(market)+" \n target: "+str(tp)+" \n stoploss: "+str(sl)
    img_name = "signal"
    
    text_string_lines = wrap(text, 37)
    text_string_lines = text.split("\n")
    
    x = COORD_TEXT[0]
    y = COORD_TEXT[1]
    
    temp_img = Image.new('RGB', (0, 0))
    temp_img_draw_interf = ImageDraw.Draw(temp_img)
    line_height = [
       temp_img_draw_interf.textsize(
           text_string_lines[i],
           font=FONT_TEXT
       )[1]
       for i in range(len(text_string_lines))
    ]
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    draw_interf = ImageDraw.Draw(img)

    draw_interf.text(COORD_NAME, user_name, font=FONT_USER_INFO, fill=COLOR_NAME)
    draw_interf.text(COORD_TAG, user_tag, font=FONT_USER_INFO, fill=COLOR_TAG)
    
    for index, line in enumerate(text_string_lines):
        draw_interf.text((x, y), line, font=FONT_TEXT, fill=COLOR_TEXT) 
        y += line_height[index] + LINE_MARGIN
    
    user_photo = Image.open('./temp.png', 'r').convert('RGBA')
    img.paste(user_photo, COORD_PHOTO, mask=user_photo)
    
    img.save(f'./{img_name}.jpg')
    return True


def delete_signal_local(filename="./signal.jpg"):
    if os.path.exists(filename):
        os.remove(filename)


def notify_insta(market,BTCETH='BTC'):
    if market and market >1:
        market = int(market)
        tp = int(market + market*0.015)
        sl = int(market - market*0.01)
        try:
            if make_signal_image(market,tp,sl,BTCETH):
                # return
                url = upload_signal()
                if url:
                    print(url)
                    upload_post(url)
                    delete_signals()
                    delete_signal_local()
                    return True
        except Exception as e :
            print(e)
            return False
