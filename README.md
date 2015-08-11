# 麻将 Mahjong

关于麻将的工具集, 由 Organization Lab 开发

A toolbox for mahjong game, by Organization Lab

1. 和牌判断器 Mahjong checker `checker.py`
2. 向听数计算器 Xiangtingshu calculator `mahjong.py`

Author: [Organization Lab @ GitHub](Lab)


# How to use

在本地用 Python 3.4.3 运行脚本, 在 OS X 和 Windows 下测试. (Python 2.7 应也可使用, 但未测试)

Clone or Download repo to local. Then run script with Python 3.4.3

Tested in OS X and Windows. (Python 2.7 should also works, but not tested)


## 1. 和牌判断器 Mahjong checker `checker.py`

### 1.1 脚本运行方式 

输入 14 张手牌(手牌格式见下)作为参数, 或在提示后输入参数

`python checker.py hand`

e.g. `$ python checker.py 123456789m123p22s`

`python checker.py`, then input hand

脚本会判断手牌是否是和牌形. 如是和牌形, 脚本会输出和牌的手牌组合(之一).

the script will return if the hand is mahjong. If it is mahjong, the details will be shown.

### 1.2 手牌格式 valid hand format

允许简写`123456789m123p22s`, 也可每张牌单独输入, 如 `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

m-万; p-筒; s-索/条; z-字(1234567z分别代表东南西北白发中)

其它字母均暂不支持.

1-9m/p/s/z, short input is OK.
e.g. `123456789m123p22s`, `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

### 1.3 examples

```
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


## 2. 向听数计算器 Xiangtingshu calculator `mahjong.py`
### 2.1 运行方式

输入 14 张手牌(手牌格式见下)作为参数, 或在提示后输入参数

`python mahjong.py hand`

e.g. `$ python mahjong.py 123456789m123p22s`

`python mahjong.py`, then input hand

脚本会计算手牌的最小向听数, 并给出各种打法的有效牌

the script will return the xiangtingshu(向听数) of hand.

### 2.2 手牌格式 valid hand format

允许简写`123456789m123p22s`, 也可每张牌单独输入, 如 `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

m-万; p-筒; s-索/条; z-字(1234567z分别代表东南西北白发中)

其它字母均暂不支持.

### 2.3 examples

```
$ python mahjong.py 7m8m9m4p5p6p1s1s1s6s7s8s9s4s
手牌: 7m8m9m4p5p6p1s1s1s4s6s7s8s9s
打1s, 向听数0, 有效牌5s, 1种4张
打4s, 向听数0, 有效牌6s9s, 2种6张
打6s, 向听数0, 有效牌4s, 1种3张
打9s, 向听数0, 有效牌4s, 1种3张
```