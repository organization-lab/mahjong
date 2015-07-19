# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple tester of checker for mahjong

import checker
from sys import argv

RANKS = range(1, 10)
SUITS = ['m', 'p', 's', 'z']

# init card list
card_list = []
for suit in SUITS:
    for rank in RANKS:
        if suit is 'z': #special for 1-7z
            if rank < 8:
                card_list.append(str(rank) + suit)
        else:
            card_list.append(str(rank) + suit)

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
    for card in card_list:
        if checker.mahjong_checker(input_hand + card, output_notes=False):
            print(card, end=' ')
    
if __name__ == '__main__':
    main()
