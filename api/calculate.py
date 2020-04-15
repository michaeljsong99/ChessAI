import chess.polyglot # Opening book
from AugmentedBoard import AugmentedBoard


def choose_move(aboard, depth):
    try:
        move = chess.polyglot.MemoryMappedReader("Performance.bin").weighted_choice(aboard).move
        evaluation = 'Still in Opening Book'
        return (evaluation, move)
    except:
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in aboard.legal_moves:
            aboard.push(move)
            board_value = -alphabeta(-beta, -alpha, depth-1, aboard)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            if board_value > alpha:
                alpha = board_value
            aboard.pop()
        return (best_value, best_move)


def alphabeta(alpha, beta, depth, aboard):

    # First, check to see if the position is already in our cached positions.
    position_as_bits = aboard.bitify_position()
    lookup = aboard.lookup_position(depth, position_as_bits)
    if lookup is not None:
        return lookup

    best_value = -9999
    if depth == 0:
        return evaluate(alpha, beta, aboard)

    for move in aboard.legal_moves:
        aboard.push(move)
        score = -alphabeta(-beta, -alpha, depth-1, aboard)
        aboard.pop()

        if score >= beta:
            return score
        if score > best_value:
            best_value = score
        if score > alpha:
            alpha = score

    # Add the depth and position and evaluation to our cached positions.
    aboard.add_to_cache(depth, position_as_bits, best_value)

    return best_value


def evaluate(alpha, beta, aboard):

    if aboard.is_checkmate():
        if aboard.turn:
            return -9999 # White has been mated.
        else:
            return 9999 # Blakc has been mated.
    if aboard.is_stalemate() or aboard.is_insufficient_material() or aboard.can_claim_draw(): # Game is drawn.
        return 0

    current_eval = aboard.evaluation()

    if current_eval >= beta:
        return beta

    if alpha < current_eval:
        alpha = current_eval

    # Now we need to check if there are any captures that can be made, so we don't cut off too soon.
    for move in aboard.legal_moves:
        if aboard.is_capture(move): # Consider all "reasonable captures".
            if aboard.is_valid_capture(move):
                aboard.push(move)
                score = -evaluate(-beta, -alpha, aboard)
                aboard.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
    return alpha


def computerMove(aboard, depth):
    best_move = choose_move(aboard, depth)[1]
    evaluation = choose_move(aboard, depth)[0]
    print ('Best move is ' + str(best_move) + ' and evaluation is: ' + str(evaluation))
    aboard.push(best_move)
    # Now we need to clear the cache for the board.
    aboard.reset_cache()

    return aboard






