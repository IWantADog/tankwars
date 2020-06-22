import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

import sys

from config import *
from tank import Tank
from robot_tank import RobotTank
from point import Point
from wall import Brickwall
from bullet import Bullet
from collide import player_ai_collide, tank_wall_collide

MUSCI = 'music/start.ogg' 

class Environment:
    def __init__(self):
        self.group_player = Group()
        self.group_robot = Group()
        self.group_bullet_player = Group()
        self.group_bullet_robot = Group()
        self.group_wall = Group()

        self.size = (900, 600)
        
    def bulid(self):
        start_music = pygame.mixer.Sound(MUSCI)
        channel = pygame.mixer.find_channel(True)
        channel.set_volume(0.5)
        channel.play(start_music)

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Tank Wars')

        self.framerate = pygame.time.Clock()

    def add_player(self, player):
        self.group_player.add(player)
    
    def add_robot(self, robot):
        self.group_robot.add(robot)

    def add_player_bullet(self, bullet):
        self.group_bullet_player.add(bullet)

    def add_robot_bullet(self, bullet):
        self.group_bullet_robot.add(bullet)
    
    def add_wall(self, wall):
        self.group_wall.add(wall)

    def update_spirtes(self, current_time):
        for bullet in self.group_bullet_player.sprites():
            if not bullet.islive:
                self.group_bullet_player.remove(bullet)

        for robot in self.group_bullet_robot.sprites():
            # TODO robot move rewrite
            # robot.ai_move(current_time, tt.get_point(), ai_t.get_point(), rate=3000)
            robot_tank_bullet = robot.ai_shoot(current_time, 300)
            if robot_tank_bullet:
                self.group_bullet_robot.add(robot_tank_bullet)
        
        for bullet in self.group_bullet_robot.sprites():
            if not bullet.islive:
                self.group_bullet_robot.remove(bullet)

    def update_scrren(self, current_time):
        self.screen.fill((0,0,0))

        self.group_player.update(current_time)
        self.group_player.draw(self.screen)

        self.group_robot.update(current_time)
        self.group_robot.draw(self.screen)

        self.group_bullet_player.update()
        self.group_bullet_player.draw(self.screen)

        self.group_bullet_robot.update()
        self.group_bullet_robot.draw(self.screen)

        #wall_group
        self.group_wall.update()
        self.group_wall.draw(self.screen)
