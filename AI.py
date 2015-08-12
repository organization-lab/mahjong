# -*- coding: utf-8 -*-
# Author: Frank-the-Obscure @ Organzation Labortory @ GitHub
# mahjong AI

import mahjong
import autogui
import time

def heqie(hand, output_notes=False):
    """何切函数

    i: 14 card Class
    p: 比较打每张牌的向听数和有效牌
        暂时只比较种类, 不考虑张数不同
    o: 打某张牌, 及向听数
    """
    xiangtingshu_lowest = 8
    youxiaopai_max = 0
    # 统计出最小向听数和有效牌种类, MVP 版本中只取第一张
    hand.sort(key=mahjong.sort_hand)

    xiangtingshu_14, num_youxiaopai, list_youxiaopai = mahjong.cal_xiangtingshu(hand, raw_hand=False)
    if xiangtingshu_14 == -1: # 已经和牌
        return '', -1

    card0 = '' #排除相同牌, 可一定程度上提高速度
    for card in hand: # 循环打每一张牌, 判断哪张向听数最小且有效牌多.
        if mahjong.is_samecard(card, card0): #排除相同牌, 可一定程度上提高速度
            continue
        hand_card = hand[:]
        hand_card.remove(card) 
        xiangtingshu, num_youxiaopai, list_youxiaopai = mahjong.cal_xiangtingshu(hand_card, raw_hand=False)
        if xiangtingshu < xiangtingshu_lowest: #最小向听数 
            best_card = (card, xiangtingshu, num_youxiaopai, list_youxiaopai)
            xiangtingshu_lowest = xiangtingshu
            youxiaopai_max = num_youxiaopai
        elif (xiangtingshu == xiangtingshu_lowest and 
              num_youxiaopai > youxiaopai_max): # 或者相同向听数,但有效牌更多
            best_card = (card, xiangtingshu, num_youxiaopai, list_youxiaopai)
            youxiaopai_max = num_youxiaopai
        card0 = card
    card, xiangtingshu, num_youxiaopai, list_youxiaopai = best_card
    if output_notes: #输出调试信息
        youxiaopai = ''
        for i in list_youxiaopai:
            youxiaopai += str(i)
        print('打{}, 向听数{}, 有效牌{}, {}种{}张'.format(card, xiangtingshu, youxiaopai, len(list_youxiaopai), num_youxiaopai))

    return card, xiangtingshu # 返回切出的牌及向听数

def heqie_tester():
    """发牌器, 测试何切函数
    """
    paishan = mahjong.init_paishan() #init
    raw_hand = ''.join(paishan[-13:]) #发手牌
    del paishan [-13:]
    hand = mahjong.hand_processer(raw_hand, raw_hand=True)

    for card in hand:
        mahjong.used_card(card) # 计算剩余牌量

    while paishan: 
        print('剩余牌量:', len(paishan))
        new_card = paishan.pop() # 出一张牌
        mahjong.used_card(new_card) # 计算剩余牌量
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
            return True
    else:
        print('牌山没牌了.')

def ai():
    """ai using 国标v1.30
    读取手牌-(读取新摸牌-切牌)
    """
    raw_hand = autogui.get_hand()
    hand = mahjong.hand_processer(raw_hand, raw_hand=True)

    for card in hand:
        mahjong.used_card(card) # 计算剩余牌量

    while True: 
        time.sleep(1)
        autogui.pass_mingpai()
        time.sleep(1)
        autogui.pass_mingpai()
        time.sleep(1)
        autogui.pass_mingpai()
        time.sleep(1)

        new_card = autogui.get_card() # 出一张牌
        mahjong.used_card(new_card) # 计算剩余牌量
        print('hand: ', end = '')
        hand.sort(key=mahjong.sort_hand)
        mahjong.print_hand(hand)
        print('new card', new_card)
        hand_plus = hand + [mahjong.Card(new_card)]
        discard_card, xiangtingshu = heqie(hand_plus, output_notes=True)
        print('discard card:', discard_card)
        print('xiangtingshu:', xiangtingshu)
        if discard_card:
            for card in hand:
                if mahjong.is_samecard(card, discard_card):
                    print('切第n张:', hand.index(card))
                    autogui.qiepai(hand.index(card))
                    hand_plus.remove(card)
                    hand = hand_plus
                    break
            else:
                autogui.qiepai(13)
        else:
            print('和牌')
            return True
    else:
        print('牌山没牌了.')

def main():
    ai()

if __name__ == '__main__':
    main()
