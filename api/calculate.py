import chess.polyglot # Opening book
from AugmentedBoard import AugmentedBoard


def choose_move(aboard, depth):
    try:
        move = chess.polyglot.MemoryMappedReader("Performance.bin").weighted_choice(aboard).move
        evaluation = 0
        return (evaluation, move)
    except:
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in aboard.legal_moves:
            # First, add the current position to our seen positions.
            position_as_bits = aboard.bitify_position()
            aboard.add_to_seen_positions(depth, position_as_bits)

            aboard.push(move)
            board_value = -alphabeta(-beta, -alpha, depth-1, aboard)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            if board_value > alpha:
                alpha = board_value
            aboard.pop()

            # Reset the seen positions
            aboard.reset_seen_positions()

            # Check: If the returned board_value was 9999, then there is a forced checkmate. We don't check other moves.
            if best_value == 9999:
                break
        return (best_value, best_move)


def alphabeta(alpha, beta, depth, aboard):

    # First, check to see if the position is already in our cached positions.
    position_as_bits = aboard.bitify_position()

    lookup = aboard.lookup_position(depth, position_as_bits)
    if lookup is not None and depth != 0:
        return lookup

    # Check if the current player is in checkmate or stalemate.
    if aboard.is_game_over():
        if aboard.is_checkmate(): # Current side is in checkmate.
            return -9999
        else:                   # Current side is in stalemate or there is a repetition.
            return 0

    # Now check to make sure we don't have a repetition.
    is_repetition = aboard.check_for_repetition(depth, position_as_bits)
    if is_repetition:
        return 0

    best_value = -9999
    if depth == 0:
        return evaluate(alpha, beta, aboard)

    # Now add the current position to our seen positions.
    aboard.add_to_seen_positions(depth, position_as_bits)

    for move in aboard.legal_moves:
        aboard.push(move)
        score = -alphabeta(-beta, -alpha, depth-1, aboard)
        aboard.pop()

        # If the score is 9999, then just return the score.
        if score >= beta or score == 9999:
            best_value = score
            break
        if score > best_value:
            best_value = score
        if score > alpha:
            alpha = score

    # Add the depth and position and evaluation to our cached positions.
    aboard.add_to_cache(depth, position_as_bits, best_value)

    return best_value


def evaluate(alpha, beta, aboard, must_mate=False):

    # Check the cached evaluations.
    position_as_bits = aboard.bitify_position()


    # TODO: Might need to uncomment this part. Potential for too many 0 evaluations
    lookup = aboard.lookup_position(0, position_as_bits)
    if lookup is not None:
        return lookup

    # Now check to make sure we don't have a repetition.
    is_repetition = aboard.check_for_repetition(0, position_as_bits)
    if is_repetition:
        return 0

    # Now add the current position to our seen positions.
    aboard.add_to_seen_positions(0, position_as_bits)

    # TODO: Not sure about the colors here. Current side has been mated.
    if aboard.is_checkmate():
        aboard.add_to_cache(0, position_as_bits, -9999)
        return -9999

    if aboard.is_stalemate() or aboard.is_insufficient_material() or aboard.can_claim_draw(): # Game is drawn.
        aboard.add_to_cache(0, position_as_bits, 0)
        return 0

    current_eval = aboard.evaluation()

    # If we are in check, we don't want to cut off the line too soon, as there could be a forced mate.
    in_check = False
    if aboard.is_check():
        in_check = True

    if current_eval >= beta:
        if not in_check:
            aboard.add_to_cache(0, position_as_bits, beta)
            return beta
        else:
            must_mate = True # The opponent must mate us. Otherwise they would not allow this position to happen.

    new_alpha = False
    if alpha < current_eval:
        alpha = current_eval
        new_alpha = True

    # Now we need to check if there are any captures that can be made, so we don't cut off too soon.
    for move in aboard.legal_moves:

        # First check: If our alpha is -9999 or +9999, it means we found a forced checkmate. We can stop calculating.
        if abs(alpha) == 9999:
            aboard.add_to_cache(0, position_as_bits, alpha)
            return alpha

        # First, if we are in check or our , consider all possible moves.
        if in_check:
            aboard.push(move)
            score = -evaluate(-beta, -alpha, aboard, must_mate)
            aboard.pop()
            if abs(score) == 9999: # We got mated.
                aboard.add_to_cache(0, position_as_bits, score)
                return score

            if score >= beta or must_mate:
                #aboard.add_to_cache(0, position_as_bits, beta)
                return beta
            if score > alpha:
                alpha = score
                new_alpha = True
            if score > current_eval:
                current_eval = score

        # Then, if we have a valid check to give, we should consider it.
        elif aboard.is_valid_check(move):
            aboard.push(move)
            score = -evaluate(-beta, -alpha, aboard)
            aboard.pop()
            if abs(score) == 9999: # We got mated.
                aboard.add_to_cache(0, position_as_bits, score)
                return score
            if score >= beta:
                if not must_mate:
                    #aboard.add_to_cache(0, position_as_bits, beta)
                    return beta
            if score > alpha:
                alpha = score
                new_alpha = True
            if score > current_eval:
                current_eval = score

        # Otherwise, we consider all reasonable captures.
        elif aboard.is_capture(move):
            if aboard.is_valid_capture(move):
                aboard.push(move)
                score = -evaluate(-beta, -alpha, aboard)
                aboard.pop()
                if score >= beta:
                    #aboard.add_to_cache(0, position_as_bits, beta)
                    return beta
                if score > alpha:
                    alpha = score
                    new_alpha = True
                if score > current_eval:
                    current_eval = score

    if new_alpha: # Only add it to the cache if the alpha changed from the input.
        aboard.add_to_cache(0, position_as_bits, alpha)
        return alpha
    else:
        # Otherwise, return the current evaluation, as bad as it may be.
        aboard.add_to_cache(0, position_as_bits, current_eval)
        return current_eval


def computerMove(aboard, depth):
    best_move = choose_move(aboard, depth)[1]
    evaluation = choose_move(aboard, depth)[0] / 100
    print ('Best move is ' + str(best_move) + ' and evaluation is: ' + "{:.2f}".format(evaluation))
    aboard.push(best_move)
    # Now we need to clear the cache for the board.
    aboard.reset_cache()

    return aboard


def return_move_json(aboard, depth):
    best_move = choose_move(aboard, depth)[1]
    evaluation = round((choose_move(aboard, depth)[0] / 100), 2)
    if aboard.turn == chess.BLACK:
        evaluation = -evaluation
    return {
        'move': aboard.san(best_move),
        'evaluation': evaluation
    }


