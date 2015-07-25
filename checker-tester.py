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
    # issue: need to add a checker here.
    if checker.hand_processer(input_hand, length=13, check_input=True):
        flag = False
        for card in card_list:
            if checker.mahjong_checker(input_hand + card, output_notes=False):
                print(card, end=' ')
                flag = True
        if flag:
            print()
        else:
            print('Not tingpai.')
    else:
        print('Wrong input!')

if __name__ == '__main__':
    #test_cases()
    main()
