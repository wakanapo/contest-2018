#!/usr/bin/python3

N = 15

# The main routine of AI.
# input: str[N][N] field : state of the field.
# output: int[2] : where to put a stone in this turn.

def LongestPoint(field, position, mark):
    dists = [CountStonesOnLine(field, position, (1, 1), mark),
     CountStonesOnLine(field, position, (1, 0), mark),
     CountStonesOnLine(field, position, (1, -1), mark),
     CountStonesOnLine(field, position, (0, 1), mark),
     ]
    return max(dists)

def Think(field):
    CENTER = (int(N / 2), int(N / 2))
    best_position = (0, 0)
    for i in range(N):
        for j in range(N):
            if field[i][j] != '.':
                continue
            if GetDistance((i, j), CENTER) < GetDistance(best_position, CENTER):
                best_position = (i, j)

    for i in range(N):
        for j in range(N):
            if field[i][j] != '.':
                continue

            position = (i, j)
            # Assume to put a stone on (i, j).
            field[i][j] = 'O'
            if CanHaveFiveStones(field, position, 'O'):
                DebugPrint('I have a winning choice at (%d, %d)' % (i, j))
                return position

            field[i][j] = 'X'
            if CanHaveFiveStones(field, position, 'X'):
                return position

            field[i][j] = 'X'
            if CanHaveNStones(field, position, 'X', 4):
                return position
            
            # Revert the assumption.
            field[i][j] = '.'
            if LongestPoint(field, position, 'O') > LongestPoint(field, best_position, 'O'):
                best_position = position

            if LongestPoint(field, position, 'O') == LongestPoint(field, best_position, 'O'):
               if CanHaveNStones(field, position, 'O', LongestPoint(field, position, 'O')):
                   best_position = position
    return best_position

def RangeCheck(position):
    if position[0] > 14 or position[0] < 0:
        return False
    if position[1] > 14 or position[0] < 0:
        return False
    return True

def CanHaveNStones(field, position, mark, n):
    if CountStonesOnLine(field, position, (1, 1), mark) >= n:
        if RangeCheck((position[0] + 1, position[1] + 1)) and field[position[0] + 1][position[1] + 1] == mark:
            if RangeCheck((position[0] + n, position[1] + n)):
                return field[position[0] + n][position[1] + n] == '.'
            
        if  RangeCheck((position[0] - 1, position[1] - 1)) and field[position[0] - 1][position[1] - 1] == mark:
            if RangeCheck((position[0] - n, position[1] - n)):
                return field[position[0] - n][position[1] - n] == '.'
            
    if CountStonesOnLine(field, position, (1, 0), mark) >= n:
        if  RangeCheck((position[0] + 1, position[1])) and field[position[0] + 1][position[1]] == mark:
            if RangeCheck((position[0] + n, position[1])):
                return field[position[0] + n][position[1]] == '.'
        if  RangeCheck((position[0] - 1, position[1])) and field[position[0] - 1][position[1]] == mark:
            if  RangeCheck((position[0] - n, position[1])):
                return field[position[0] - n][position[1]] == '.'
            
    if CountStonesOnLine(field, position, (1, -1), mark) >= n:
        if  RangeCheck((position[0] + 1, position[1] - 1)) and field[position[0] + 1][position[1] - 1] == mark:
            if  RangeCheck((position[0] + n, position[1] - n)):
                return field[position[0] + n][position[1] - n] == '.'
        if  RangeCheck((position[0] - 1, position[1] + 1)) and field[position[0] - 1][position[1] + 1] == mark:
            if RangeCheck((position[0] - n, position[1] + n)):
                return field[position[0] - n][position[1] + n] == '.'
            
    if CountStonesOnLine(field, position, (0, 1), mark) >= n:
        if  RangeCheck((position[0], position[1] + 1)) and field[position[0]][position[1] + 1] == mark:
            if  RangeCheck((position[0], position[1] + n)):
                return field[position[0]][position[1] + n] == '.'
        if  RangeCheck((position[0], position[1] - 1)) and field[position[0]][position[1] - 1] == mark:
            if  RangeCheck((position[0], position[1] - n)):
                return field[position[0]][position[1] - n] == '.'


# Returns true if you have five stones from |position|. Returns false otherwise.
def CanHaveFiveStones(field, position, mark):
    return (CountStonesOnLine(field, position, (1, 1), mark) >= 5 or
            CountStonesOnLine(field, position, (1, 0), mark) >= 5 or
            CountStonesOnLine(field, position, (1, -1), mark) >= 5 or
            CountStonesOnLine(field, position, (0, 1), mark) >= 5)


# Returns the number of stones you can put around |position| in the direction specified by |diff|.
def CountStonesOnLine(field, position, diff, mark):
    count = 0

    row = position[0]
    col = position[1]
    while True:
        if row < 0 or col < 0 or row >= N or col >= N or field[row][col] != mark:
            break
        row += diff[0]
        col += diff[1]
        count += 1

    row = position[0] - diff[0]
    col = position[1] - diff[1]
    while True:
        if row < 0 or col < 0 or row >= N or col >= N or field[row][col] != mark:
            break
        row -= diff[0]
        col -= diff[1]
        count += 1

    return count


# Returns the Manhattan distance from |a| to |b|.
def GetDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# =============================================================================
# DO NOT EDIT FOLLOWING FUNCTIONS
# =============================================================================

def main():
    field = Input()
    position = Think(field)
    Output(position)


def Input():
    field = [list(input()) for i in range(N)]
    return field


def Output(position):
    print(position[0], position[1])


# Outputs |msg| to stderr; This is actually a thin wrapper of print().
def DebugPrint(*msg):
    import sys
    print(*msg, file=sys.stderr)


if __name__    == '__main__':
    main()
