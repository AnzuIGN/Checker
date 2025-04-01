from Board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'  # White starts first.
        self.selected = None
        self.valid_moves = {}
        self.winner = None

    def no_moves_available(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece and piece.color == color:
                    if self.board.get_valid_moves(piece):
                        return False
        return True

    def check_winner(self):
        # First, check by piece count.
        white_count = sum(1 for row in self.board.board for piece in row if piece and piece.color == 'white')
        black_count = sum(1 for row in self.board.board for piece in row if piece and piece.color == 'black')
        if white_count == 0:
            return 'black'
        elif black_count == 0:
            return 'white'
        # Optionally, check if the current side has no moves available.
        if self.no_moves_available(self.turn):
            return 'white' if self.turn == 'black' else 'black'
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
        # After switching turn, update the winner if one side has no pieces.
        self.winner = self.check_winner()
