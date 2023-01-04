import sys

LOST = 0
DRAW = 3
WON = 6

opp_offset = "A"
me_offset = "X"
score = 0
for line in sys.stdin.readlines():
    (opp, me) = line.rstrip().split()
    opp_move = ord(opp) - ord(opp_offset)
    me_move = ord(me) - ord(me_offset)
    if opp_move == me_move:
        score += DRAW + me_move + 1
    elif opp_move == 0 and me_move == 1:
        score += WON + me_move + 1
    elif opp_move == 0 and me_move == 2:
        score += LOST + me_move + 1
    elif opp_move == 1 and me_move == 0:
        score += LOST + me_move + 1
    elif opp_move == 1 and me_move == 2:
        score += WON + me_move + 1
    elif opp_move == 2 and me_move == 0:
        score += WON + me_move + 1
    elif opp_move == 2 and me_move == 1:
        score += LOST + me_move + 1

print(score)
