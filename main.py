import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank
from point import Point
from collide import player_ai_collide, player_bullet_collide
import sys

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    #boss
    boss_point = Point(300, 300)

    #player
    player = Tank('tank.png', 2)

    #player bullent group
    bullet_group = Group()

    #ai_tank
    ai = AiTank(player.point, boss_point)
    # ai1.start()

    #ai_tank bullent group
    ai_bullet_group = Group()



    #tank group
    player_group = Group()
    player_group.add(player)

    #ai tank group
    ai_group = Group()
    ai_group.add(ai)


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


        screen.fill((0,0,0))

        player_group.update(current_time)
        ai_group.update(current_time)

        player_group.draw(screen)
        ai_group.draw(screen)

        bullet_group.update()
        ai_bullet_group.update()

        bullet_group.draw(screen)
        ai_bullet_group.draw(screen)


        pygame.display.update()