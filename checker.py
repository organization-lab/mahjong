# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
import re

test_hand = [('1m',0), ('2m',0), ('3m',0), 
            ('4p', 0), ('5p',0), ('6p', 0), 
            ('7s', 0), ('8s', 0), ('9s', 0), 
            ('1z', 0), ('1z', 0)]

class Card:
    """docstring for card"""
    def __init__(self, card):
        super(Card, self).__init__()
        self.rank = re.search('[1-9]', card).group()
        self.suit = re.search('[mpsz]', card).group()        

    def __str__(self):
        return self.rank + self.suit

print(Card('1m'))

def checker(hand):
    tempset = []
    for card, status in hand:
        print(card, status)
        print(re.match('\d+', card).group()) #temp
        if status is False:
            if test_set(tempset, card) != tempset: 
                tempset = test_set(tempset, card)
                status = True
            if len(tempset) == 3: #finished set
                print(tempset)

def test_set(tempset, card):
    if len(tempset) == 0: #no card added for set
        return tempset.add(card)
    elif len(tempset) == 1 or len(tempset) == 2: #one/two card added
        if card.rank == tempset[0].rank + 1: #right card for straight
            return tempset.add(card)
        else:
            return tempset

checker(test_hand)