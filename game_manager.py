from disk import Disk
import copy
import random


class GameManager:
    """Class that includes all connect four game logic"""
    def __init__(self, width, ROW_COUNT, COLUMN_COUNT, SIDE):
        self.width = width
        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT
        self.board = [[0] * self.COLUMN_COUNT for i in range(self.ROW_COUNT)]
        self.game_over = False
        self.turn = 0
        self.turn_timer = 0
        self.AI_Col = 0
        self.disks = []
        self.recent_piece = None
        self.player_piece = 1
        self.AI_piece = 2
        self.depth = 3
        self.winner = 0
        self.SIDE = SIDE

    # proccessing visualization part
    def update(self):
        background(180)
        for disk in self.disks:
            disk.display(self.SIDE)
            if disk.active is True:
                disk.y = disk.y + disk.rate
                disk.rate += 1
                if self.recent_piece is not None:
                    r = self.recent_piece[0]
                    y_bottom = (r + 1) * self.SIDE + self.SIDE / 2
                    if disk.y >= y_bottom:
                        del self.disks[:]
                        self.recent_piece = None
        noStroke()
        self.draw_board()
        strokeWeight(15)
        stroke(0, 0, 210)
        for i in range(0, 7):
            line(0, 700 - 100 * i, 700, 700 - 100 * i)
            line(0 + 100 * i, 100, 0 + 100 * i, 700)
        line(700, 100, 700, 700)
        textSize(64)
        fill(0, 255, 0)
        self.draw_message()

    def draw_board(self):
        DELAY = 80
        self.turn_timer += 1
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.recent_piece and self.recent_piece[0] == r \
                   and self.recent_piece[1] == c:
                    continue
                if self.board[r][c] == 1:
                    fill(255, 0, 0)
                    ellipse(c * self.SIDE + self.SIDE / 2,
                            (r + 1) * self.SIDE + self.SIDE / 2,
                            self.SIDE, self.SIDE)
                elif self.board[r][c] == 2:
                    fill(255, 255, 0)
                    ellipse(c * self.SIDE + self.SIDE / 2,
                            (r + 1) * self.SIDE + self.SIDE / 2,
                            self.SIDE, self.SIDE)
        if not self.game_over and self.turn == 1 and self.turn_timer > DELAY:
            self.play_ai()
            self.disks.append(Disk(self.AI_Col * self.SIDE + self.SIDE / 2,
                                   self.SIDE / 2, 1))
            self.disks[-1].active = True

    def prepare_to_drop(self):
        # and adjust the disk's position to be in the middle of a column.
        mouseX_revised = ((mouseX // self.SIDE) * self.SIDE
                          + self.SIDE / 2)
        if mouseY <= self.SIDE and self.turn == 0 and not self.game_over:
            self.disks.append(Disk(mouseX_revised, self.SIDE / 2, 0))

    def drag_moving(self):
        mouseX_revised = ((mouseX // self.SIDE) * self.SIDE
                          + self.SIDE / 2)
        # handle exception when mouseX is out of width's range
        if mouseX_revised >= self.width:
            mouseX_revised = (((self.width - 1) // self.SIDE)
                              * self.SIDE + self.SIDE / 2)
        elif mouseX_revised < 0:
            mouseX_revised = self.SIDE / 2
        mouseY_revised = self.SIDE / 2
        if len(self.disks) != 0 and self.turn == 0:
            self.disks[-1].x = mouseX_revised

    def start_drop(self):
        if len(self.disks) != 0 and self.turn == 0:
            self.disks[-1].active = True
            self.disks[-1].x = (self.disks[-1].x // self.SIDE) \
                * self.SIDE + self.SIDE / 2
            if not self.game_over:
                self.play(self.disks[-1].x, self.disks[-1].y)

    def draw_message(self):
        fill(0)
        textSize(38)
        # board is full
        if len(self.disks) == self.ROW_COUNT * self.COLUMN_COUNT:
            self.game_over = True
        if self.game_over:
            if self.winner == 0:
                text("BOARD IS FULL. TIE.", 210, 75)
            elif self.winner == 1:
                text("RED WINS", 250, 75)
            else:
                text("YELLOW WINS", 230, 75)
            return True

    # data structure part
    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
        self.recent_piece = (row, col)

    def is_valid_location(self, board, col):
        return board[0][col] == 0

    def get_next_open_row(self, board, col):
        for i in range(self.ROW_COUNT - 1, -1, -1):
            if board[i][col] == 0:
                return i

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def scoring(self, window, piece):
        '''scoring system for AI minimax algorithm'''
        score = 0
        opp_piece = self.player_piece
        if piece == self.player_piece:
            opp_piece = self.AI_piece

        if window.count(piece) == 4:
            score += 10000
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5
        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 80
        return score

    def score_position(self, board, piece):
        score = 0
        winning_length = 4
        # score for horizontal
        for r in range(self.ROW_COUNT):
            row_list = [board[r][c] for c in range(self.COLUMN_COUNT)]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_list[c:c+winning_length]
                score += self.scoring(window, piece)
        # score for vertical
        for c in range(self.COLUMN_COUNT):
            column_list = [board[r][c] for r in range(self.ROW_COUNT)]
            for r in range(self.ROW_COUNT - 3):
                window = column_list[r:r+winning_length]
                score += self.scoring(window, piece)
        # score for up diagonal
        for r in range(self.ROW_COUNT - 1, self.ROW_COUNT - 4, -1):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r-i][c+i] for i in range(winning_length)]
                score += self.scoring(window, piece)
        # score for down diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r+i][c+i] for i in range(winning_length)]
                score += self.scoring(window, piece)
        return score

    def is_terminal_node(self, board):
        return self.winning(board, self.player_piece) \
            or self.winning(board, self.AI_piece) \
            or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, maximizingPlayer):
        '''minimax algorithm that looks couple depth ahead of the board'''
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        LARGE_NUMBER = 100000000000000
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning(board, self.AI_piece):
                    return (None, LARGE_NUMBER)
                elif self.winning(board, self.player_piece):
                    return (None, -LARGE_NUMBER)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, self.AI_piece))
        if maximizingPlayer:
            value = -float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, row, col, self.AI_piece)
                new_score = self.minimax(board_copy, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else:  # Minimizing player
            value = float('inf')
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, row, col, self.player_piece)
                new_score = self.minimax(board_copy, depth-1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    def winning(self, board, piece):
        # check horizontal for winning
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece \
                  and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True
        # check vertical for winning
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r+1][c] == piece \
                  and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True
        # check for up diagonal for winning:
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 1, self.ROW_COUNT - 4, -1):
                if board[r][c] == piece and board[r-1][c+1] == piece \
                   and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True
        # check for down diagonal for winning
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r+1][c+1] == piece \
                   and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

    def play(self, mouseX, mouseY):
        if self.turn == 0:
            col = mouseX // self.SIDE
            if self.is_valid_location(self.board, col):
                row = self.get_next_open_row(self.board, col)
                self.drop_piece(self.board, row, col, self.player_piece)
                if self.winning(self.board, 1):
                    print("Human player wins")
                    self.winner = 1
                    self.game_over = True
                    return 1
                self.turn = 1
                self.turn_timer = 0

    def play_ai(self):
        if not self.game_over:
            self.AI_Col = self.minimax(self.board, self.depth, True)[0]
            if self.is_valid_location(self.board, self.AI_Col):
                row = self.get_next_open_row(self.board, self.AI_Col)
                self.drop_piece(self.board, row, self.AI_Col, self.AI_piece)
                if self.winning(self.board, 2):
                    print("AI wins")
                    self.winner = 2
                    self.game_over = True
                    return 2
            self.turn = 0
            self.turn_timer = 0
