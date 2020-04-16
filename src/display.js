import Chess from  "chess.js" // if recieving an error about new Chess() not being a constructor
import React, { Component } from "react";
import Chessboard from "chessboardjsx";

class Display extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        console.log(this.props.evaluation)
        return (
            <div>
                <Chessboard
                    id={this.props.id}
                    width={this.props.width}
                    position={this.props.position}
                    onDrop={this.props.onDrop}
                    onMouseOverSquare={this.props.onMouseOverSquare}
                    onMouseOutSquare={this.props.onMouseOutSquare}
                    boardStyle={this.props.boardStyle}
                    squareStyles={this.props.squareStyles}
                    dropSquareStyle={this.props.dropSquareStyle}
                    onDragOverSquare={this.props.onDragOverSquare}
                    onSquareClick={this.props.onSquareClick}
                    onSquareRightClick={this.props.onSquareRightClick}
                />
                <p>{this.props.current_message}</p>
                <p>Current evaluation: {this.props.evaluation.toFixed(2).toString()}</p>
            </div>
        )
    }
}


export default Display;