class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False

    def make_queen(self):
        self.queen = True

    def __str__(self):
        if self.color == 'white':
            return "Q" if self.queen else "q"
        else:
            return "W" if self.queen else "w"