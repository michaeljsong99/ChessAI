import React, { Component } from "react";
import PropTypes from "prop-types";
import Chess from  "chess.js" // if recieving an error about new Chess() not being a constructor
import Display from "./display.js";

class HumanVsCPU extends Component {
  static propTypes = { children: PropTypes.func };

  state = {
    fen: "start",
    // square styles for active drop square
    dropSquareStyle: {},
    // custom square styles
    squareStyles: {},
    // square with the currently clicked piece
    pieceSquare: "",
    // currently clicked square
    square: "",
    // array of past game moves
    history: [],
    // current evaluation of the position
    evaluation: 0,
    player_can_move: true,
    current_message: 'Your turn!',
    width: window.innerWidth,
    height: window.innerHeight,
    board_width: window.innerWidth,
  };

  componentDidMount() {
    this.game = new Chess();
    window.addEventListener("resize", this.updateWindowDimensions);
    this.updateWindowDimensions();
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateWindowDimensions)
  }

  updateWindowDimensions = () => {
    this.setState({width: window.innerWidth,
                   height: window.innerHeight});
    this.getBoardWidth();
    console.log("Resizing!");
    console.log(this.state.board_width);
  }

  getBoardWidth = () => {
    const min_dimension = Math.min(this.state.width * 0.8, this.state.height * 0.8)
    const board_width = Math.min(min_dimension, 700)
    this.setState({
      board_width: board_width
    });
  };

  // To restart the game.
  restartGame() {
      this.game = new Chess();
  }
  
  // Call the Python API - pass in the FEN string.
  calculateMove () {
    this.setState({
        player_can_move: false
    })
    const position  = this.game.fen();
    const url = 'https://young-coast-75480.herokuapp.com/api/calculate/?position=' + position
    console.log(url)
    fetch(url)
    .then(res => res.json())
    .then(data => {
        let move=this.game.move(
            data.move
        )
        if (this.game.game_over() === true) {
            console.log('GAME OVER')
            let message = 'Game Drawn!';
            let evaluation = 0;
            if (this.game.in_checkmate()) {
                message = 'Aww... You lost. :('
                if (this.game.turn() === 'w') evaluation = -100;
                else evaluation = 100;
            }
            this.setState({
                evaluation: evaluation,
                current_message: message,
                fen: this.game.fen(),
                history: this.game.history({ verbose: true }),
            })
            return;
        }
        // illegal move
        if (move=== null) console.log('Null Move')
        if (move === null) return;
        this.setState(({ history, pieceSquare }) => ({
            fen: this.game.fen(),
            evaluation: data.evaluation,
            history: this.game.history({ verbose: true }),
            player_can_move: true, // Allow the player to move again.
            current_message: 'Your turn!',
            squareStyles: squareStyling({ pieceSquare, history })
        }));
    })
  }

  // keep clicked square style and remove hint squares
  removeHighlightSquare = () => {
    this.setState(({ pieceSquare, history }) => ({
      squareStyles: squareStyling({ pieceSquare, history })
    }));
  };

  // show possible moves
  highlightSquare = (sourceSquare, squaresToHighlight) => {
    const highlightStyles = [sourceSquare, ...squaresToHighlight].reduce(
      (a, c) => {
        return {
          ...a,
          ...{
            [c]: {
              background:
                "radial-gradient(circle, #fffc00 25%, transparent 40%)",
              borderRadius: "10%"
            }
          },
          ...squareStyling({
            history: this.state.history,
            pieceSquare: this.state.pieceSquare
          })
        };
      },
      {}
    );

    this.setState(({ squareStyles }) => ({
      squareStyles: { ...squareStyles, ...highlightStyles }
    }));
  };

  onDrop = ({ sourceSquare, targetSquare }) => {
    if (this.state.player_can_move === false) return;
    // see if the move is legal
    let move = this.game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q" // always promote to a queen for example simplicity
    });
    
    // illegal move
    if (move === null) return;
    this.setState(({ history, pieceSquare }) => ({
      fen: this.game.fen(),
      history: this.game.history({ verbose: true }),
      current_message: 'Computer is thinking...',
      squareStyles: squareStyling({ pieceSquare, history })
    }));
    // Check if the game is over.
    if (this.game.game_over() === true) {
        console.log('GAME OVER')
        let message = 'Game Drawn!';
        let evaluation = 0;
        if (this.game.in_checkmate()) {
            message = 'Congratulations! You won! :D'
            if (this.game.turn() === 'w') evaluation = -100;
            else evaluation = 100;
        }
        this.setState({
            evaluation: evaluation,
            current_message: message,
            fen: this.game.fen(),
            history: this.game.history({ verbose: true }),
        })
        return;
    }
    // Otherwise, have the engine calculate the move.
    this.calculateMove()
  };

  onMouseOverSquare = square => {
    // get list of possible moves for this square
    let moves = this.game.moves({
      square: square,
      verbose: true
    });

    // exit if there are no moves available for this square
    if (moves.length === 0) return;

    let squaresToHighlight = [];
    for (var i = 0; i < moves.length; i++) {
      squaresToHighlight.push(moves[i].to);
    }

    this.highlightSquare(square, squaresToHighlight);
  };

  onMouseOutSquare = square => this.removeHighlightSquare(square);

  // central squares get diff dropSquareStyles
  onDragOverSquare = square => {
    this.setState({
      dropSquareStyle:
        square === "e4" || square === "d4" || square === "e5" || square === "d5"
          ? { backgroundColor: "cornFlowerBlue" }
          : { boxShadow: "inset 0 0 1px 4px rgb(255, 255, 0)" }
    });
  };

  onSquareClick = square => {
    this.setState(({ history }) => ({
      squareStyles: squareStyling({ pieceSquare: square, history }),
      pieceSquare: square
    }));
    if (this.state.player_can_move === false) return;
    let move = this.game.move({
      from: this.state.pieceSquare,
      to: square,
      promotion: "q" // always promote to a queen for example simplicity
    });
    // illegal move
    if (move === null) return;

    this.setState({
      fen: this.game.fen(),
      current_message: 'Computer is thinking...',
      history: this.game.history({ verbose: true }),
      pieceSquare: ""
    });
    if (this.game.game_over() === true) {
        console.log('GAME OVER')
        let message = 'Game Drawn!';
        let evaluation = 0;
        if (this.game.in_checkmate()) {
            message = 'Congratulations! You won! :D'
            if (this.game.turn() === 'w') evaluation = -100;
            else evaluation = 100;
        }
        this.setState({
            evaluation: evaluation,
            current_message: message,
            fen: this.game.fen(),
            history: this.game.history({ verbose: true }),
        })
        return;
    }
    this.calculateMove();
  };

  onSquareRightClick = square =>
    this.setState({
      squareStyles: { [square]: { backgroundColor: "deepPink" } }
    });

  render() {
    const { fen, dropSquareStyle, squareStyles, evaluation, current_message, board_width } = this.state;

    return this.props.children({
      squareStyles,
      position: fen,
      onMouseOverSquare: this.onMouseOverSquare,
      onMouseOutSquare: this.onMouseOutSquare,
      onDrop: this.onDrop,
      dropSquareStyle,
      onDragOverSquare: this.onDragOverSquare,
      onSquareClick: this.onSquareClick,
      onSquareRightClick: this.onSquareRightClick,
      evaluation,
      current_message,
      board_width
    });
  }
}

export default function WithMoveValidation() {
  return (
    <div>
      <HumanVsCPU>
        {({
          position,
          onDrop,
          onMouseOverSquare,
          onMouseOutSquare,
          squareStyles,
          dropSquareStyle,
          onDragOverSquare,
          onSquareClick,
          onSquareRightClick,
          evaluation,
          current_message,
          board_width
        }) => (
          <Display
            id="HumanVsCPU"
            width={board_width}
            position={position}
            onDrop={onDrop}
            onMouseOverSquare={onMouseOverSquare}
            onMouseOutSquare={onMouseOutSquare}
            boardStyle={{
              borderRadius: "5px",
              boxShadow: `0 5px 15px rgba(0, 0, 0, 0.5)`
            }}
            squareStyles={squareStyles}
            dropSquareStyle={dropSquareStyle}
            onDragOverSquare={onDragOverSquare}
            onSquareClick={onSquareClick}
            onSquareRightClick={onSquareRightClick}
            evaluation={evaluation}
            current_message={current_message}
          />
        )}
      </HumanVsCPU>
      
    </div>
  );
}

const squareStyling = ({ pieceSquare, history }) => {
  const sourceSquare = history.length && history[history.length - 1].from;
  const targetSquare = history.length && history[history.length - 1].to;

  return {
    [pieceSquare]: { backgroundColor: "rgba(255, 255, 0, 0.4)" },
    ...(history.length && {
      [sourceSquare]: {
        backgroundColor: "rgba(255, 255, 0, 0.4)"
      }
    }),
    ...(history.length && {
      [targetSquare]: {
        backgroundColor: "rgba(255, 255, 0, 0.4)"
      }
    })
  };
};