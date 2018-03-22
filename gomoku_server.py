#!/usr/bin/python2

import os
import sys
import subprocess

class Game(object):
  N = 15
  NUM_PLAYERS = 2

  def __init__(self):
    self.board_ = [[0] * Game.N for _ in xrange(Game.N)]
    self.playing_id_ = 1
    self.passes_ = 0

  def get_state(self, id):
    return '\n'.join([''.join([self.get_stone(i, j, id) for j in xrange(Game.N)])
                      for i in xrange(Game.N)]) + '\n'

  def get_stone(self, i, j, c):
    if i not in xrange(Game.N) or j not in xrange(Game.N):
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
    for i in xrange(Game.N):
      for j in xrange(Game.N):
        c = self.board_[i][j]
        if c == 0:
          continue
        if (all(self.get_stone(i+k, j, c) == 'O' for k in xrange(5)) or
            all(self.get_stone(i, j+k, c) == 'O' for k in xrange(5)) or
            all(self.get_stone(i+k, j+k, c) == 'O' for k in xrange(5)) or
            all(self.get_stone(i+k, j-k, c) == 'O' for k in xrange(5))):
          return True
    return False


class Player(object):
  def __init__(self, id, ai):
    self.id_ = id
    self.command_ = ('java ' + ai) if ai[0].isupper() else ai

  def play(self, game):
    state = game.get_state(self.id)
    child = subprocess.Popen(self.command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=True)
    place = child.communicate(state)[0]
    return map(int, place.strip().split(' '))

  @property
  def id(self):
    return self.id_

  @property
  def command(self):
    return self.command_


class Gomoku(object):
  def __init__(self, ai):
    self.players_ = [Player(i + 1, ai[i]) for i in [0, 1]]
    self.game_ = Game()

  def run_game(self):
    winner = self.run_loop()
    if winner.id > 0:
      print '%s won the game' % winner.command
    else:
      print 'Draw game'

  def run_loop(self):
    game = self.game_
    while True:
      for player in self.players_:
        place = player.play(game)
        if game.put_stone(place):
          # Dump board state from 1st player's view
          print game.get_state(1)
          # Wins the game
          if game.is_over():
            return player
        else:
          print 'Pass'
          if not game.play_pass():
            # draw game
            return Player(0, '')


# Compile source code if needed, and returns the command to launch the program.
def Compile(filename):
  basepath, ext = os.path.splitext(filename)
  basename = os.path.basename(basepath)
  if ext in ('.cc', '.cpp'):
    # C++
    subprocess.call(['g++', '-O3', '-W', '-std=c++14', '-o', basename, filename])
    return './' + basename
  elif ext == '.java':
    # Java
    subprocess.call(['javac', '-d', '.', filename])
    return basename
  elif ext == '.py':
    # Python
    return filename
  raise ValueError('Unknown extension: %s' % ext)


def main():
  if len(sys.argv) != 3:
    print >> sys.stderr, 'Usage: %s <code1> <code2>' % sys.argv[0]
    return
  ai = [Compile(filename) for filename in sys.argv[1:]]
  gomoku = Gomoku(ai)
  gomoku.run_game()


if __name__ == '__main__':
  main()
