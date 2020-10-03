from game_manager import GameManager

COLUMN_COUNT = 7
ROW_COUNT = 6
SIDE = 100
width = COLUMN_COUNT * SIDE


def init_board():
    ZERO = 0
    game = GameManager(width, ZERO, ZERO, SIDE)
    assert game.board == []
    TWO = 2
    game = GameManager(width, TWO, TWO, SIDE)
    assert game.board == [[0, 0],
                          [0, 0]]
    FOUR = 4
    game = GameManager(width, FOUR, FOUR, SIDE)
    assert game.board == [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]


def test_drop_piece():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    game.drop_piece(game.board, 5, 5, 2)
    assert game.board == [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 2, 0]]


def test_is_valid_location():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    game.board = [[1, 1, 1, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 2, 0]]
    assert game.is_valid_location(game.board, 5) is False
    assert game.is_valid_location(game.board, 6) is True


def test_winning():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    win_horizontal = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]
    win_vertical = [[0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0]]
    win_up_diagnol = [[0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 1, 1, 0, 0],
                      [0, 0, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]
    win_dn_diagnol = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 2, 0, 1, 0],
                      [0, 0, 0, 0, 2, 0, 1]]

    assert game.winning(win_horizontal, 1) is True
    assert game.winning(win_horizontal, 1) is True
    assert game.winning(win_up_diagnol, 1) is True
    assert game.winning(win_dn_diagnol, 1) is True


def test_get_next_open_row():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 0]]
    assert game.get_next_open_row(game.board, 5) == 5
    assert game.get_next_open_row(board, 5) == 4


def test_get_valid_locations():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    board = [[0, 0, 0, 0, 0, 5, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 0]]

    assert game.get_valid_locations(board) == [0, 1, 2, 3, 4, 6]
    assert game.get_valid_locations(game.board) == [0, 1, 2, 3, 4, 5, 6]


def test_scoring():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    window = [1, 1, 1, 0, 2, 2, 2]
    assert game.scoring(window, game.AI_piece) == -70


def test_score_position():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 0],
             [0, 0, 0, 0, 2, 0, 0],
             [0, 0, 0, 2, 0, 0, 0]]
    assert game.score_position(board, 2) == 10


def test_is_terminal_node():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 2],
             [0, 0, 0, 0, 0, 2, 0],
             [0, 0, 0, 0, 2, 0, 0],
             [0, 0, 0, 2, 0, 0, 0]]

    assert game.is_terminal_node(board) is True
    assert game.is_terminal_node(game.board) is False


def test_minimax():
    game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 1, 0, 2, 0],
             [0, 0, 1, 0, 2, 0, 2],
             [0, 0, 0, 2, 0, 0, 2]]
    assert game.minimax(board, 3, True)[0] == 1
