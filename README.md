# Mahjong 麻将

A toolbox for mahjong game, by Organization lab

Author: Frank-the-Obscure @ GitHub


## Mahjong checker 和牌判断器

usage:

0. hand format

1-9m/p/s/z, short input is OK.
e.g. `123456789m123p22s`, `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`
允许简写`123456789m123p22s`, 也可每张牌单独输入, 如 `1m2m3m4m5m6m7m8m9m1p2p3p2s2s`

1. `python checker.py hand`

2. `python checker.py`, then input hand

3. the script will return if the hand is mahjong.  
If it is mahjong, the details will be shown.

脚本会判断手牌是否是和牌形. 如是和牌形, 脚本会输出具体的手牌组合.

Note of v 1.0:

only stardard mahjong supported.

只支持标准和牌形