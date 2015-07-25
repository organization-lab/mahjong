# 麻将 Mahjong

关于麻将的工具集, 由Organization Lab 开发

A toolbox for mahjong game, by Organization Lab

Author: [Organization Lab @ GitHub](Lab)

## Release Note
v 1.1: 标准型, 七对子和十三幺均已支持.

七对子接受四归一

# How to use

在本地用 Python 3.4.3 运行脚本, 在 OS X 和 Windows 下测试. (Python 2.7 应也可使用, 但未测试)

Clone or Download repo to local. Then run script with Python 3.4.3

Tested in OS X and Windows. (Python 2.7 should also works, but not tested)

## 1. 和牌判断器 Mahjong checker 

### 1.1 脚本运行方式 

输入 14 张手牌(手牌格式见下)作为参数, 或在提示后输入参数

`python checker.py hand`

e.g. `$ python checker.py 123456789m123p22s`

`python checker.py`, then input hand

脚本会判断手牌是否是和牌形. 如是和牌形, 脚本会输出和牌的手牌组合(之一).

the script will return if the hand is mahjong. If it is mahjong, the details will be shown.

### 1.2 手牌格式 valid hand format

允许简写`123456789m123p22s`, 也可每张牌单独输入, 如 `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

其它字母均暂不支持.

1-9m/p/s/z, short input is OK.
e.g. `123456789m123p22s`, `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

### 1.3 examples
```python

$ python checker.py 123456m456789p11s
Hand is mahjong. Wining hand is:
1m2m3m 4m5m6m 4p5p6p 7p8p9p 1s1s

$ python checker.py 113355777799s
Hand is not valid.

$ python checker.py 11335577779911s
Hand is mahjong. Wining hand is:
1s1s 1s1s 3s3s 5s5s 7s7s 7s7s 9s9s

$ python checker.py 119m19p19s1234567z
Hand is mahjong. Wining hand is:
1m 1m 9m 1p 9p 1s 9s 1z 2z 3z 4z 5z 6z 7z

$ python checker.py
input hand: 123m456789p789s11z
Hand is mahjong. Wining hand is:
1m2m3m 4p5p6p 7p8p9p 7s8s9s 1z1z
```

## 2. 听牌判断器 Mahjong checker of unfinished form
与上述和牌判断器类似, 输入 **13** 张手牌(手牌格式相同).

脚本将给出手牌所听的牌

注: 已有四张, 形式上听第五张算作听牌.

`python checker-tester.py hand`

e.g. `$ python checker-tester.py 1112345678999m`

`python checker-tester.py`, then input hand

```python
$ python checker-tester.py 13456789m111s44z
2m

$ python checker-tester.py 23456789m111s44z
1m 4m 7m

$ python checker-tester.py 123456789m111s4z
4z

$ python checker-tester.py 123456789m11s44z
1s 4z

$ python checker-tester.py 19m19p19s1234567z
1m 9m 1p 9p 1s 9s 1z 2z 3z 4z 5z 6z 7z

$ python checker-tester.py 1112345678999m
1m 2m 3m 4m 5m 6m 7m 8m 9m

$ python checker-tester.py 123456789m11s46z
Not tingpai.

$ python checker-tester.py 123456789m111s46z
Wrong input!

$ python checker-tester.py 123456789m1111z
1z

```


