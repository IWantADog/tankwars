import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank, GiftTank, BossTank
from point import Point
from wall import Brickwall, Steelwall
from boss import Boss
import sys
from map import load_map
from collide import player_ai_collide, player_bullet_collide, tank_wall_collide\
    , bullet_wall_collide, ai_bullent_collide, tank_boss_collide
from config import windows_width, windows_height, background, ai_tank_tag, player_img,\
    ai_number, number_img, tank_img



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((windows_width, windows_height))

    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    bg = pygame.image.load(background).convert()

    p_img = pygame.image.load(player_img).convert_alpha()

    ai_tag = pygame.image.load(ai_tank_tag).convert_alpha()
    tag_point = [(925+(i%2)*25, 100+(i//2)*25) for i in range(3)]


    #boss
    boss = Boss(450, 560)
    #boss group
    boss_group = Group()
    boss_group.add(boss)

    #player
    player = Tank(tank_img)

    number_master_img = pygame.image.load(number_img).convert_alpha()


    #player bullent group
    bullet_group = Group()

    boss_point = boss.get_point()
    #ai_tank
    now_ai_number = 3
    ai_1 = AiTank(player.point, boss_point)
    ai_2 = GiftTank(player.point, boss_point)
    ai_3 = BossTank(player.point, boss_point)


    #ai_tank bullent group
    ai_bullet_group = Group()

    #wall group
    # bwall = Brickwall(Point(300, 100))
    # swall = Steelwall(Point(300, 140))
    wall_group = load_map()


    #tank group
    player_group = Group()
    player_group.add(player)

    #ai tank group
    ai_group = Group()
    ai_group.add(ai_1)
    ai_group.add(ai_2)
    ai_group.add(ai_3)


    while True:
        framerate.tick(30)
        current_time = pygame.time.get_ticks()

        rect = Rect(player.get_life() * 18, 0, 18, 14)
        number_img = number_master_img.subsurface(rect)

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

        # add ai tank
        if len(ai_group.sprites()) < 3 and now_ai_number < ai_number:
            ai_group.add(AiTank(player.point, boss_point))
            ai_number += 1

        # clear bullet
        for bullet in bullet_group.sprites():
            if not bullet.islive:
                bullet_group.remove(bullet)

        # clear player
        if player.get_life() == 0 and player.get_birth() <= 0:
            player_group.remove(player)

        # clear ai which boom is 0(表示加载完毕了死亡图片)
        for item in ai_group.sprites():
            if item.boom == 0:
                ai_group.remove(item)
                if tag_point:
                    tag_point.pop()

        # clear wall which wall life is 0
        for item in wall_group.sprites():
            if item.life <= 0:
                wall_group.remove(item)

        # ai move&shooting module
        for ai in ai_group.sprites():
            ai.ai_move(current_time, 3000)
            ai_tank_bullet = ai.ai_shoot(current_time, 300)
            if ai_tank_bullet:
                ai_bullet_group.add(ai_tank_bullet)

        for bullet in ai_bullet_group.sprites():
            if not bullet.islive:
                ai_bullet_group.remove(bullet)

        #player-ai collide
        player_ai_collide(player, ai_group)

        # ai ai collide
        for ai in ai_group.sprites():
            player_ai_collide(ai, ai_group)

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

        screen.fill((0,0,0))

        player_group.update(current_time)
        ai_group.update(current_time)

        player_group.draw(screen)
        ai_group.draw(screen)

        wall_group.update()
        wall_group.draw(screen)

        boss_group.update()
        boss_group.draw(screen)

        bullet_group.update()
        ai_bullet_group.update()

        bullet_group.draw(screen)
        ai_bullet_group.draw(screen)

        screen.blit(bg, (900, 0))
        screen.blit(p_img, (925, 400))
        screen.blit(number_img, (950, 400))
        for tag in tag_point:
            screen.blit(ai_tag, tag)


        pygame.display.update()