# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple checker for mahjong: test if the cards makes a winning hand.


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
        return str(self.card1) + str(self.card2) + str(self.card3) + str(self.index)

'''
# test Mianzi class
mianzi1 = Mianzi(Card('1m'), Card('2m'), Card('3m'))
print(mianzi1)
mianzi2 = Mianzi(Card('3m'), Card('4m'), Card('5m'))
print(mianzi2)
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
        return str(self.card1) + str(self.card2) + str(self.index)

'''
# test Quetou class
quetou1 = Quetou(Card('1m'), Card('1m'))
print(quetou1)
quetou2 = Quetou(Card('5z'), Card('5z'))
print(quetou2)
# end test
'''

MIANZI_MAX = 4
QUETOU_MAX = 1

def checker(raw_hand):
    # change raw hand to Card hand
    hand = []
    for card in raw_hand:
        hand.append(Card(card))

    tempset = []
    i = 0
    j = i + 1
    k = j + 1
    while i < len(hand): # i.e. 14
        if hand[i].get_flag() == True:
            i += 1
        else:
            j = i + 1
            while j < len(hand) and k < len(hand):
                if hand[j].get_flag() == True:
                    j += 1
                else:
                    k = j + 1
                    if isdazi(hand[i], hand[j]):
                        print(hand[i].get_rank(), hand[j].get_rank())
                        while k < len(hand):
                            if ismianzi(hand[i], hand[j], hand[k]):
                                tempset.append(Mianzi(hand[i], hand[j], hand[k]))
                                hand[i].set_flag(True)
                                hand[j].set_flag(True)
                                hand[k].set_flag(True)                                
                                break
                            else: 
                                k += 1
                        break
                    else:
                        j += 1
            i += 1
    print('check finished:')
    for i in tempset:
        print(i)

def hand_checker(hand, mianzi_needed=MIANZI_MAX, quetou_needed=QUETOU_MAX):
    # basic logic for 2/3 card
    if mianzi_needed == 1 and len(hand) == 3:
        return ismianzi(hand[0], hand[1], hand[2])
    if quetou_needed == 1 and len(hand) == 2:
        return isquetou(hand[0], hand[1])
    # iteration method
    i = 0
    j = i + 1
    k = j + 1
    while j < len(hand):
        while k < len(hand):
            if ismianzi(hand[i], hand[j], hand[k]):
                print(i,j,k, hand[i], hand[j], hand[k]) # test
                iter_hand = hand
                del iter_hand[k] # must delete from end to begin
                del iter_hand[j]
                del iter_hand[i]
                for i in iter_hand:
                    print(i)
                if hand_checker(iter_hand, mianzi_needed - 1, quetou_needed):
                    print('OK')
                    for card in hand:
                        card.flag = True
                    return hand
            else: 
                k += 1
        else:
            j += 1
    return None


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

def hand_processer(raw_hand):
    # process raw hand to single card list
    hand = []

    for split in re.findall('\d+[mpsz]', raw_hand):
        suit = re.search('[mpsz]', split).group()
        ranks = re.findall('\d', split)
        test = ranks.sort() # sort ranks, seems no need for sorting suit.
        for rank in ranks:
            hand.append(Card(rank + suit))

    return hand

if __name__ == '__main__':

    print(hand_checker(hand_processer('122334789m123s'), 4, 0))

    test_hand = '122343m456s789p11z'
    # print(hand_processer(test_hand))
    #checker(hand_processer(test_hand))