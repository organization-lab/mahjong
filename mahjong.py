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

def init_paishan():
    """ 生成136张牌山
    i: nothing
    o: a list of 136 random card
    """
    paishan_list = CARD_LIST * 4
    random.shuffle(paishan_list)
    return paishan_list

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

class Group(object):
    """docstring for Group
    手牌组: 面子 雀头 搭子 复合搭, etc.

    """
    def __init__(self, cards, closed=True):
        # cards: card 列表(in Card class)
        super(Group, self).__init__()
        self.cards = cards # 牌组成员列表, 使用列表表示
        self.closed = True # 是否都在手中(closed)
        self.type = self.cal_type()

    def __str__(self): # note: 如何把列表串联变成字符最快, 似乎 py doc FAQ 有
        str_group = ''
        for card in self.cards:
            str_group += str(card)
        return str_group

    def sort(self):
        if self.type in MIANZI:
            sort_type = 0
        elif self.type in QUETOU:
            sort_type = 1
        elif self.type in DAZI: # todo 需要排序, 按照面子雀头搭子孤张顺序
            sort_type = 2
        elif self.type in GUZHANG:
            sort_type = 3
        sort_suit = self.cards[0].get_suit()
        return str(sort_type) + sort_suit + str(self)

    def get_cards(self):
        return self.cards

    def cal_type(self):
        """返回牌组类型: 面子 雀头 搭子 复合搭

        i: 排序的手牌(便于判断搭子大小顺序)
        p: 先根据张数归类, 再判断是否成牌组
        o: 1 孤张 2 雀头/两面/边张/坎张 3 刻子/顺子/连坎/复合搭(特指搭子加对子型)...
        """
        if len(self.cards) == 0:
            return None
        elif len(self.cards) == 1:
            return "guzhang"
        elif len(self.cards) == 2:
            if self.cards[0].get_suit() == self.cards[1].get_suit():
                if self.cards[0].get_rank() == self.cards[1].get_rank(): #雀头
                    return "duizi"
                elif (self.cards[0].get_rank() == self.cards[1].get_rank() - 1 and 
                      self.cards[0].get_suit() is not 'z'): #两面或边张
                    if self.cards[0].get_rank() == 1 or self.cards[0].get_rank() == 8: # 12, 89 边张
                        return "bianzhang"
                    else: #两面
                        return "liangmian"
                elif (self.cards[0].get_rank() == self.cards[1].get_rank() - 2 and 
                      self.cards[0].get_suit() is not 'z'): #坎张
                    return "kanzhang"
            else:
                return None
        elif len(self.cards) == 3:
            # todo: 每次都取回可能比较慢, 也许要考虑提取出来用变量暂存?
            if (self.cards[0].get_suit() == self.cards[1].get_suit() and 
                self.cards[0].get_suit() == self.cards[2].get_suit()):
                if (self.cards[0].get_rank() == self.cards[1].get_rank() and 
                    self.cards[0].get_rank() == self.cards[2].get_rank()):
                    return "kezi"
                    # todo: 可能要加入复合搭
                elif (self.cards[0].get_suit() is not 'z' and
                      self.cards[0].get_rank() == self.cards[1].get_rank() - 1 and 
                      self.cards[1].get_rank() == self.cards[2].get_rank() - 1): # 顺子不能是字牌
                    return "shunzi"
                elif (self.cards[0].get_suit() is not 'z' and
                      self.cards[0].get_rank() == self.cards[1].get_rank() - 2 and 
                      self.cards[1].get_rank() == self.cards[2].get_rank() - 2): # 顺子不能是字牌
                    return "liankan"
                elif (self.cards[0].get_suit() is not 'z' and
                      (self.cards[0].get_rank() == self.cards[2].get_rank() - 1 or 
                       self.cards[0].get_rank() == self.cards[2].get_rank() - 2)):
                    # 复合搭共有112 113 122 133四种形态: 1 3张差别为1或2; 因排序第二张必然位于中间,且不是顺子(否则已经return)
                    return "fuheda"
            else:
                return None
        else: 
            return None
    
    def get_type(self):
        return self.type

    def youxiaopai(self):
        """返回有效牌类型(和数量?)

        """
        pass

class Hand_in_group(object):
    """docstring for Hand_in_group

    i: groups列表, 如果不输入默认为空
    """
    def __init__(self, groups=[]):
        super(Hand_in_group, self).__init__()
        self.groups = groups[:] 
        # 如果不copy而是直接赋值, 会出现问题: 
        # 几个类变量使用同一个列表(和一开始以为的新建列表不同).
        # 虽然类变量地址不同, 但列表的链接相同!
    
    def __str__(self): # note: 如何把列表串联变成字符最快, 似乎 py doc FAQ 有
        str_hand = ''
        for group in self.groups:
            str_hand += group.get_type() + '-' + str(group) + '; '
        return str_hand

    def append(self, new_group):
        self.groups.append(new_group)
        return self

    def remove(self, remove_group): 
        for group in self.groups:
            if is_samegroup(remove_group, group): # todo: 判断两个类变量内容是否相同, 有无更好方法
                self.groups.remove(group)
                return

    def get_groups(self):
        return self.groups

    def sort(self):
        #排序
        self.groups.sort(key=Group.sort)

    def xiangtingshu(self):
        #2.计算向听数 n=8-2*面子-1*雀头(<=1)-1*搭子(<=4-面子)
        num_mianzi = 0
        num_quetou = 0
        num_dazi = 0
        for group in self.groups:
            type_of_group = group.get_type() 
            if type_of_group in MIANZI:
                num_mianzi += 1
            elif type_of_group in QUETOU and num_quetou < 1:
                num_quetou += 1
            elif type_of_group in DAZI and num_dazi < 4 - num_mianzi: # todo 需要排序, 按照面子雀头搭子孤张顺序
                num_dazi += 1
        return 8 - 2 * num_mianzi - num_quetou - num_dazi

def is_samegroup(group1, group2):
    """判断两个牌组是否一样

    """
    return str(group1) == str(group2)

def is_samehandingroup(hand_in_group1, hand_in_group2):
    # todo: 目前暂时是列表, 要改写成类的方法
    return str(hand_in_group1) == str(hand_in_group2) #todo: while else?似乎有这个语法

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
        print(card, end=' ')
    print()

def issamehand(hand1, hand2):
    """判断两手牌是否完全相同: 但需要先排好序再用
    """
    if len(hand1) != len(hand2):
        return False
    else:
        i = 0
        while i < len(hand1):
            if not issamecard(hand1[i], hand2[i]):
                return False
            i += 1
        return True

def issamecard(card1, card2):
    """判断两张牌是否相同
    """
    if (card1.get_suit() == card2.get_suit() and 
        card1.get_rank() == card2.get_rank()):
        return True
    else:
        return False

def isdazi(card1, card2):
    if card1.suit == card2.suit:
        if card1.rank == card2.rank or card1.rank == card2.rank - 1 or card1.rank == card2.rank - 2:
            return True
    return False

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
    """# reverse hand name to sort by suit first

    i: card class
    """
    return card.get_suit(), card.get_rank()

def mahjong_checker(hand, output_notes=False, raw_hand=False):
    """ check if hand is mahjong

    i: hand or raw hand(整理成列表和简写均可接受)
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

def hand_to_group(hand_todo, hand_set=Hand_in_group()):
    """把手牌整理为不同的牌组并计算向听数

    i: hand set 使用分类 hand_todo: Card的列表; hand_set: Hand_in_group class
    p: 每张牌迭代
    o: 列表, 每个成员是 tuple (向听数, 牌组列表)
    """
    global list_xiangtingshu, xiangtingshu_lowest
    if len(hand_todo) == 0: #finished
        # 计算向听数, 如果小于等于当前最小值, 添加到列表中
        # todo: 速度优化. 直接先算一下len(), 如果len很大, 可不用排序直接return, 节约时间
        hand_set.sort()
        xiangtingshu = hand_set.xiangtingshu()
        if xiangtingshu == xiangtingshu_lowest:
            list_xiangtingshu.append((xiangtingshu, hand_set))
        elif xiangtingshu < xiangtingshu_lowest:
            xiangtingshu_lowest = xiangtingshu
            list_xiangtingshu = []
            list_xiangtingshu.append((xiangtingshu, hand_set))
        return

    card_to_set = hand_todo[0] # 需要处理的牌
    #print('card to process', card_to_set) #
    for group in hand_set.get_groups():
        type_group = group.get_type()
        group_plus_card = Group(group.get_cards() + [card_to_set])
        type_plus_card = group_plus_card.get_type()
        #print(type_of_cards(setted), hand_todo[0])# 

        if type_group in MIANZI: 
            # 如果已是面子, 无法添加, 则与孤张处理一样
            pass
        elif type_group in DAZI and type_plus_card in MIANZI:
            # 如果是搭子, 并可与新牌组成面子
            #print('make mianzi')
            hand_set_new = Hand_in_group(hand_set.get_groups())
            hand_set_new.remove(group)
            hand_set_new.append(group_plus_card)
            hand_to_group(hand_todo[1:], hand_set_new)
        elif type_group in GUZHANG and type_plus_card in DAZI:
            # 如果是孤张, 并可与新牌组成搭子
            #print('make dazi')#
            groups = hand_set.get_groups()
            new = Hand_in_group(groups)
            new.remove(group)
            new.append(group_plus_card)
            hand_to_group(hand_todo[1:], new)

    hand_set_new = Hand_in_group(hand_set.get_groups())
    hand_set_new.append(Group([card_to_set]))
    hand_to_group(hand_todo[1:], hand_set_new)# 孤张处理

def xiangtingshu(hand, raw_hand=True):
    """判断向听数的封装

    i: hand set 使用分类 hand_todo: Card的列表
    p: 先用hand_to_group分类; 再分别计算向听数
    o: 向听数
    """
    global list_xiangtingshu, xiangtingshu_lowest #todo: 迭代无法传递, 故暂时使用了全局变量
    
    list_xiangtingshu = []
    xiangtingshu_lowest = XIANGTINGSHU_MAX #init

    hand = hand_processer(hand)
    hand_to_group(hand) # 1.处理成为手牌组
    #print('group', len(list_xiangtingshu)) #

    print('xiangtingshu:', xiangtingshu_lowest) #
    unique_hands = []
    for num, hand in list_xiangtingshu: # 去重
        for unique_hand in unique_hands:
            if is_samehandingroup(hand, unique_hand):
                break
        else:
            unique_hands.append(hand)
    for hand in unique_hands: # 输出最小向听数的牌型
        print(hand)

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
    xiangtingshu(input_hand)

if __name__ == '__main__':
    main()
