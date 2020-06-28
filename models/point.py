class Point():
    def __init__(self, p):
        self.x, self.y = p

    def __str__(self):
        return 'x: %f, y: %f' % (self.x, self.y)

    def get(self):
        return self.x, self.y

    def get_distance(self, point):
        return abs(self.x - point.x or self.y - point.y)


if __name__ == '__main__':
    p = Point((1, 2))
    sp = Point((9, 2))
    if -1:
        print('aa')
    # print(p)
    # print(p.get())
    # print(p.x, p.y)
    print(p.get_distance(sp))