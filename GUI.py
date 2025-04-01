# GUI.py
import tkinter as tk
from Game import Game
from Constants import ROWS, COLS, SQUARE_SIZE
import Animations

WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

class CheckersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.game = Game()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        # Draw board squares.
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "#ccc" if (row + col) % 2 == 0 else "#999"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Highlight valid moves for a selected piece.
        if self.game.selected:
            for move in self.game.valid_moves.keys():
                r, c = move
                x1 = c * SQUARE_SIZE
                y1 = r * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", stipple="gray50", outline="")

        # Draw pieces.
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.board.board[row][col]
                if piece:
                    cx = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    cy = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    if piece.color == "black":
                        self.canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30,
                                                fill="white", outline="")
                        piece_item = self.canvas.create_oval(cx - 26, cy - 26, cx + 26, cy + 26,
                                                             fill="black", outline="black", width=2)
                    else:
                        piece_item = self.canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30,
                                                             fill="white", outline="black", width=2)
                    if piece.queen:
                        self.canvas.create_text(cx, cy, text="👑", font=("Arial", 30, "bold"), fill="gold")
                    if piece.color == self.game.turn and self.game.board.get_valid_moves(piece):
                        Animations.animate_piece_flash(self.canvas, piece_item)
        self.root.update()

    def click(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if not self.game.selected:
            self.game.select(row, col)
        else:
            if (row, col) in self.game.valid_moves:
                start_row, start_col = self.game.selected.row, self.game.selected.col
                start_coords = (start_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                start_row * SQUARE_SIZE + SQUARE_SIZE // 2)
                end_coords = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            row * SQUARE_SIZE + SQUARE_SIZE // 2)
                if self.game.selected.color == "black":
                    self.canvas.create_oval(start_coords[0]-30, start_coords[1]-30,
                                            start_coords[0]+30, start_coords[1]+30,
                                            fill="white", outline="")
                    moving_piece = self.canvas.create_oval(start_coords[0]-26, start_coords[1]-26,
                                                        start_coords[0]+26, start_coords[1]+26,
                                                        fill="black", outline="black", width=2)
                else:
                    moving_piece = self.canvas.create_oval(start_coords[0]-30, start_coords[1]-30,
                                                        start_coords[0]+30, start_coords[1]+30,
                                                        fill="white", outline="black", width=2)
                if self.game.selected.queen:
                    self.canvas.create_text(start_coords[0], start_coords[1],
                                            text="👑", font=("Arial", 30, "bold"), fill="gold")
                Animations.animate_piece_move(self.canvas, moving_piece, start_coords, end_coords)
                self.canvas.delete(moving_piece)
                self.game._move(row, col)
            else:
                self.game.selected = None
                self.game.valid_moves = {}
                self.game.select(row, col)
        self.draw_board()
        self.draw_winner_text()
        if self.game.winner:
            text = f"{self.game.winner.capitalize()} wins!"
            x = WIDTH // 2
            y = HEIGHT // 2
            # Draw outline: four offset copies in black.
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                self.canvas.create_text(x + dx, y + dy,
                                        text=text,
                                        font=("Arial", 32, "bold"),
                                        fill="black")
            # Draw main text in gold on top.
            self.canvas.create_text(x, y,
                                    text=text,
                                    font=("Arial", 32, "bold"),
                                    fill="gold")

    def run(self):
        self.canvas.bind("<Button-1>", self.click)
        self.root.mainloop()

def main():
    root = tk.Tk()
    gui = CheckersGUI(root)
    gui.run()

if __name__ == '__main__':
    main()
