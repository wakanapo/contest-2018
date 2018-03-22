import java.util.*;
import java.lang.*;
import java.io.*;


public class Gomoku {
  static final int N = 15;  // size of field

  static class Position {
    Position(int r, int c) {
      row = r;
      col = c;
    }
    public int row;
    public int col;
  };

  // The main routine of AI.
  static Position Think(final String[] field) {
    final Position kCenter = new Position(N / 2, N / 2);
    Position best_position = new Position(0, 0);
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        final char c = field[i].charAt(j);
        if (c != '.')
          continue;

        Position position = new Position(i, j);
        if (CanGetFiveStones(field, position))
          return position;
        if (GetDistance(best_position, kCenter) > GetDistance(position, kCenter))
          best_position = position;
      }
    }
    return best_position;
  }

  // Returns true if you can get five stones from |position|. Returns false otherwise.
  static boolean CanGetFiveStones(final String[] field, final Position position) {
    // Checks all 8 directions.
    return (CountStones(field, position, -1, -1) + CountStones(field, position, 1, 1) + 1 >= 5 ||
        CountStones(field, position, -1, 0) + CountStones(field, position, 1, 0) + 1 >= 5 ||
        CountStones(field, position, -1, 1) + CountStones(field, position, 1, -1) + 1 >= 5 ||
        CountStones(field, position, 0, -1) + CountStones(field, position, 0, 1) + 1 >= 5);
  }

  // Returns the number of stones on the direction (|dr|, |dc|) from the next position of |position|.
  static int CountStones(final String[] field, final Position position, int dr, int dc) {
    for (int count = 1;; count++) {
      int row = position.row + count * dr, col = position.col + count * dc;
      if (row < 0 || col < 0 || row >= N || col >= N || field[row].charAt(col) != 'O') {
        return count - 1;
      }
    }
  }

  // Returns the Manhattan distance from |a| to |b|.
  static int GetDistance(final Position a, final Position b) {
    return Math.abs(a.row - b.row) + Math.abs(a.col - b.col);
  }

  // ============================================================================
  // DO NOT EDIT FOLLOWING FUNCTIONS
  // ============================================================================

  static String[] Input(){
    Scanner scanner = new Scanner(System.in);
    String field[] = new String[N];
    for (int i = 0; i < N; i++) {
      field[i] = scanner.next();
    }
    return field;
  }

  static void Output(final Position position) {
    System.out.println(position.row + " " + position.col);
  }

  public static void main(String args[]) {
    final String[] field = Input();
    final Position position = Think(field);
    Output(position);
  }
}
