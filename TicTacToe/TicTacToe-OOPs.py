from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

# ---------- Core Enums & Data Types ----------

class Mark(Enum):
    X = "X"
    O = "O"

class GameState(Enum):
    ONGOING = auto()
    DRAW = auto()
    X_WINS = auto()
    O_WINS = auto()

@dataclass(frozen=True)
class Move:
    row: int
    col: int
    mark: Mark

# ---------- Optimized Game Engine ----------

class FastRulesGame:
    """
    Tic-Tac-Toe game engine (3x3) with O(1) win check using counters.
    Supports Human vs Human.
    """
    def __init__(self, n: int = 3):
        self.n = n
        self.board = [[None for _ in range(n)] for _ in range(n)]
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0
        self.anti_diag = 0
        self.move_count = 0
        self.state = GameState.ONGOING
        self.current = Mark.X  # X always starts

    def play(self, move: Move) -> GameState:
        if self.state != GameState.ONGOING:
            raise ValueError("Game already finished")

        r, c = move.row, move.col
        if not (0 <= r < self.n and 0 <= c < self.n):
            raise ValueError("Move out of bounds")
        if self.board[r][c] is not None:
            raise ValueError("Cell already occupied")

        # Place the move
        self.board[r][c] = move.mark
        self.move_count += 1

        # Use +1 for X, -1 for O
        delta = 1 if move.mark == Mark.X else -1
        self.rows[r] += delta
        self.cols[c] += delta
        if r == c:
            self.diag += delta
        if r + c == self.n - 1:
            self.anti_diag += delta

        # Check win in O(1)
        if self.rows[r] == self.n or self.cols[c] == self.n or self.diag == self.n or self.anti_diag == self.n:
            self.state = GameState.X_WINS
        elif self.rows[r] == -self.n or self.cols[c] == -self.n or self.diag == -self.n or self.anti_diag == -self.n:
            self.state = GameState.O_WINS
        elif self.move_count == self.n * self.n:
            self.state = GameState.DRAW

        # Switch player
        self.current = Mark.O if self.current == Mark.X else Mark.X

        return self.state

    def __str__(self):
        return "\n".join(" | ".join(cell.value if cell else " " for cell in row) for row in self.board)

# ---------- Driver Code ----------

def cli_driver():
    game = FastRulesGame(n=3)
    print("Starting Tic-Tac-Toe (3x3, Human vs Human). Coordinates are 0-indexed.")
    print(game)

    while game.state == GameState.ONGOING:
        try:
            move_input = input(f"Player {game.current.value}, enter move as 'row col': ")
            r, c = map(int, move_input.split())
            move = Move(r, c, game.current)
            state = game.play(move)
            print("\n" + str(game) + "\n")

            if state == GameState.X_WINS:
                print("Player X wins! 🎉")
            elif state == GameState.O_WINS:
                print("Player O wins! 🎉")
            elif state == GameState.DRAW:
                print("It's a draw 🤝")

        except Exception as e:
            print(f"Invalid move: {e}. Try again.\n")

if __name__ == "__main__":
    cli_driver()
