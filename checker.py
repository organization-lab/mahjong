# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple checker for mahjong: test if the cards makes a winning hand.


import re

test_hand = [('1m',0), ('2m',0), ('3m',0), 
            ('4p', 0), ('5p',0), ('6p', 0), 
            ('7s', 0), ('8s', 0), ('9s', 0), 
            ('1z', 0), ('1z', 0)]

class Card:
    """docstring for card"""
    def __init__(self, card):
        super(Card, self).__init__()
        self.rank = int(re.search('[1-9]', card).group())
        self.suit = re.search('[mpsz]', card).group()        

    def __str__(self):
        return str(self.rank) + self.suit

# test Card class
card0 = Card('1m')
print(card0)
# end test

class Mianzi(object):
    """docstring for Mianzi"""
    def __init__(self, card1, card2, card3):
        super(Mianzi, self).__init__()
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.index = card1.rank
    def __str__(self):
        return str(self.card1) + str(self.card2) + str(self.card3) + str(self.index)

# test Mianzi class
mianzi1 = Mianzi(Card('1m'), Card('2m'), Card('3m'))
print(mianzi1)
mianzi2 = Mianzi(Card('3m'), Card('4m'), Card('5m'))
print(mianzi2)
# end test

class Quetou(object):
    """docstring for Quetou"""
    def __init__(self, card1, card2):
        super(Quetou, self).__init__()
        self.card1 = card1
        self.card2 = card2
        self.index = card1.rank
    def __str__(self):
        return str(self.card1) + str(self.card2) + str(self.index)
# test Quetou class
quetou1 = Quetou(Card('1m'), Card('1m'))
print(quetou1)
quetou2 = Quetou(Card('5z'), Card('5z'))
print(quetou2)
# end test


#init test hand
hand = []
for i in test_hand:
    hand.append((Card(i[0]),i[1]))

def checker(hand):
    tempset = []
    for card, status in hand:
        print(card, status)
        if status == False:
            if test_set(tempset, card) != tempset: 
                tempset = test_set(tempset, card)
                status = True
            #print(tempset)
            if len(tempset) == 3: #finished set
                for i in tempset:
                    print(i, end=',')
                print()
                tempset = []

def test_set(tempset, card):
    if len(tempset) == 0: #no card added for set
        tempset.append(card)
    elif len(tempset) == 1 or len(tempset) == 2: #one/two card added
        if card.rank == tempset[- 1].rank + 1: #right card for straight
            tempset.append(card)
    return tempset

def ismianzi(card1, card2, card3):
    if card1.suit == card2.suit and card1.suit == card3.suit:
        if card1.rank == card2.rank - 1 and card2.rank == card3.rank - 1:
            return True
        elif card1.rank == card2.rank and card1.rank == card3.rank:
            return True
    return False


# checking if it is a pair
def isquetou(card1, card2):
    if card1.suit == card2.suit and card1.rank == card2.rank:
        return True
    else:
        return False

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

checker(hand)