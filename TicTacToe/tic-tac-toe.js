const readline = require('readline');

// Helper function to get input from user
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function printBoard(board) {
  board.forEach(row => {
    console.log(row.join(" | "));
    console.log("---------");
  });
}

function checkWinner(board, player) {
  // Check rows and columns
  for (let i = 0; i < 3; i++) {
    if (
      board[i].every(cell => cell === player) ||
      board.map(row => row[i]).every(cell => cell === player)
    ) {
      return true;
    }
  }

  // Check diagonals
  if (
    [0, 1, 2].every(i => board[i][i] === player) ||
    [0, 1, 2].every(i => board[i][2 - i] === player)
  ) {
    return true;
  }

  return false;
}

function isDraw(board) {
  return board.flat().every(cell => cell !== " ");
}

function getAvailableMoves(board) {
  const moves = [];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      if (board[i][j] === " ") {
        moves.push([i, j]);
      }
    }
  }
  return moves;
}

function ask(question) {
  return new Promise(resolve => rl.question(question, answer => resolve(answer)));
}

async function playGame() {
  const board = Array.from({ length: 3 }, () => Array(3).fill(" "));
  const players = ["X", "O"];
  let currentPlayer = players[Math.floor(Math.random() * 2)];

  console.log("Welcome to Tic-Tac-Toe!");
  printBoard(board);

  while (true) {
    console.log(`${currentPlayer}'s turn`);

    let input = await ask("Enter row and column (0-2) separated by space: ");
    let [row, col] = input.trim().split(" ").map(Number);

    if (!board[row] || board[row][col] !== " ") {
      console.log("Invalid move. Try again.");
      console.log("Available moves:", getAvailableMoves(board));
      continue;
    }

    board[row][col] = currentPlayer;
    printBoard(board);

    if (checkWinner(board, currentPlayer)) {
      console.log(`${currentPlayer} wins!`);
      break;
    }

    if (isDraw(board)) {
      console.log("It's a draw!");
      break;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
  }

  rl.close();
}

playGame();
