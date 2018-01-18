import pygame
from wall import Steelwall, Brickwall
from pygame.sprite import Group
from point import Point

def load_map():
     brickwall_point_1 = [Point(150, 100+i*40) for i in range(8)]
     brickwall_point_2 = [Point(350, 100+i*40) for i in range(8)]
     brickwall_point_3 = [Point(550, 100+i*40) for i in range(8)]
     brickwall_point_4 = [Point(750, 100+i*40) for i in range(8)]
     brickwall_point_5 = [Point(410, 560), Point(490, 560), Point(410, 520),
                          Point(450, 520), Point(490, 520)]
     brickwall_point_6 = [Point(100 + i*40, 450) for i in range(5)]
     brickwall_point_7 = [Point(640 + i*40, 450) for i in range(5)]
     steelwall_point = [Point(0, 300), Point(860, 300)]

     wall = []
     wall.extend(brickwall_point_1)
     wall.extend(brickwall_point_2)
     wall.extend(brickwall_point_3)
     wall.extend(brickwall_point_4)
     wall.extend(brickwall_point_5)
     wall.extend(brickwall_point_6)
     wall.extend(brickwall_point_7)

     group = Group()

     for item in wall:
         group.add(Brickwall(item))

     for item in steelwall_point:
         group.add(Steelwall(item))

     return group

