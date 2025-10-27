import { useState } from 'react';

function Square({value, onSquareClick, isSelected}) {
  return (
    <button 
      className={`square ${isSelected ? 'selected' : ''}`} 
      onClick={onSquareClick}
    >
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [moveCount, setMoveCount] = useState(0);
  const [selectedPiece, setSelectedPiece] = useState(null);

  function countPlayerPieces(player) {
    return squares.filter(square => square === player).length;
  }

  function isAdjacent(from, to) {
    const adjacentSquares = {
      0: [1, 3, 4],
      1: [0, 2, 3, 4, 5],
      2: [1, 4, 5],
      3: [0, 1, 4, 6, 7],
      4: [0, 1, 2, 3, 5, 6, 7, 8],
      5: [1, 2, 4, 7, 8],
      6: [3, 4, 7],
      7: [3, 4, 5, 6, 8],
      8: [4, 5, 7]
    };
    return adjacentSquares[from].includes(to);
  }

  function mustMoveFromCenter(player) {
    // If the player does not have a piece in the center, rule doesn't apply
    if (squares[4] !== player) {
      return { mustMove: false };
    }

    // Check if any piece can make a winning move
    for (let from = 0; from < 9; from++) {
      if (squares[from] === player) {
        const tmpSquares = squares.slice();
        for (let to = 0; to < 9; to++) {
          if (!squares[to] && isAdjacent(from, to)) {
            tmpSquares[from] = null;
            tmpSquares[to] = player;
            if (calculateWinner(tmpSquares)) {
              return { mustMove: false, winningMove: { from, to } };
            }
            tmpSquares[from] = player;
            tmpSquares[to] = null;
          }
        }
      }
    }
    // No winning move found with any piece, must move from center
    return { mustMove: true };
  }

  function handleClick(i) {
    if (calculateWinner(squares)) {
      return;
    }

    const playerSwitch = xIsNext ? 'X' : 'O';
    const pieces = countPlayerPieces(playerSwitch);

    // Moving phase (after placing 3 pieces)
    if (pieces === 3) {
      const moveStatus = mustMoveFromCenter(playerSwitch);

      if (selectedPiece === null) {
        // Selecting a piece to move
        if (squares[i] === playerSwitch) {
          if (moveStatus.mustMove && i !== 4) {
            setSelectedPiece(null);
            return;
          }
          setSelectedPiece(i);
        }
      } else {
        // A piece is already selected (at `selectedPiece`). User clicked `i`.

        // Case 1: User clicked on one of their *own* pieces to change selection
        if (squares[i] === playerSwitch) {
          setSelectedPiece(i);
          return;
        }

        // Case 2: User clicked on a valid, empty, adjacent square
        if (!squares[i] && isAdjacent(selectedPiece, i)) {
          // If a winning move exists, only allow that move or moving from center
          if (moveStatus.winningMove) {
            if (
              (selectedPiece === moveStatus.winningMove.from && i === moveStatus.winningMove.to) ||
              selectedPiece === 4
            ) {
              const nextSquares = squares.slice();
              nextSquares[selectedPiece] = null;
              nextSquares[i] = playerSwitch;
              setSquares(nextSquares);
              setSelectedPiece(null);
              setXIsNext(!xIsNext);
              return;
            } else {
              setSelectedPiece(null);
              return;
            }
          }

          // Otherwise, allow any valid move
          const nextSquares = squares.slice();
          nextSquares[selectedPiece] = null;
          nextSquares[i] = playerSwitch;
          setSquares(nextSquares);
          setSelectedPiece(null);
          setXIsNext(!xIsNext);
          return;
        }
        // Case 3: Invalid move (clicked opponent, non-adjacent, etc.)
        setSelectedPiece(null);
      }
      return;
    }

    // Placing phase (first 3 pieces)
    if (!squares[i]) {
      const nextSquares = squares.slice();
      nextSquares[i] = playerSwitch;
      setSquares(nextSquares);
      setMoveCount(moveCount + 1);
      setXIsNext(!xIsNext);
    }
  }

  const winner = calculateWinner(squares);
  const currentPlayer = xIsNext ? 'X' : 'O';
  const playerPieces = countPlayerPieces(currentPlayer);
  
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else if (selectedPiece !== null) {
    status = `${currentPlayer}'s turn: Select destination square`;
  } else if (playerPieces === 3) {
    if (mustMoveFromCenter(currentPlayer) && squares[4] === currentPlayer) {
      status = `${currentPlayer}'s turn: Must move from center`;
    } else {
      status = `${currentPlayer}'s turn: Select a piece to move`;
    }
  } else {
    status = `Next player: ${currentPlayer}`;
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square 
          value={squares[0]} 
          onSquareClick={() => handleClick(0)}
          isSelected={selectedPiece === 0}
        />
        <Square 
          value={squares[1]} 
          onSquareClick={() => handleClick(1)}
          isSelected={selectedPiece === 1}
        />
        <Square 
          value={squares[2]} 
          onSquareClick={() => handleClick(2)}
          isSelected={selectedPiece === 2}
        />
      </div>
      <div className="board-row">
        <Square 
          value={squares[3]} 
          onSquareClick={() => handleClick(3)}
          isSelected={selectedPiece === 3}
        />
        <Square 
          value={squares[4]} 
          onSquareClick={() => handleClick(4)}
          isSelected={selectedPiece === 4}
        />
        <Square 
          value={squares[5]} 
          onSquareClick={() => handleClick(5)}
          isSelected={selectedPiece === 5}
        />
      </div>
      <div className="board-row">
        <Square 
          value={squares[6]} 
          onSquareClick={() => handleClick(6)}
          isSelected={selectedPiece === 6}
        />
        <Square 
          value={squares[7]} 
          onSquareClick={() => handleClick(7)}
          isSelected={selectedPiece === 7}
        />
        <Square 
          value={squares[8]} 
          onSquareClick={() => handleClick(8)}
          isSelected={selectedPiece === 8}
        />
      </div>
    </>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
