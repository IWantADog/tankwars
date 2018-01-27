import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank
from point import Point
from wall import Brickwall, Steelwall
from boss import Boss
from gift import Clock, OneLife
from config import tank_img
from collide import player_ai_collide, player_bullet_collide, tank_wall_collide\
    , bullet_wall_collide, ai_bullent_collide, tank_boss_collide, player_gift_collide
import sys

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    #boss
    boss_point = Point(300, 300)

    #player
    player = Tank(tank_img, point=Point(100,200))

    #player bullent group
    bullet_group = Group()

    #ai_tank
    ai = AiTank(player.point, boss_point)
    # ai1.start()

    #ai_tank bullent group
    ai_bullet_group = Group()

    #wall
    bwall = Brickwall(Point(300, 100))
    swall = Steelwall(Point(300, 140))

    #wall group
    wall_group = Group()
    wall_group.add(bwall)
    wall_group.add(swall)

    #tank group
    player_group = Group()
    player_group.add(player)

    #ai tank group
    ai_group = Group()
    ai_group.add(ai)


    #boss
    boss = Boss(200, 210)
    #boss group
    boss_group = Group()
    boss_group.add(boss)

    gift_clock = Clock(Point(250, 200))
    gift_onelife = OneLife(Point(250, 300))
    # gift group
    gift_group = Group()
    gift_group.add(gift_clock)
    gift_group.add(gift_onelife)

    while True:
        framerate.tick(30)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            player.move('w')
        elif keys[K_s]:
            player.move('s')
        elif keys[K_a]:
            player.move('a')
        elif keys[K_d]:
            player.move('d')

        if keys[K_j]:
            new_bullet = player.shoot(current_time, 300)
            if new_bullet:
                bullet_group.add(new_bullet)

        # clear bullet
        for bullet in bullet_group.sprites():
            if not bullet.islive:
                bullet_group.remove(bullet)

        # clear ai which boom is 0(表示加载完毕了死亡图片)
        for item in ai_group.sprites():
            if item.boom == 0:
                ai_group.remove(item)

        # clear wall which wall life is 0
        for item in wall_group.sprites():
            if item.life <= 0:
                wall_group.remove(item)

        # ai move&shooting module
        ai.ai_move(current_time, 3000)
        ai_tank_bullet = ai.ai_shoot(current_time, 300)
        if ai_tank_bullet:
            ai_bullet_group.add(ai_tank_bullet)

        for bullet in ai_bullet_group.sprites():
            if not bullet.islive:
                ai_bullet_group.remove(bullet)

        #player-ai collide
        player_ai_collide(player, ai_group)

        #play bullets collide
        player_bullet_collide(bullet_group, ai_group)

        #tank walls collide
        tank_wall_collide(player_group, wall_group)
        tank_wall_collide(ai_group, wall_group)

        #bullents walls collide
        bullet_wall_collide(bullet_group, wall_group)
        bullet_wall_collide(ai_bullet_group, wall_group)

        #tank boss collide
        tank_boss_collide(player_group, boss)
        tank_boss_collide(ai_group, boss)

        #ai bullet collide
        ai_bullent_collide(player, ai_bullet_group)
        ai_bullent_collide(boss, ai_bullet_group)

        #player gift collide
        player_gift_collide(player, gift_group, ai_group)

        screen.fill((0,0,0))

        player_group.update(current_time)
        ai_group.update(current_time)

        player_group.draw(screen)
        ai_group.draw(screen)

        wall_group.update()
        wall_group.draw(screen)

        boss_group.update()
        boss_group.draw(screen)

        gift_group.update()
        gift_group.draw(screen)

        bullet_group.update()
        ai_bullet_group.update()

        bullet_group.draw(screen)
        ai_bullet_group.draw(screen)


        pygame.display.update()