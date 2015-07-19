# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple checker for mahjong: test if the cards makes a winning hand.
# class and function api


import re

class Card:
    """docstring for card"""
    def __init__(self, card, flag=False):
        super(Card, self).__init__()
        self.rank = int(re.search('[1-9]', card).group())
        self.suit = re.search('[mpsz]', card).group()
        self.flag = flag        

    def __str__(self):
        return str(self.rank) + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_flag(self):
        return self.flag

    def set_flag(self, flag):
        self.flag = flag

'''
# test Card class
card0 = Card('1m')
print(card0)
# end test
'''

class Mianzi(object):
    """docstring for Mianzi"""
    def __init__(self, card1, card2, card3):
        super(Mianzi, self).__init__()

        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.index = card1.rank

    def __str__(self):
        if self.isvalid():
            return str(self.card1) + str(self.card2) + str(self.card3) 
        else:
            return 'not valid!'

    def isvalid(self):
        if self.card1.suit == self.card2.suit and self.card1.suit == self.card3.suit:
            if self.card1.rank == self.card2.rank - 1 and self.card2.rank == self.card3.rank - 1:
                return True
            elif self.card1.rank == self.card2.rank and self.card1.rank == self.card3.rank:
                return True
        return False

'''
# test Mianzi class
mianzi1 = Mianzi(Card('1m'), Card('2m'), Card('3m'))
print(mianzi1)
print(mianzi1.isvalid())

mianzi2 = Mianzi(Card('3m'), Card('4m'), Card('6m'))
print(mianzi2.isvalid())
# end test
'''

class Quetou(object):
    """docstring for Quetou"""
    def __init__(self, card1, card2):
        super(Quetou, self).__init__()
        
        self.card1 = card1
        self.card2 = card2
        self.index = card1.rank
    def __str__(self):
        if self.isvalid():
            return str(self.card1) + str(self.card2) 
        else:
            return 'not valid!'
    def isvalid(self):
        if self.card1.suit == self.card2.suit and self.card1.rank == self.card2.rank:
            return True
        else:
            return False
'''
# test Quetou class
quetou1 = Quetou(Card('1m'), Card('1m'))
print(quetou1)
print(quetou1.isvalid())
quetou2 = Quetou(Card('5z'), Card('3z'))
print(quetou2)
print(quetou2.isvalid())
# end test
'''

VALID_LENGTH_OF_HAND = 14
MIANZI_MAX = 4
QUETOU_MAX = 1
finished_hand = []


# not for kanzhang now, 判断和牌暂时不包括坎张
def isdazi(card1, card2):
    if card1.suit == card2.suit:
        if card1.rank == card2.rank or card1.rank == card2.rank - 1:
            return True
    return False

'''
#test ismianzi, isquetou, isdazi
print('ismianzi', ismianzi(Card('1m'), Card('2m'), Card('3m')))
print('ismianzi', ismianzi(Card('1m'), Card('2m'), Card('4m')))
print('ismianzi', ismianzi(Card('1m'), Card('1m'), Card('1m')))
print('isquetou', isquetou(Card('1m'), Card('2m')))
print('isquetou', isquetou(Card('3z'), Card('3z')))
print('isdazi', isdazi(Card('1m'), Card('1m')))
print('isdazi', isdazi(Card('1m'), Card('2m')))
print('isdazi', isdazi(Card('1m'), Card('3m')))
'''

def hand_processer(raw_hand):
    # process raw hand to single card list
    hand = []
    # 1. separate hand
    for split in re.findall('[1-9]+[mpsz]', raw_hand): #valid number 1-9, valid suit mpsz
        suit = re.search('[mpsz]', split).group()
        ranks = re.findall('[1-9]', split)
        for rank in ranks:
            hand.append(rank + suit)
    # 2. sort first by suit, second by rank
    hand.sort(key=sort_hand)
    # 3. check if hand length is valid
    if len(hand) != VALID_LENGTH_OF_HAND:
        print('hand is not valid, please check')
        return None
    # 4. output by Card class
    hand_in_class = []
    for card in hand:
        hand_in_class.append(Card(card))

    return hand_in_class

def sort_hand(card):
    # reverse hand name to sort by suit first
    rank, suit = card
    return suit + rank

