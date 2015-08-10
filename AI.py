# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# mahjong AI

import mahjong
import checker
import checker_tester

def heqie_new(hand):
    # todo: 只判断 unique card, 在重复型将可明显减少判断时间.
    xiangtingshu_lowest = 9
    best_cards = []
    # 统计出最小向听数
    for card in hand: 
        hand_card = hand[:]
        hand_card.remove(card)         
        xiangtingshu, list_youxiaopai = mahjong.xiangtingshu(hand_card, raw_hand=False, output_notes=True)
        if xiangtingshu < xiangtingshu_lowest:
            best_cards = [(card, xiangtingshu, list_youxiaopai)]
            xiangtingshu_lowest = xiangtingshu
        elif xiangtingshu == xiangtingshu_lowest:
            best_cards.append((card, xiangtingshu, list_youxiaopai))
    # 输出
    print('手牌:')
    mahjong.print_hand(hand) # 输出手牌内容
    #print(best_cards)
    for card, xiangtingshu, list_youxiaopai in best_cards:
        youxiaopai = ''
        for i in list_youxiaopai:
            youxiaopai += str(i)
        print('打{}, 向听数{}, 有效牌{}'.format(card, xiangtingshu, youxiaopai))

def heqie(hand):
    """何切函数
    i: 手牌14张 in class
    o: 打某张 or 宣布和牌
    """
    if checker.mahjong_checker(hand, output_notes=False, raw_hand=False): 
        # 已经和牌
        print("和牌")
        return False
    else:
        # 需要打某张牌
        # 先判断是否已经听牌了
        tingpai = checker_tester.totingpai_14(hand)
        if tingpai:
            hand.remove(tingpai.pop())
        else:
            # 没听牌, 打左数第一张 =.=
            print(hand[0])
            del hand[0]
        return hand

def heqie_tester():
    """发牌器, 测试何切函数
    """
    paishan = checker.init_paishan()
    test_hand = checker.hand_processer("123456789m1244p", raw_hand=True)
    while paishan: 
        new_card = paishan.pop()
        print('new card', new_card)
        s = heqie(test_hand + [checker.Card(new_card)])
        if s:
            print("temp hand", end = ":")
            for card in s:
                print(card, end = ",")
            print()
        else:
            break

heqie_new(checker.hand_processer("123456789m258p88s", raw_hand=True))