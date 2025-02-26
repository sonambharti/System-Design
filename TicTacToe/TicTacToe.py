import random

def print_board(board):
    """Displays the current Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    """Checks if the given player has won the game."""
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """Checks if the game is a draw (no empty spaces left)."""
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def get_available_moves(board):
    """Returns a list of available moves."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def play_game():
    """Controls the flow of the game."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = random.choice(players)  # Randomly choose who starts
    
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    
    while True:
        print(f"{current_player}'s turn")
        row, col = map(int, input("Enter row and column (0-2) separated by space: ").split())
        
        if board[row][col] != " ":
            print("Invalid move. Try again.")
            continue
        
        board[row][col] = current_player
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"{current_player} wins!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = "X" if current_player == "O" else "O"  # Switch turns

if __name__ == "__main__":
    play_game()
