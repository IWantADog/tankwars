import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

import sys

from config import *
from tank import Tank, PlayerTank
from robot_tank import RobotTank
from point import Point
from wall import Brickwall
from bullet import Bullet
from collide import player_ai_collide, tank_wall_collide
from environment import Environment

def local_environment_init():
    pygame.init()
    pygame.mixer.init()

if __name__ == '__main__':
    local_environment_init()
    env = Environment()
    env.bulid()

    #player
    player = PlayerTank()
    player.load_images()
    env.add_player(player)

    #robot tank
    # robot = RobotTank()
    # env.add_robot(robot)

    #brickwall
    bwall = Brickwall((300, 100))
    env.add_wall(bwall)

    while True:
        env.framerate.tick(30)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        new_bullet = player.controller(keys, current_time)
        if new_bullet:
            env.add_player_bullet(new_bullet)

        env.update_spirtes(current_time)
        env.update_scrren(current_time)
        pygame.display.update()