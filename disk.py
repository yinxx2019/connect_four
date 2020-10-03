class Disk:
    def __init__(self, x, y, turn):
        self.x = x
        self.y = y
        self.fall = True
        self.active = False
        self.rate = 1
        self.turn = turn
        self.timer = 0

    def display(self, radius):
        noStroke()
        if self.turn == 0:
            fill(255, 0, 0)
            ellipse(self.x, self.y, radius, radius)
        elif self.turn == 1:
            fill(255, 255, 0)
            ellipse(self.x, self.y, radius, radius)
