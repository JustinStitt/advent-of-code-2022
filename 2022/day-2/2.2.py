import sys

outcomes = [
    lambda x: 2 if not x else x - 1,
    lambda x: x,
    lambda x: 0 if x == 2 else x + 1,
]

opp_offset = "A"
me_offset = "X"
score = 0
LOST = 0
DRAW = 3
WON = 6

for line in sys.stdin.readlines():
    (opp, should) = line.rstrip().split()
    opp_move = ord(opp) - ord(opp_offset)  # 0 1 2
    me_move = outcomes[ord(should) - ord(me_offset)](opp_move)
    # now calculate
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
