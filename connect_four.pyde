from game_manager import GameManager
from scorefile import ScoreFile

COLUMN_COUNT = 7
ROW_COUNT = 6
SIDE = 100
width = COLUMN_COUNT * SIDE
height = (ROW_COUNT + 1) * SIDE
game = GameManager(width, ROW_COUNT, COLUMN_COUNT, SIDE)
scorefile = ScoreFile()
count = 0


def setup():
    size(width, height)


def input(self, message='Please enter your name:'):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)


def draw():
    background(0)
    handle_scorefile()
    game.update()


def mousePressed():
    game.prepare_to_drop()


def mouseDragged():
    game.drag_moving()


def mouseReleased():
    game.start_drop()


def handle_player_name():
    global player_name
    player_name = input('Please enter your name:')
    if player_name and player_name != "":
        player_name = player_name
    else:  # Canceled dialog or input nothing
        player_name = "anonymous player"
    noLoop()


def handle_scorefile():
    global count
    global player_name
    if game.draw_message() and game.recent_piece is None:
        score_file = open('scores.txt', 'a')
        if game.winner == 1:  # human player wins
            if count == 0:
                handle_player_name()
                score_file.write(player_name + " 1\n")
        else:  # tie or AI wins
            if count == 0:
                handle_player_name()
                score_file.write(player_name + " 0\n")
        count += 1
        score_file.close()
        if scorefile.count == 0:
            scorefile.process_file()
