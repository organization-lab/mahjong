# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple tester of checker for mahjong

import checker
from sys import argv

'''
# init card list
RANKS = range(1, 10)
SUITS = ['m', 'p', 's', 'z']
card_list = []
for suit in SUITS:
    for rank in RANKS:
        if suit is 'z': 
            #special for 1-7z
            if rank < 8:
                card_list.append(str(rank) + suit)
        else:
            card_list.append(str(rank) + suit)
'''
# alternative using list comprehensions
card_list = [str(rank) + suit 
             for suit in ['m', 'p', 's', 'z'] 
             for rank in range(1, 10) 
             if rank in range(1,8) or suit is not 'z']

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

def istingpai(hand, raw_hand=True, output_notes=True):
    """判断13张牌是否听牌

    i: 接受 raw_hand 和 Class hand

    """
    if raw_hand:
        hand = checker.hand_processer(hand, length=13, check_input=True)
    if hand:
        flag = False
        for card in card_list:
            hand_card = hand[:]
            hand_card.append(checker.Card(card))
            #for i in hand_card: # test
            #    print(i, end='') #test
            if checker.mahjong_checker(hand_card, output_notes=False, raw_hand=False):
                if output_notes:
                    print(card, end=' ')
                flag = True
        if flag:
            if output_notes:
                print()
            return True
        else:
            if output_notes:
                print('Not tingpai.')
            return False
    else:
        print('Wrong input!')
        return False

def totingpai_14(hand, raw_hand=True):
    """判断14张牌打掉哪张/哪些可以听牌

    """

    hand = checker.hand_processer(hand, raw_hand=raw_hand, length=14, check_input=True)
    flag = False
    for card in hand:
        hand_card = hand[:]
        hand_card.remove(card)
        if istingpai(hand_card, raw_hand=False, output_notes=False):
            #print('istingpai', card)
            flag = True
    if flag:
        return True
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
        for card in card_list:  
            #print(card)
            hand_card = hand[:]
            hand_card.append(checker.Card(card))
            if totingpai_14(hand_card, raw_hand=False):
                print(card, end=' ')
        print()

if __name__ == '__main__':

    #istingpai('1112345876999m')
    #istingpai(checker.hand_processer('1112345876999m'),raw_hand=False)

    #print(totingpai_14('11123456789999m'))
    #print(totingpai_14('123456789m12345p'))
    print(totingpai_14('1122556699m1223p'))
    print(totingpai_14('1122556699m1233p')) # issue here


    #isyixiangting('123456m1245789p')
    #isyixiangting('123456m1256699p')
    #isyixiangting('123456m1599p123s')
    isyixiangting('1122556699m132p')
    #main()
