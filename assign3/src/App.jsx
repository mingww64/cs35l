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
    // If the player has a piece in the center
    if (squares[4] === player) {
      const tmpSquares = squares.slice();
      // Check adjacent squares for empty spots
      const adjacentToCenter = [0, 1, 2, 3, 5, 6, 7, 8];
      for (let to of adjacentToCenter) {
        if (!squares[to]) {
          // Try moving to this position
          tmpSquares[4] = null;
          tmpSquares[to] = player;
          if (calculateWinner(tmpSquares)) {
            return false; // Found a winning move, can stay in center
          }
          // Reset for next iteration
          tmpSquares[4] = player;
          tmpSquares[to] = null;
        }
      }
      return true; // Must move from center as no winning move is available
    }
    return false; // No piece in center
  }

  function handleClick(i) {
    if (calculateWinner(squares)) {
      return;
    }

    const nextMove = xIsNext ? 'X' : 'O';
    const pieces = countPlayerPieces(nextMove);

    // Moving phase (after placing 3 pieces)
    if (pieces === 3) {
      if (selectedPiece === null) {
        // Selecting a piece to move
        if (squares[i] === nextMove) {
          // If player has a piece in center and it's not selected, they must select it
          if (mustMoveFromCenter(nextMove) && squares[4] === nextMove && i !== 4) {
            return;
          }
          setSelectedPiece(i);
        }
      } else {
        // A piece is already selected (at `selectedPiece`). User clicked `i`.

        // Case 1: User clicked on one of their *own* pieces (to change selection)
        if (squares[i] === nextMove) {
          // Check the 'mustMoveFromCenter' rule for the *new* piece
          if (mustMoveFromCenter(nextMove) && squares[4] === nextMove && i !== 4) {
            // Invalid new selection. Deselect the *original* piece.
            setSelectedPiece(null);
            return;
          }
          // Otherwise, it's a valid new piece to select.
          setSelectedPiece(i);
          return; // Exit.
        }

        // Case 2: User clicked on a valid, empty, adjacent square (a valid move)
        if (!squares[i] && isAdjacent(selectedPiece, i)) {
          const nextSquares = squares.slice();
          
          // Handle the center piece movement
          if (selectedPiece === 4 && mustMoveFromCenter(nextMove)) {
            // Always allow moving from center when it's required
            nextSquares[selectedPiece] = null;
            nextSquares[i] = nextMove;
            setSquares(nextSquares);
            setSelectedPiece(null);
            setXIsNext(!xIsNext);
            return;
          } else if (selectedPiece !== 4 || !mustMoveFromCenter(nextMove)) {
            // Handle non-center pieces or when center move isn't required
            nextSquares[selectedPiece] = null;
            nextSquares[i] = nextMove;
            setSquares(nextSquares);
            setSelectedPiece(null);
            setXIsNext(!xIsNext);
            return;
          }
        }
        
        // Case 3: Invalid move (clicked opponent, non-adjacent, etc.)
        // Deselect the piece.
        setSelectedPiece(null);
      }
      return;
    }

    // Placing phase (first 3 pieces)
    if (!squares[i]) {
      const nextSquares = squares.slice();
      nextSquares[i] = nextMove;
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
