from calculate import *

def player_move(aboard):
    while True:
        try:
            move = input('Enter your move: \n')
            aboard.push_san(move)
            break
        except ValueError:
            print ("Illegal move! Please try aggain.")

    return aboard


def playGame():
    moveTotal = 0
    board = AugmentedBoard()
    depth = input("Enter search depth: \n")
    depth = int(depth)
    while not board.is_game_over():
        print(board)
        if moveTotal % 2 == 1:
            board = player_move(board)
        else:
            board = computerMove(board, depth)
        moveTotal = moveTotal + 1

    print(board)
    print("Game is over")


def return_move(fen_str, depth = 2):
    board = AugmentedBoard(fen=fen_str)
    json_return =  return_move_json(board, depth)
    return json_return

#playGame()