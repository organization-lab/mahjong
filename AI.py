# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# mahjong AI

import mahjong
import checker
import checker_tester

def heqie(hand, output_notes=False):
    # todo: 只判断 unique card, 在重复型将可明显减少判断时间.
    """何切函数

    i: 14 card
    p: 比较打每张牌的向听数和有效牌
        暂时只比较种类, 不考虑张数不同
    o: 打某张牌
    """
    xiangtingshu_lowest = 8
    youxiaopai_max = 0
    # 统计出最小向听数和有效牌种类, MVP 版本中只取第一张
    hand.sort(key=mahjong.sort_hand)

    xiangtingshu_14, list_youxiaopai = mahjong.cal_xiangtingshu(hand, raw_hand=False)
    if xiangtingshu_14 == -1:
        return '', -1

    card0 = '' #排除相同牌, 可提高速度
    for card in hand:
        if mahjong.is_samecard(card, card0):
            continue
        hand_card = hand[:]
        hand_card.remove(card)         
        xiangtingshu, list_youxiaopai = mahjong.cal_xiangtingshu(hand_card, raw_hand=False)
        if xiangtingshu < xiangtingshu_lowest:
            best_card = (card, xiangtingshu, list_youxiaopai)
            xiangtingshu_lowest = xiangtingshu
            youxiaopai_max = len(list_youxiaopai)
        elif (xiangtingshu == xiangtingshu_lowest and 
              len(list_youxiaopai) > youxiaopai_max):
            best_card = (card, xiangtingshu, list_youxiaopai)
        card0 = card
    card, xiangtingshu, list_youxiaopai = best_card
    if output_notes: #输出调试信息
        mahjong.print_hand(hand) # 输出手牌内容
        youxiaopai = ''
        for i in list_youxiaopai:
            youxiaopai += str(i)
        print('打{}, 向听数{}, 有效牌{}'.format(card, xiangtingshu, youxiaopai))

    return card, xiangtingshu

def heqie_old(hand):
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
    paishan = mahjong.init_paishan()
    raw_hand = ''.join(paishan[-13:])
    del paishan [-13:]
    hand = mahjong.hand_processer(raw_hand, raw_hand=True)
    while paishan: 
        print('剩余牌量:', len(paishan))
        new_card = paishan.pop()
        print('hand: ', end = '')
        hand.sort(key=mahjong.sort_hand)
        mahjong.print_hand(hand)
        print('new card', new_card)
        hand = hand + [mahjong.Card(new_card)]
        discard_card, xiangtingshu = heqie(hand, output_notes=True)
        print('discard card:', discard_card)
        print('xiangtingshu:', xiangtingshu)
        print()
        if discard_card:
            for card in hand:
                if mahjong.is_samecard(card, discard_card):
                    hand.remove(card)
                    break
        else:
            print('和牌')
            break
    else:
        print('牌山没牌了.')

def main():
    from sys import argv
    script, hand = argv
    heqie(checker.hand_processer(hand),output_notes=True)

if __name__ == '__main__':
    #main()
    heqie_tester()