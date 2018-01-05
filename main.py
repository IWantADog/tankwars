import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank
from point import Point
import sys

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    #boss
    boss_point = Point(300, 300)

    #player
    tt = Tank('tank.png', 2)

    #player bullent group
    bullet_group = Group()

    #ai_tank
    ai1 = AiTank(tt.point, boss_point)
    # ai1.start()

    #ai_tank bullent group
    ai_bullet_group = Group()



    #tank group
    group = Group()
    group.add(tt)
    group.add(ai1)


    while True:
        framerate.tick(30)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            tt.move('w')
        elif keys[K_s]:
            tt.move('s')
        elif keys[K_a]:
            tt.move('a')
        elif keys[K_d]:
            tt.move('d')

        if keys[K_j]:
            new_bullet = tt.shoot(current_time, 300)
            if new_bullet:
                bullet_group.add(new_bullet)
            # pass

        for bullet in bullet_group.sprites():
            if not bullet.islive:
                bullet_group.remove(bullet)
                # passj

        # ai1.running(current_time)
        ai1.ai_move(current_time, 3000)
        ai_tank_bullet = ai1.ai_shoot(current_time, 300)
        if ai_tank_bullet:
            ai_bullet_group.add(ai_tank_bullet)

        for bullet in ai_bullet_group.sprites():
            if not bullet.islive:
                ai_bullet_group.remove(bullet)
                # passj

        # print('1111 ', len(bullet_group.sprites()))
        screen.fill((0,0,0))

        group.update(current_time)
        group.draw(screen)


        bullet_group.update()
        ai_bullet_group.update()

        bullet_group.draw(screen)
        ai_bullet_group.draw(screen)


        pygame.display.update()