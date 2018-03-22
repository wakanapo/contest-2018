#include <cmath>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static const int N = 15;  // Size of field

using Field = vector<string>;
struct Position {
  int row;
  int col;
};

// Forward declartions of library functions.
bool CanGetFiveStones(const Field&, const Position&);
int CountStones(const Field&, const Position&, int, int);
int GetDistance(const Position&, const Position&);

// The main routine of AI.
Position Think(const Field& field) {
  static const Position kCenter {N / 2, N / 2};
  Position best_position = {0, 0};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      const char c = field[i][j];
      if (c != '.')
        continue;

      Position position = {i, j};
      if (CanGetFiveStones(field, position))
        return position;

      if (GetDistance(best_position, kCenter) > GetDistance(position, kCenter))
        best_position = position;
    }
  }
  return best_position;
}

// Returns true if you can get five stones from |position|. Returns false otherwise.
bool CanGetFiveStones(const Field& field, const Position& position) {
  // Checks all 8 directions.
  return (CountStones(field, position, -1, -1) + CountStones(field, position, 1, 1) + 1 >= 5 ||
          CountStones(field, position, -1, 0) + CountStones(field, position, 1, 0) + 1 >= 5 ||
          CountStones(field, position, -1, 1) + CountStones(field, position, 1, -1) + 1 >= 5 ||
          CountStones(field, position, 0, -1) + CountStones(field, position, 0, 1) + 1 >= 5);
}

// Returns the number of stones on the direction (|dr|, |dc|) from the next position of |position|.
int CountStones(const Field& field, const Position& position, int dr, int dc) {
  for (int count = 1;; ++count) {
    int row = position.row + count * dr, col = position.col + count * dc;
    if (row < 0 || col < 0 || row >= N || col >= N || field[row][col] != 'O') {
      return count - 1;
    }
  }
}

// Returns the Manhattan distance from |a| to |b|.
int GetDistance(const Position& a, const Position& b) {
  return abs(a.row - b.row) + abs(a.col - b.col);
}

// ============================================================================
// DO NOT EDIT FOLLOWING FUNCTIONS
// ============================================================================

Field Input(){
  Field field(N);
  for (int i = 0; i < N; ++i) {
    cin >> field[i];
  }
  return field;
}

void Output(const Position& position) {
  cout << position.row << " " << position.col << endl;
}

int main() {
  const Field field = Input();
  const Position position = Think(field);
  Output(position);
  return 0;
}
