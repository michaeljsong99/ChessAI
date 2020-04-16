from chess import *


# Augmented Board also keeps track of the material advantage.
class AugmentedBoard(Board):

    piece_symbols = [None, "p", "n", "b", "r", "q", "k"]

    squares = [
        'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
        'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
        'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
        'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
        'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
        'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
        'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
        'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8',
    ]

    material_values = {
        PAWN: 100,
        KNIGHT: 300,
        BISHOP: 325,
        ROOK: 500,
        QUEEN: 900
    }
     # Central pawns are encouraged to be advanced.

    pawntable = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0]

    # Knights are typically best in the center.
    knighttable = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50]

    # Bishops avoid corners and borders.
    bishoptable = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20]

    # Rooks should occupy 7th rank and avoid a and h files.
    rooktable = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0]

    # Queens should try to centralize.
    queentable = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, -5, 0, 0, 0, 0, -5, -10,
        -10, 5, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 5, 5, 5, 0, -5,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, -5, 0, 0, 0, 0, -5, -10,
        -20, -10, -10, -5, -5, -10, -10, -20]

    kingtable = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30]

    # A hash map that contains < depth < position, evaluation >>
    _cached_positions = {}



    def _calculate_material(self):
        material_count = 0
        pieces = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]
        for piece in pieces:
            white_pieces = list(self.pieces(piece_type=piece, color=WHITE))
            material_count += self.material_values[piece] * len(white_pieces)
            black_pieces = list(self.pieces(piece_type=piece, color=BLACK))
            material_count -= self.material_values[piece] * len(black_pieces)
        return material_count

    # For now, piece activity is static.
    def _calculate_activity(self):
        pawn_activity = sum(self.pawntable[i] for i in self.pieces(PAWN, WHITE)) - \
                        sum(self.pawntable[square_mirror(i)] for i in self.pieces(PAWN, BLACK))
        knight_activity = sum(self.knighttable[i] for i in self.pieces(KNIGHT, WHITE)) - \
                        sum(self.knighttable[square_mirror(i)] for i in self.pieces(KNIGHT, BLACK))
        bishop_activity = sum(self.bishoptable[i] for i in self.pieces(BISHOP, WHITE)) - \
                        sum(self.bishoptable[square_mirror(i)] for i in self.pieces(BISHOP, BLACK))
        rook_activity = sum(self.rooktable[i] for i in self.pieces(ROOK, WHITE)) - \
                        sum(self.rooktable[square_mirror(i)] for i in self.pieces(ROOK, BLACK))
        queen_activity = sum(self.queentable[i] for i in self.pieces(QUEEN, WHITE)) - \
                        sum(self.queentable[square_mirror(i)] for i in self.pieces(QUEEN, BLACK))
        king_safety = sum(self.kingtable[i] for i in self.pieces(KING, WHITE)) - \
                        sum(self.kingtable[square_mirror(i)] for i in self.pieces(KING, BLACK))

        return pawn_activity + knight_activity + bishop_activity + rook_activity + queen_activity + king_safety

    def evaluation(self):
        eval = self._calculate_material() + self._calculate_activity()
        if self.turn == WHITE:
            return eval
        else:
            return -eval

    # Returns true if a enemy piece can be taken that has no defenders, or the enemy piece value is greater or equal to our piece.
    def is_valid_capture(self, move):
        if self.is_en_passant(move): # If it is an en-passant, we must consider it.
            return True

        moved_from = move.from_square
        captured = move.to_square
        capturer = self.piece_type_at(moved_from)
        if capturer == KING:                        # If it is a king capture, it is legal. So we consider it.
            return True
        capturer_value = self.material_values[capturer]
        captured_value = self.material_values[self.piece_type_at(captured)]

        if captured_value >= capturer_value:    # We must consider the capture.
            return True

        num_attackers = num_defenders = 0
        if self.turn == WHITE:
            num_attackers = len(self.attackers(color=WHITE, square=captured))
            num_defenders = len(self.attackers(color=BLACK, square=captured))
        else:
            num_attackers = len(self.attackers(color=BLACK, square=captured))
            num_defenders = len(self.attackers(color=WHITE, square=captured))

        if num_defenders == 0: # The piece is unprotected.
            return True

        elif num_attackers > num_defenders: # There are more attackers than defenders.
            return True

        else:
            return False

    # Converts a position to a 773 bit tuple.
    def bitify_position(self):

        position = []
        for square in SQUARES_180:
            mask = BB_SQUARES[square]

            if not self.occupied & mask:
                position.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            elif bool(self.occupied_co[WHITE] & mask):
                if self.pawns & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
                elif self.knights & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
                elif self.bishops & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
                elif self.rooks & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
                elif self.queens & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
                elif self.kings & mask:
                    position.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            # Now we know it is a black piece.
            elif self.pawns & mask:
                position.extend([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            elif self.knights & mask:
                position.extend([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            elif self.bishops & mask:
                position.extend([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            elif self.rooks & mask:
                position.extend([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
            elif self.queens & mask:
                position.extend([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
            elif self.kings & mask:
                position.extend([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

        # Now add 5 more bits for:
        # 1. Side to move: 1 for White, 0 for Black
        # 2. White can Castle Kingside
        # 3. White can Castle Queenside
        # 4. Black can Castle Kingside
        # 5. Black can Castle Queenside

        turn = 1 if self.turn == WHITE else 0
        w_ks_castle = 1 if self.has_kingside_castling_rights(WHITE) else 0
        w_qs_castle = 1 if self.has_queenside_castling_rights(WHITE) else 0
        b_ks_castle = 1 if self.has_kingside_castling_rights(BLACK) else 0
        b_qs_castle = 1 if self.has_queenside_castling_rights(BLACK) else 0

        position.extend([turn, w_ks_castle, w_qs_castle, b_ks_castle, b_qs_castle])

        return tuple(position)

    # Add a given depth and position to our cache.
    def add_to_cache(self, depth, position, evaluation):
        if depth not in self._cached_positions:
            self._cached_positions[depth] = {position: evaluation}
        elif position not in self._cached_positions[depth]:
            self._cached_positions[depth][position] = evaluation

    # Check if a given depth and position is in our cache. Returns None if the depth and position does not exist.
    def lookup_position(self, depth, position):
        if depth in self._cached_positions:
            if position in self._cached_positions[depth]:
                return self._cached_positions[depth][position]
        return None

    # Resets the cached_positions to be an empty hash map.
    def reset_cache(self):
        self._cached_positions = {}

    # Gets the type of piece promoted.
    def get_piece_promoted(self, piece_as_int):
        return self.piece_symbols[piece_as_int]





