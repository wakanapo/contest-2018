#!/usr/bin/python3

import os
import sys
import subprocess

class Game(object):
  N = 15
  NUM_PLAYERS = 2

  def __init__(self):
    self.board_ = [[0] * Game.N for _ in range(Game.N)]
    self.playing_id_ = 1
    self.passes_ = 0

  def get_state(self, id):
    return '\n'.join([''.join([self.get_stone(i, j, id) for j in range(Game.N)])
                      for i in range(Game.N)]) + '\n'

  def get_stone(self, i, j, c):
    if i not in range(Game.N) or j not in range(Game.N):
      return ' '
    b = self.board_[i][j]
    return '.' if b is 0 else 'O' if b == c else 'X'

  def put_stone(self, place):
    i, j = place[0], place[1]
    if i < 0 or j < 0 or i >= Game.N or j >= Game.N or self.board_[i][j] != 0:
      return False
    self.board_[i][j] = self.playing_id_
    self.next_turn()
    self.passes_ = 0
    return True

  def play_pass(self):
    self.next_turn()
    self.passes_ += 1
    return self.passes_ < Game.NUM_PLAYERS

  def next_turn(self):
    self.playing_id_ = self.playing_id_ % Game.NUM_PLAYERS + 1

  def is_over(self):
    for i in range(Game.N):
      for j in range(Game.N):
        c = self.board_[i][j]
        if c == 0:
          continue
        if (all(self.get_stone(i+k, j, c) == 'O' for k in range(5)) or
            all(self.get_stone(i, j+k, c) == 'O' for k in range(5)) or
            all(self.get_stone(i+k, j+k, c) == 'O' for k in range(5)) or
            all(self.get_stone(i+k, j-k, c) == 'O' for k in range(5))):
          return True
    return False


class Player(object):
  def __init__(self, id, filepath):
    self.id_ = id
    self.path_ = filepath

  def play(self, game):
    state = game.get_state(self.id)
    child = subprocess.Popen(self.command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=True)
    place = child.communicate(state.encode())[0]
    return list(map(int, place.strip().split(b' ')))

  @property
  def id(self):
    return self.id_

  @property
  def path(self):
    return self.path_

  @property
  def command(self):
    return 'python3 ' + self.path


class Gomoku(object):
  def __init__(self, ai):
    self.players_ = [Player(i + 1, ai[i]) for i in [0, 1]]
    self.game_ = Game()

  def run_game(self):
    winner = self.run_loop()
    if winner.id > 0:
      print('{0} won the game'.format(winner.path))
    else:
      print('Draw game')

  def run_loop(self):
    game = self.game_
    while True:
      for player in self.players_:
        place = player.play(game)
        if game.put_stone(place):
          # Dump board state from 1st player's view
          print(game.get_state(1))
          # Wins the game
          if game.is_over():
            return player
        else:
          print('Pass')
          if not game.play_pass():
            # draw game
            return Player(0, '')


def main():
  if len(sys.argv) == 1:
    print("""
Usage:
 {0} player1 player2
    player1 and player2 are names of pythoncode, e.g. gomoku.py.
    player1 works as the firsr-hand player, and player2 works as the second-hand player.
    If you ommit player2, we assume 'gomoku.py' as player2.""".format(sys.argv[0]),
          file=sys.stderr)
    return
  ai = [filename for filename in sys.argv[1:]]
  if len(ai) < 2:
    ai.append('gomoku.py')
  gomoku = Gomoku(ai)
  gomoku.run_game()


if __name__ == '__main__':
  main()
