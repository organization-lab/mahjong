# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# a simple checker for mahjong: test if the cards makes a winning hand.


import re
from sys import argv

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


VALID_LENGTH_OF_HAND = 14
MIANZI_MAX = 4
QUETOU_MAX = 1
finished_hand = []

def hand_checker(hand, mianzi_needed=MIANZI_MAX, quetou_needed=QUETOU_MAX):
    global finished_hand
    # every iteration: return finished hand

    # basic logic for 2/3 card
    if mianzi_needed == 1 and len(hand) == 3:
        if Mianzi(hand[0], hand[1], hand[2]).isvalid():
            finished_hand.append(Mianzi(hand[0], hand[1], hand[2]))
        return Mianzi(hand[0], hand[1], hand[2]).isvalid()
    if quetou_needed == 1 and len(hand) == 2:
        if Quetou(hand[0], hand[1]).isvalid():
            finished_hand.append(Quetou(hand[0], hand[1]))
        return Quetou(hand[0], hand[1]).isvalid()
    # iteration method
    i = 0
    j = i + 1
    k = j + 1
    while j < len(hand):
        # 迭代: 因为只有一个雀头, 先尝试形成雀头; 如果不能, 则该张牌一定是面子的组成部分.
        if quetou_needed and Quetou(hand[i], hand[j]).isvalid():
            iter_hand = hand[:] # slicing to create a copy (instead of '=', modifying the original list)
            del iter_hand[j]
            del iter_hand[i]
            if hand_checker(iter_hand, mianzi_needed, quetou_needed - 1):
                '''# 剩下手牌可以make, finish
                for card in hand:
                    card.flag = True
                    print(card, end=',') # test card in hand
                print() # test'''
                finished_hand.append(Quetou(hand[i], hand[j]))
                return hand
            else: 
                pass
                # 剩下手牌不能make, 说明不应该把这两张牌当成雀头
        while k < len(hand):
            if Mianzi(hand[i], hand[j], hand[k]).isvalid():
                iter_hand = hand[:] # slicing to create a copy (instead of '=', modifying the original list)
                del iter_hand[k] # trick must delete from end to begin
                del iter_hand[j]
                del iter_hand[i]
                if hand_checker(iter_hand, mianzi_needed - 1, quetou_needed):
                    '''
                    for card in hand:
                        card.flag = True
                        print(card, end=',') # test card in hand
                    print() # test '''
                    finished_hand.append(Mianzi(hand[i], hand[j], hand[k]))                   
                    return hand
                else: 
                    k += 1
            else: 
                k += 1
        else:
            j += 1
            k = j + 1
    return None

def isdazi(card1, card2):
    # not for kanzhang now, 判断和牌暂时不包括坎张
    if card1.suit == card2.suit:
        if card1.rank == card2.rank or card1.rank == card2.rank - 1:
            return True
    return False

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


#print(hand_checker(hand_processer('11122m'),1,1))


if __name__ == '__main__':
    try:
        script, test_hand = argv
    except ValueError:
        test_hand = input('input hand: ')

    finished_hand = []
    if hand_processer(test_hand):
        if hand_checker(hand_processer(test_hand)):
            print('Hand is mahjong. Wining hand is: ')
            finished_hand.reverse()

            #move quetou to last
            for i in finished_hand:
                if type(i) == Quetou:
                    quetou = i
                    finished_hand.remove(i)
            finished_hand.append(quetou)
            for i in finished_hand:
                print(i, end= ' ')
            print()
        else:
            print('Hand is not mahjong.')
    #print(hand_processer(test_hand))
    #checker(hand_processer(test_hand))
