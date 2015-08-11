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
        #类型+花色+内容; 如0m1m2m3m(面子 万 123m)1s3s3s

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

    def youxiaopai(self, make=''):
        """返回有效牌类型(和数量?)

        i: 牌组
        o: 有效牌列表, in Card class
        """
        if self.type in MIANZI:
            return []
        elif self.type is 'duizi':
            return [self.cards[0]]
        elif self.type is 'bianzhang':
            if self.cards[0].get_rank() == 1:
                rank = '3'
            else:
                rank = '7'
            return [Card(rank + self.cards[0].get_suit())]
        elif self.type is 'kanzhang':
            rank = str(self.cards[0].get_rank() + 1)
            return [Card(rank + self.cards[0].get_suit())]
        elif self.type is 'liangmian':
            rank1 = str(self.cards[0].get_rank() - 1)
            rank2 = str(self.cards[0].get_rank() + 2)
            return [Card(rank1 + self.cards[0].get_suit()),
                    Card(rank2 + self.cards[0].get_suit())]
        elif self.type is 'guzhang':
            if make is 'quetou' or self.cards[0].get_suit() is 'z': # 为了做雀头, 或字牌也只有本身
                return [self.cards[0]]
            else:
                ranks = [-2, -1, 0, 1, 2]
                return [Card(str(rank + self.cards[0].get_rank()) + self.cards[0].get_suit()) 
                        for rank in ranks 
                        if rank + self.cards[0].get_rank() in range(1, 10)]
        else:
            return []

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
        #计算向听数 n=8-2*面子-1*雀头(<=1)-1*搭子(<=4-面子)
        num_mianzi = 0
        num_quetou = 0
        num_dazi = 0
        for group in self.groups:
            type_of_group = group.get_type() 
            if type_of_group in MIANZI:
                num_mianzi += 1
            elif type_of_group in QUETOU and num_quetou < 1:
                num_quetou += 1
            elif type_of_group in DAZI and num_dazi < 4 - num_mianzi: 
                num_dazi += 1
        return 8 - 2 * num_mianzi - num_quetou - num_dazi

    def youxiaopai(self):
        """输出有效牌

        i: 牌组
        p: 按照面子-雀头-搭子-孤张排序并统计数量后, 即可按顺序处理
        o: 有效牌列表(Card class list)
        """
        num_mianzi = 0
        num_quetou = 0
        num_dazi = 0
        num_guzhang = 0
        for group in self.groups: # 计算各个组成部分的数量
            type_of_group = group.get_type() 
            if type_of_group in MIANZI:
                num_mianzi += 1
            elif type_of_group in QUETOU:
                num_quetou += 1
            elif type_of_group in DAZI and num_dazi < 4 - num_mianzi: 
                num_dazi += 1
            else:
                num_guzhang += 1
        list_youxiaopai = [] # 用列表存放所有的有效牌
        for group in self.groups:
            type_of_group = group.get_type() 
            if type_of_group in MIANZI: # 面子没有有效牌
                pass
            elif (type_of_group is 'duizi' and 
                  num_quetou > 1 and num_mianzi < 4): 
                # 两个以上雀头, 且面子未完成时有对倒
                list_youxiaopai += group.youxiaopai()
            elif (type_of_group is 'duizi' and 
                  num_guzhang > 0 and num_mianzi + num_dazi < 4): 
                # 或搭子还不足, 任意孤张都是有效牌
                list_youxiaopai += group.youxiaopai()
            elif (type_of_group in ['bianzhang', 'kanzhang', 'liangmian'] and
                  num_mianzi < 4): 
                list_youxiaopai += group.youxiaopai()
            elif type_of_group is 'guzhang': # 孤张有两种情况, 形成搭子和形成雀头
                if num_quetou == 0:
                    list_youxiaopai += group.youxiaopai(make='quetou')
                elif num_mianzi + (num_quetou - 1) + num_dazi < 4: 
                # 面子+(对子-1)+搭子<4
                    list_youxiaopai += group.youxiaopai()
        return list_youxiaopai

MIANZI = ['shunzi', 'kezi']
QUETOU = ['duizi']
DAZI = ['duizi', 'bianzhang', 'kanzhang', 'liangmian']
GUZHANG = ['guzhang'] # init respones

CARD_LIST = [str(rank) + suit 
             for suit in ['m', 'p', 's', 'z'] 
             for rank in range(1, 10) 
             if rank in range(1,8) or suit is not 'z']

CARD_LEFT = {card:4 for card in CARD_LIST} # 存储剩余牌量的字典, 通过 used_card 删除

VALID_LENGTH_OF_HAND = 14
MIANZI_MAX = 4
QUETOU_MAX = 1
XIANGTINGSHU_MAX = 8
finished_hand = [] # use this list for storing finished hand after iteration

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

def is_samegroup(group1, group2):
    #判断两个牌组是否相同, 使用 str() 比较字符串
    return str(group1) == str(group2)

def is_samehandingroup(hand_in_group1, hand_in_group2):
    return str(hand_in_group1) == str(hand_in_group2) 

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

def hand_to_group(hand_todo, hand_set=Hand_in_group()):
    """把手牌整理为不同的牌组并计算向听数

    i: hand set 使用分类 hand_todo: Card的列表; hand_set: Hand_in_group class
    p: 每张牌迭代, 尝试加入每一个牌组之中. 或作为孤张(速度慢的主要原因, 大约 2^n 复杂度)
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

def cal_xiangtingshu(hand, raw_hand=True, output_notes=False):
    """计算向听数的封装

    i: hand set 使用分类 hand_todo: Card的列表, 最好是13张
    p: 先用hand_to_group分类; 去重; 合并不同 group 的所有有效牌; 输出
    o: 最小向听数, 有效牌数量, 有效牌列表
    """
    global list_xiangtingshu, xiangtingshu_lowest 
    #todo: 迭代无法传递, 故暂时使用了全局变量
    
    list_xiangtingshu = []
    xiangtingshu_lowest = XIANGTINGSHU_MAX #init

    hand = hand_processer(hand, raw_hand)
    hand_to_group(hand) # 1.处理成为手牌组
    if output_notes:
        print('向听数:', xiangtingshu_lowest) #
    unique_hands = []
    for num, hand in list_xiangtingshu: # 去重
        for unique_hand in unique_hands:
            if is_samehandingroup(hand, unique_hand):
                break
        else:
            unique_hands.append(hand)
    unique_youxiaopais = []
    for hand in unique_hands: # 输出最小向听数的牌型
        #print(hand)
        for card in hand.youxiaopai():
            for youxiaopai in unique_youxiaopais:
                if is_samecard(card, youxiaopai):
                    break
            else: # todo 查阅 for else
                unique_youxiaopais.append(card)
    unique_youxiaopais.sort(key=sort_hand) # 排序, 稍作整理

    num_youxiaopai = 0
    for card in unique_youxiaopais:
        num_youxiaopai += CARD_LEFT[str(card)]

    if output_notes:
        for card in unique_youxiaopais:
            print(card, end = '')
        print()

    return xiangtingshu_lowest, num_youxiaopai, unique_youxiaopais

def xiangtingshu_output(hand, raw_hand=True):
    """通过比较向听数和有效牌, 输出打某张, 向听数, 有效牌列表等何切信息

    i: hand 最好是14张
    p: 调用 cal_xiangtingshu(), 输出所有的可能最小向听数组合, 暂只支持标准型
    o: 输出何切信息
    """
    hand = hand_processer(hand, raw_hand)
    # todo: 只判断 unique card, 在重复型将可明显减少判断时间.

    xiangtingshu_lowest = 8
    best_cards = []
    for card in hand: 
        used_card(card)# 从牌山中去掉
    # 统计出最小向听数
    card0 = ''
    for card in hand: 
        if is_samecard(card, card0):
            continue
        else:
            card0 = card
        hand_card = hand[:]
        hand_card.remove(card)         
        xiangtingshu, num_youxiaopai, list_youxiaopai = cal_xiangtingshu(hand_card, raw_hand=False)
        if xiangtingshu < xiangtingshu_lowest:
            best_cards = [(card, xiangtingshu, num_youxiaopai, list_youxiaopai)]
            xiangtingshu_lowest = xiangtingshu
        elif xiangtingshu == xiangtingshu_lowest:
            best_cards.append((card, xiangtingshu, num_youxiaopai, list_youxiaopai))
    # 输出
    print('手牌: ', end = '')
    print_hand(hand) # 输出手牌内容
    #print(best_cards)
    for card, xiangtingshu, num_youxiaopai, list_youxiaopai in best_cards:
        youxiaopai = ''
        for i in list_youxiaopai:
            youxiaopai += str(i)
        print('打{}, 向听数{}, 有效牌{}, {}种{}张'.format(card, xiangtingshu, youxiaopai, len(list_youxiaopai), num_youxiaopai))    

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

    xiangtingshu_output(input_hand)

if __name__ == '__main__':
    main()
