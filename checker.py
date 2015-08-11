# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ GitHub
# mahjong basic module

import re
import random

class Card:
    """docstring for card"""
    def __init__(self, card):
        super(Card, self).__init__()
        self.suit = re.search('[mpsz]', card).group()
        if self.suit is 'z':
            self.rank = int(re.search('[1-7]', card).group())
        else:
            self.rank = int(re.search('[1-9]', card).group())       

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

MIANZI = ['shunzi', 'kezi']
QUETOU = ['duizi']
DAZI = ['duizi', 'bianzhang', 'kanzhang', 'liangmian']
GUZHANG = ['guzhang'] # init respones

CARD_LIST = [str(rank) + suit 
             for suit in ['m', 'p', 's', 'z'] 
             for rank in range(1, 10) 
             if rank in range(1,8) or suit is not 'z']

CARD_LEFT = {card:4 for card in CARD_LIST}

def init_paishan():
    """ 生成136张牌山
    i: nothing
    o: a list of 136 random card
    """
    paishan_list = CARD_LIST * 4
    random.shuffle(paishan_list)
    return paishan_list

def used_card(card): # 从字典中去掉用过的牌, card in Card class
    CARD_LEFT[str(card)] -= 1


VALID_LENGTH_OF_HAND = 14
MIANZI_MAX = 4
QUETOU_MAX = 1
XIANGTINGSHU_MAX = 8
finished_hand = [] # use this list for storing finished hand after iteration

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
        if (self.card1.suit == self.card2.suit and 
            self.card1.suit == self.card3.suit):
            if (self.card1.rank == self.card2.rank - 1 and 
                self.card2.rank == self.card3.rank - 1 and
                self.card1.suit is not 'z'): # 顺子不能是字牌
                return True
            elif (self.card1.rank == self.card2.rank and 
                  self.card1.rank == self.card3.rank):
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
        if (self.card1.suit == self.card2.suit and 
            self.card1.rank == self.card2.rank):
            return True
        else:
            return False

''' 写了初步的手牌类, 但暂不计划使用.
class Hand(object):
    """docstring for Hand"""
    def __init__(self, raw_hand, length=VALID_LENGTH_OF_HAND, check_input=False):
        # 1. separate hand
        self.hand = []
        for split in re.findall('[1-9]+[mpsz]', raw_hand): #valid number 1-9, valid suit mpsz
            suit = re.search('[mpsz]', split).group()
            ranks = re.findall('[1-9]', split)
            for rank in ranks:
                self.hand.append(rank + suit)
        # 3. check if hand length is valid
        if len(self.hand) != length and check_input:
            #print('hand is not valid, please check')
            self.hand = None
        # 4. output by Card class
        hand_in_class = [Card(card) for card in self.hand]
        # 2. sort first by suit, second by rank
        hand_in_class.sort(key = sort_hand)
        self.hand = hand_in_class 

    def __str__(self):
        hand_list = []
        for card in self.hand:
            hand_list.append(str(card.get_rank()) + card.get_suit())
        return ' '.join(hand_list)

    def sort_hand(card):
        """# reverse hand name to sort by suit first

        i: card class
        """
        return card.get_suit(), card.get_rank()
'''

def hand_checker(hand, mianzi_needed=MIANZI_MAX, quetou_needed=QUETOU_MAX):
    """iterator for standard form

    标准型判断: 用ijk三个变量逐步上升迭代每一张牌, 每完成一部分就切掉迭代.
    直至组成需要的面子和雀头数量
    """
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
    # i j k 是面子的三张牌, 在手牌中不断向后移动寻找构成面子的牌
    i = 0
    j = i + 1
    k = j + 1
    while j < len(hand):
        # 迭代: 因为只有一个雀头, 先尝试形成雀头; 
        # 如果不能, 则该张牌一定是面子的组成部分.
        if quetou_needed and Quetou(hand[i], hand[j]).isvalid():
            iter_hand = hand[:] 
            # slicing to create a copy 
            # (instead of '=', which modifying the original list)
            del iter_hand[j]
            del iter_hand[i]
            if hand_checker(iter_hand, mianzi_needed, quetou_needed - 1):
                finished_hand.append(Quetou(hand[i], hand[j]))
                return hand
            else: 
                pass
                # 剩下手牌不能make, 说明不应该把这两张牌当成雀头
        while k < len(hand):
            if Mianzi(hand[i], hand[j], hand[k]).isvalid():
                iter_hand = hand[:] 
                del iter_hand[k] # trick: must delete from end to begin
                del iter_hand[j]
                del iter_hand[i]
                if hand_checker(iter_hand, mianzi_needed - 1, quetou_needed):
                    finished_hand.append(Mianzi(hand[i], hand[j], hand[k]))                   
                    return hand
                else: 
                    k += 1 # 这张牌不能构成面子, 变量需要换成下一张牌继续尝试
            else: 
                k += 1
        else:
            j += 1 # j变化时, 要重置k的值
            k = j + 1
    return None

def non_standard_form(hand, 
    mianzi_needed=MIANZI_MAX, 
    quetou_needed=QUETOU_MAX):
    # non-standard form of mahjong
    global finished_hand 
    finished_hand = []

    if mianzi_needed == MIANZI_MAX and quetou_needed == QUETOU_MAX:
        # qiduizi (seven pairs)
        i = 0
        flag = True # 判断是否形成七对子
        while i < len(hand) - 1:
            if not Quetou(hand[i], hand[i + 1]).isvalid():
                flag = False
                break
            finished_hand.append(Quetou(hand[i], hand[i + 1]))
            i += 2
        if flag:
            # print('mahjong: qiduizi')
            return True
        # 十三幺: 静态匹配十三种和牌形即可.
        yaojiu = hand_processer('19m19p19s1234567z')
        # 生成十三种和牌形, use list comprehensions & sorted()
        # 两次注意到返回值的问题..分别用+[]和sorted创建新对象
        shisanyao = [sorted(yaojiu + [card], key=sort_hand) 
                     for card in yaojiu]
        # 循环判断是否一致
        for shisanyao_hand in shisanyao:
            if issamehand(shisanyao_hand, hand):
                finished_hand = shisanyao_hand
                return True
    else:
        return False

def print_hand(hand):
    """print hand for testing

    """
    for card in hand:
        print(card, end='')
    print()

def issamehand(hand1, hand2):
    """判断两手牌是否完全相同: 但需要先排好序再用
    """
    if len(hand1) != len(hand2):
        return False
    else:
        i = 0
        while i < len(hand1):
            if not is_samecard(hand1[i], hand2[i]):
                return False
            i += 1
        return True

def is_samecard(card1, card2):
    """判断两张牌是否相同
    """
    return str(card1) == str(card2)

def hand_processer(hand, raw_hand=True, length=VALID_LENGTH_OF_HAND, check_input=False):
    """ process raw hand to single card list

    i: raw hand, length of hand, check input or not
    o: list of cards by Card class; 
    return None when wrong input & check input is True
    """
    if not raw_hand:
        hand.sort(key=sort_hand)
        return hand
    # or input raw_hand
    processed_hand = []
    # 1. separate hand
    for split in re.findall('[1-9]+[mpsz]', hand): 
        #valid number 1-9, valid suit mpsz
        suit = re.search('[mpsz]', split).group()
        ranks = re.findall('[1-9]', split)
        for rank in ranks:
            processed_hand.append(rank + suit)
    # 3. check if hand length is valid
    if len(processed_hand) != length and check_input:
        #print('hand is not valid, please check')
        return None
    # 4. output by Card class
    hand_in_class = [Card(card) for card in processed_hand]
    # 2. sort first by suit, second by rank
    hand_in_class.sort(key=sort_hand)
    return hand_in_class

def sort_hand(card):
    """ reverse hand name to sort by suit first

    i: list of card class
    """
    return card.get_suit(), card.get_rank()

def mahjong_checker(hand, output_notes=False, raw_hand=True):
    """判断是否和牌

    i: hand or raw hand(整理成列表和简写均可接受)
    p: 可判断标准型 七对子和十三幺
    o: if the hand is mahjong or not. return True / False
    output_notes is for printing info
    """
    global finished_hand 
    finished_hand = []

    if raw_hand: # process raw hand to hand if needed
        hand = hand_processer(hand, check_input=True)
    if hand:
        # 1. non standard form
        if non_standard_form(hand):
            if output_notes:
                print('Hand is mahjong. Wining hand is: ') 
                # may need abstract as a variable
                for i in format_finished_hand(finished_hand, 'qiduizi'):
                    print(i, end= ' ')
                print()                
            return True
        else:
            finished_hand = [] # re-init global
        # 2. standard form
        if hand_checker(hand):
            if output_notes:
                print('Hand is mahjong. Wining hand is: ')
                for i in format_finished_hand(finished_hand):
                    print(i, end= ' ')
                print()
            return True
        else:
            if output_notes:
                print('Hand is not mahjong.')
            return False
    else:
        print('Hand is not valid.')
        return False

def format_finished_hand(finished_hand, kind='standard'):
    # 整理和牌型结构
    if kind is not 'standard':
        # non-standard form 非标准型
        return finished_hand
    else:
        # 1.reverse mahjong
        finished_hand.reverse()
        # 2.move quetou to last
        for hand_set in finished_hand:
            if type(hand_set) == Quetou:
                quetou = hand_set
                finished_hand.remove(hand_set)
        finished_hand.append(quetou)
        return finished_hand

def main():
    """main func.

    i: argv or input later
    o: is mahjong or not
    """
    from sys import argv
    try:
        script, input_hand = argv
    except ValueError:
        input_hand = input('input hand: ')

    mahjong_checker(input_hand, output_notes=True)

if __name__ == '__main__':
    main()
