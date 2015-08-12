# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# autogui interface: for 国标v1.30

import pyautogui
import mahjong

pyautogui.PAUSE = 0 # 0.1 second pause after each call by pyautogui

def get_hand(debug=False):
    """获取手牌信息
    i:
    p: 截图-逐张寻找-添加, 时间大约1s, 每局一次, 因此目前可接受.
    o: 手牌列表
    """
    hand_image = pyautogui.screenshot(region=(119, 450, 323, 44)) 
        #截取手牌图, 国标ver1.30位于左上角时, 坐标 (118, 449). 
        #牌25, 46, 但只取23, 44
    hand = []
    for card in mahjong.CARD_LIST:
        card_position = pyautogui.locateAll('images\{}.png'.format(card), 
                                            hand_image, grayscale=True)
        num_card = len(list(card_position))
        if num_card:
            hand.append(card * num_card)
        if len(hand) == 13: # 如果已经到十三张, 说明已完成, 可提前结束.
            break
    if debug:
        print(''.join(hand))
    return ''.join(hand)

def get_card(debug=True):
    """获取新抓牌信息
    i:
    p: 截图-逐张寻找-匹配则输出
    o: 手牌列表
    """
    card_image = pyautogui.screenshot(region=(459, 450, 23, 44))
        # 国标ver1.30位于左上角, 这是准确值, 无任何余量
    for card in mahjong.CARD_LIST:
        card_position = pyautogui.locate('images\{}.png'.format(card), 
                                         card_image, grayscale=False)
        if card_position:
            if debug:
                print(card, card_position) #for debug
            return card

def qiepai(card_position):
    """切出指定位置的手牌

    i: 手牌位置 0-13: 暂时只支持门清, 摸切张要单独考虑位移
    p: 左起计算位置 - click
    """
    if card_position == 13: # 摸切
        mouse_position = (470, 472) # 459+11, 450+22, 大约是摸切中心
    else:
        mouse_position = (130 + 25 * card_position, 472)
    pyautogui.click(mouse_position)

def pass_mingpai():
    pyautogui.click(340, 272)

def main(): # 测试用
    print(get_hand())
    print(get_card())

if __name__ == '__main__':
    main()