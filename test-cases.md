# Mahjong - test cases

## 1. 向听数 13
暂只有标准型

1.1 听牌

123456789m123p8s

123456789m23p88s

1.2 一向听

12345689m233p88s

123456789m23p68s

123456789m28p88s

1.3 两向听

123889m23p23388s

## 2. 何切 14

2.1 听牌

123456789m123p68s

123456789m235p88s

123456789m236p88s

2.2 一向听

12345689m2335p88s

123456789m235p68s

123456789m258p88s

2.3 两向听

123889m23p233588s


## 3. Classes

3.1 Card class

Card('1m')
Card('2m')
Card('3m')

3.2 Group class

Group([Card('1m')])
Group([Card('1m'), Card('2m')])
Group([Card('2m'), Card('2m')])
Group([Card('2m'), Card('3m')])
Group([Card('1m'), Card('3m')])
