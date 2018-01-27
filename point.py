class Point():
    def __init__(self, p):
        self.x, self.y = p

    def __str__(self):
        return 'x: %f, y: %f' % (self.x, self.y)

    def get(self):
        return self.x, self.y


if __name__ == '__main__':
    p = Point((1, 2))
    print(p)
    print(p.get())
    print(p.x, p.y)