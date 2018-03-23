#!/usr/bin/python3

N = 15

# The main routine of AI.
# input: str[N] field : state of the field.
# output: int[2] : where to put a stone in this turn.
def Think(field):
  CENTER = (int(N / 2), int(N / 2))

  best_position = (0, 0)
  for i in range(N):
    for j in range(N):
      if field[i][j] != '.':
        continue

      position = (i, j)
      # Assume to put a stone on (i, j).
      field[i][j] = 'O'
      if DoHaveFiveStones(field, position):
        return position
      field[i][j] = '.'
      if GetDistance(best_position, CENTER) > GetDistance(position, CENTER):
        best_position = position
  return best_position

# Returns true if you have a five-stones line from |position|. Returns false otherwise.
def DoHaveFiveStones(field, position):
  return (CountStonesOnLine(field, position, (1, 1)) >= 5 or
          CountStonesOnLine(field, position, (1, 0)) >= 5 or
          CountStonesOnLine(field, position, (1, -1)) >= 5 or
          CountStonesOnLine(field, position, (0, 1)) >= 5)

# Returns the number of stones on the line segment on the direction of |diff| from |position|.
def CountStonesOnLine(field, position, diff):
  count = 0

  row = position[0]
  col = position[1]
  while True:
    if row < 0 or col < 0 or row >= N or col >= N or field[row][col] != 'O':
      return count
    row += diff[0]
    col += diff[1]
    count += 1

  row = position[0] - diff[0]
  col = position[1] - diff[1]
  while True:
    if row < 0 or col < 0 or row >= N or col >= N or field[row][col] != 'O':
      return count
    row -= diff[0]
    col -= diff[1]
    count += 1

  return -1

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

if __name__  == '__main__':
  main()
