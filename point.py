class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x: %f, y: %f' % (self.x, self.y)

    def get(self):
        return self.x, self.y