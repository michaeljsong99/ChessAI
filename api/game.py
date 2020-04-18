from calculate import *

def player_move(aboard):
    while True:
        try:
            move = input('Enter your move: \n')
            aboard.push_san(move)
            break
        except ValueError:
            print ("Illegal move! Please try again.")

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

# Test mate in 2.
#return_move("6k1/4r3/5r2/8/8/8/8/6K1 b - - 0 1")

# Test mate in 2 (first move no check). (White to Move)
# TODO: This currently works on Depth 3, but not Depth 2
#return_move("4n1k1/5p2/5Pp1/p5Q1/7R/8/6K1/8 w - - 0 1")

# Test mate in 3 (all checks).
#return_move("6k1/6pr/6N1/5q2/B7/3N1pP1/3N1P2/6K1 b - - 0 1")

# Test: TODO: Taking things with check!
#return_move("r1bq2kr/pppp3p/2n1pp1B/7Q/4P1p1/2P5/PPP1BPPP/R3K2R w - - 0 1")

# Test
#return_move("r1bk3r/ppp1bp1p/6p1/3n4/3PQ3/2P5/PP3PPP/RN2K1NR b - - 0 1")

# TODO: The engine randomly sacs its queen here - why?
#return_move("r2q1n2/7r/2Q1pnk1/3p1p2/p2P1B2/8/PPP3PP/R3R1K1 w - - 0 1")

# Test: What is the evaluation of this position?
#return_move("Q2q1n2/7r/4pnk1/3p1p2/p2PPB2/8/PPP3PP/R3R1K1 b - - 0 1", depth=1)


#board = AugmentedBoard()
#print(board)
#print('Number of Attackers: ' + str(len(board.attackers(color=chess.WHITE, square=chess.B3))))


#playGame()