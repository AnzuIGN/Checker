from Board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'  # White starts first
        self.selected = None
        self.valid_moves = {}
        self.winner = None


    def no_moves_available(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece and piece.color == color:
                    valid = self.board.get_valid_moves(piece)
                    if valid:  # If there's at least one valid move
                        return False
        return True


    def check_winner(self):
        if self.no_moves_available(self.turn):
            return 'white' if self.turn == 'black' else 'black'
        # Fallback: check by piece count.
        white_count = sum(1 for row in self.board.board for piece in row if piece and piece.color == 'white')
        black_count = sum(1 for row in self.board.board for piece in row if piece and piece.color == 'black')
        if white_count == 0:
            return 'black'
        elif black_count == 0:
            return 'white'
        return None

    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected:
            if self._move(row, col):
                return True
            else:
                self.selected = None
                self.valid_moves = {}
                return self.select(row, col)
        if piece is not None and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            # (Optional: enforce mandatory capture by filtering moves if needed.)
            return True
        return False

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                for piece in skipped:
                    self.board.remove([piece])
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.selected = None
        self.valid_moves = {}
        self.turn = 'white' if self.turn == 'black' else 'black'
        # After switching turn, check if the new side has any moves.
        self.winner = self.check_winner()
