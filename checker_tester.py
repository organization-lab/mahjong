# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple tester of checker for mahjong

import mahjong
from sys import argv

'''
# init card list
RANKS = range(1, 10)
SUITS = ['m', 'p', 's', 'z']
CARD_LIST = []
for suit in SUITS:
    for rank in RANKS:
        if suit is 'z': 
            #special for 1-7z
            if rank < 8:
                CARD_LIST.append(str(rank) + suit)
        else:
            CARD_LIST.append(str(rank) + suit)
'''
# alternative using list comprehensions
CARD_LIST = [str(rank) + suit 
             for suit in ['m', 'p', 's', 'z'] 
             for rank in range(1, 10) 
             if rank in range(1,8) or suit is not 'z']

def init_paishan():
    """ 生成136张牌山
    i: nothing
    o: a list of 136 random card
    """
    CARD_LIST = [str(rank) + suit 
             for suit in ['m', 'p', 's', 'z'] 
             for rank in range(1, 10) 
             if rank in range(1,8) or suit is not 'z']
    pass

def test_cases():
    cases_14 = ['11112345678999m', 
                '123456789m123p55s', 
                '11123m444567p789s',
                '1133557799m1133p', 
                '19m19p19s12345677z',
                '19m19p19s1234567z']
    for case in cases_14:
        checker.mahjong_checker(case)

def main():
    """return the one more card to make mahjong

    听牌判断, 输出所听牌张
    i: hand of 13 card
    o: all card (of 34 kinds) to make the hand mahjong
    """
    try:
        script, input_hand = argv
    except ValueError:
        input_hand = input('input hand of 13 card: ')
    istingpai(input_hand)

def istingpai(hand, raw_hand=False, output_notes=False):
    """判断13张牌是否听牌

    i: 接受 raw_hand 和 Class hand, 通过 raw_hand 变量指示
    """
    if raw_hand:
        hand = checker.hand_processer(hand, length=13, check_input=True)
    if hand:
        flag = False
        cardlist_of_tingpai = []
        for card in CARD_LIST:
            hand_card = hand + [checker.Card(card)]
            hand_card = checker.hand_processer(hand_card, raw_hand=False) #sort again
            if checker.mahjong_checker(hand_card, output_notes=False, raw_hand=False):
                if output_notes:
                    print(card, end=' ')
                cardlist_of_tingpai.append(card)
                flag = True
        if flag:
            if output_notes:
                print()
            return cardlist_of_tingpai
        else:
            if output_notes:
                print('Not tingpai.')
            return False
    else:
        print('Wrong input!')
        return False

def totingpai_14(hand, raw_hand=False, output_notes=False):
    """判断14张牌打掉哪张/哪些可以听牌

    """
    hand = checker.hand_processer(hand, raw_hand=raw_hand, length=14, check_input=True)
    flag = False # flag 用来标记是否已经听牌
    totingpai_list = []
    for card in hand:
        hand_card = hand[:]
        hand_card.remove(card) 
        tingpai_list = istingpai(hand_card, raw_hand=False, output_notes=False)
        if istingpai(hand_card, raw_hand=False, output_notes=False):
            totingpai_list.append(card)
            if output_notes:
                print('打 {} 听'.format(card), end=' ')
                for i in tingpai_list:
                    print(i, end=' ')
                print()
            flag = True
    if flag:
        return totingpai_list # 返回能听牌的列表
    else:
        return False

def isyixiangting(hand, raw_hand=True):
    """判断13张牌是否是一向听

    """
    hand = checker.hand_processer(hand, raw_hand=raw_hand, length=13, check_input=True)

    if istingpai(hand, raw_hand=False, output_notes=False): #已经听牌, 直接返回
        print('is tingpai')
        return False
    else: # 还没听牌
        for card in CARD_LIST: 
            hand_card = hand[:]
            hand_card.append(checker.Card(card))
            if totingpai_14(hand_card, raw_hand=False, output_notes=False):
                print(card, end=' ')
        print()

if __name__ == '__main__':

    #istingpai('1122556699m133p')
    #istingpai(checker.hand_processer('1112345876999m'),raw_hand=False)

    """
    print(totingpai_14('1112345678999m1s'))
    print(totingpai_14('123456789m12345p'))
    print(totingpai_14('1122556699m1223p'))
    print(totingpai_14('1122556699m1233p')) 
    print(totingpai_14('123456789m1278p5s'))
    print(totingpai_14('11123456789999m'))
    """

    isyixiangting('123456m1245789p')
    #isyixiangting('123456m1256699p')
    #isyixiangting('123456m1599p123s')
    #isyixiangting('1122556699m132p')
    #isyixiangting('19m19p123456777z')
    #main()
