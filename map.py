import pygame
from wall import Steelwall, Brickwall
from pygame.sprite import Group
from point import Point

def load_map():
     brickwall_point_1 = [(150, 100+i*40) for i in range(3)]
     brickwall_point_2 = [(150, 280+i*40) for i in range(3)]
     brickwall_point_3 = [(350, 100+i*40) for i in range(3)]
     brickwall_point_4 = [(350, 280+i*40) for i in range(3)]
     brickwall_point_5 = [(550, 100+i*40) for i in range(3)]
     brickwall_point_6 = [(550, 280+i*40) for i in range(3)]
     brickwall_point_7 = [(750, 100+i*40) for i in range(3)]
     brickwall_point_8 = [(750, 280+i*40) for i in range(3)]
     brickwall_point_9 = [(410, 560), (490, 560), (410, 520),
                          (450, 520), (490, 520)]
     brickwall_point_10 = [(100 + i*40, 450) for i in range(5)]
     brickwall_point_11 = [(640 + i*40, 450) for i in range(5)]
     steelwall_point = [(0, 300), (860, 300)]

     wall = []
     wall.extend(brickwall_point_1)
     wall.extend(brickwall_point_2)
     wall.extend(brickwall_point_3)
     wall.extend(brickwall_point_4)
     wall.extend(brickwall_point_5)
     wall.extend(brickwall_point_6)
     wall.extend(brickwall_point_7)
     wall.extend(brickwall_point_8)
     wall.extend(brickwall_point_9)
     wall.extend(brickwall_point_10)
     wall.extend(brickwall_point_11)

     group = Group()

     for item in wall:
         group.add(Brickwall(item))

     for item in steelwall_point:
         group.add(Steelwall(item))

     return group

