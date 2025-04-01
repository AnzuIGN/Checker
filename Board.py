from Pieces import Piece

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                # Pieces are placed on dark squares: where (row+col) is odd.
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = Piece(row, col, 'black')
                    elif row > 4:
                        board[row][col] = Piece(row, col, 'white')
        return board

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[row][col] = piece
        self.board[piece.row][piece.col] = None
        piece.row = row
        piece.col = col
        # Promote to queen if reaching the opposite side.
        if row in [0, 7]:
            piece.make_queen()

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None

    def winner(self):
        white_count = sum(1 for row in self.board for piece in row if piece and piece.color == 'white')
        black_count = sum(1 for row in self.board for piece in row if piece and piece.color == 'black')
        if white_count == 0:
            return 'black'
        elif black_count == 0:
            return 'white'
        return None

    def get_valid_moves(self, piece):
        if piece.queen:
            return self._get_queen_moves(piece)
        else:
            return self._get_normal_moves(piece)

    # ----- Normal (non-queen) Moves & Multi-Jumps -----
    def _get_normal_moves(self, piece):
        row, col = piece.row, piece.col
        simple_moves = {}
        # Define forward directions based on color.
        directions = [(-1, -1), (-1, 1)] if piece.color == 'white' else [(1, -1), (1, 1)]
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.get_piece(r, c) is None:
                simple_moves[(r, c)] = []
        # Check for jumps (chain capture) recursively.
        jump_moves = self._get_normal_jumps(piece, row, col, [])
        # If any jump moves exist, they take precedence over simple moves.
        return jump_moves if jump_moves else simple_moves

    def _get_normal_jumps(self, piece, row, col, captured):
        moves = {}
        # Only forward jumps for normal pieces.
        directions = [(-1, -1), (-1, 1)] if piece.color == 'white' else [(1, -1), (1, 1)]
        for dr, dc in directions:
            enemy_r = row + dr
            enemy_c = col + dc
            landing_r = row + 2 * dr
            landing_c = col + 2 * dc
            if 0 <= enemy_r < 8 and 0 <= enemy_c < 8 and 0 <= landing_r < 8 and 0 <= landing_c < 8:
                enemy_piece = self.get_piece(enemy_r, enemy_c)
                landing = self.get_piece(landing_r, landing_c)
                # If an enemy piece is present, not already captured, and landing square is empty:
                if enemy_piece and enemy_piece.color != piece.color and landing is None and enemy_piece not in captured:
                    new_captured = captured + [enemy_piece]
                    # Recursively search for further jumps from the landing square.
                    subsequent = self._get_normal_jumps(piece, landing_r, landing_c, new_captured)
                    if subsequent:
                        for move, cap in subsequent.items():
                            moves[move] = new_captured + cap
                    else:
                        moves[(landing_r, landing_c)] = new_captured
        return moves

    # ----- Queen Moves & Multi-Jumps -----
    def _get_queen_moves(self, piece):
        row, col = piece.row, piece.col
        simple_moves = {}
        # Queen can move in all four diagonal directions.
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.get_piece(r, c) is None:
                simple_moves[(r, c)] = []
                r += dr
                c += dc
        jump_moves = self._get_queen_jumps(piece, row, col, [])
        return jump_moves if jump_moves else simple_moves

    def _get_queen_jumps(self, piece, row, col, captured):
        moves = {}
        stack = [(row, col, captured)]
        visited = set()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        while stack:
            cur_r, cur_c, cap = stack.pop()
            # Create a key for the current state.
            state_key = (cur_r, cur_c, tuple(sorted(id(p) for p in cap)))
            if state_key in visited:
                continue
            visited.add(state_key)
            for dr, dc in directions:
                r, c = cur_r + dr, cur_c + dc
                # Advance along the diagonal until an enemy piece or board edge is reached.
                while 0 <= r < 8 and 0 <= c < 8 and self.get_piece(r, c) is None:
                    r += dr
                    c += dc
                # If out of bounds, skip to next direction.
                if not (0 <= r < 8 and 0 <= c < 8):
                    continue
                enemy = self.get_piece(r, c)
                # If encountered piece is allied or already captured, skip this direction.
                if enemy is None or enemy.color == piece.color or enemy in cap:
                    continue
                # Found an enemy; move one more step for landing.
                r += dr
                c += dc
                # Record every empty landing square beyond the enemy.
                while 0 <= r < 8 and 0 <= c < 8 and self.get_piece(r, c) is None:
                    new_cap = cap + [enemy]
                    moves[(r, c)] = new_cap
                    # Add the new state to the stack for further jumps.
                    stack.append((r, c, new_cap))
                    r += dr
                    c += dc
        return moves
