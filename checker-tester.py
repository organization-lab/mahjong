# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple tester of checker for mahjong

import checker

RANKS = range(1, 10)
SUITS = ['m', 'p', 's', 'z']

# init cards

card_list = []
for suit in SUITS:
    for rank in RANKS:
        if suit is 'z': #special for 1-7z
            if rank < 8:
                card_list.append(str(rank) + suit)
        else:
            card_list.append(str(rank) + suit)
print(card_list)

if __name__ == '__main__':
    for card in card_list:
        if checker.mahjong_checker('123456789m2333s' + card, output_notes=False):
            print(card, end=' ')