# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# mahjong AI

import checker
import checker_tester

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

heqie_tester()