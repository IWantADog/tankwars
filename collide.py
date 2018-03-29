import pygame
from point import Point
from pygame.locals import *
from pygame.sprite import Group

def get_collide_dirct(ppoint, apoint):
    px, py = ppoint.get()
    ax, ay = apoint.get()
    x = abs(px - ax)
    y = abs(py - ay)

    if x < y:
        if py > ay:
            return 'w', 's'
        else:
            return 's', 'w'
    elif x >= y:
        if px > ax:
            return 'a', 'd'
        else:
            return 'd', 'a'

# def player_ai_collide(player, ai_group):
#     collide_list = pygame.sprite.spritecollide(player, ai_group, False)
#     for item in collide_list:
#         pp = player.get_point()
#         ip = item.get_point()
#         pd, ad = get_collide_dirct(pp, ip)
#         print(pd,'   ', ad)
#         player.set_collide_dirct(pd)
#         item.set_collide_dirct(ad)
#         print('aaaa')

def player_ai_collide(player, ai_group):
    for item in ai_group.sprites():
        if player != item and pygame.sprite.collide_rect(player, item):
            pp = player.get_point()
            ip = item.get_point()
            pd, ad = get_collide_dirct(pp, ip)
            # print(pd, '   ', ad)
            player.set_collide_dirct(pd)
            item.set_collide_dirct(ad)

def player_gift_collide(player, gift_group, ai_group, current_time, start_time):
    collide_list = pygame.sprite.spritecollide(player, gift_group, True)
    for gift in collide_list:
        if gift.name == 'clock':
            start_time = current_time
            for ai in ai_group.sprites():
                ai.state = 'clock'
        elif gift.name == 'onelife':
            player.add_life(1)

    for ai in ai_group.sprites():
        if ai.state == 'clock':
            if current_time <= start_time + 5000:
                for a in ai_group:
                    a.state = 'clock'
            else:
                for a in ai_group:
                    a.state = 'notfind'
            break
    return start_time

def player_bullet_collide(play_bullet, ai_group):
    for item in ai_group.sprites():
        collide_list = pygame.sprite.spritecollide(item, play_bullet, True)
        item.lost_life(len(collide_list))

def ai_bullent_collide(tank, ai_bullet):
    collide_list = pygame.sprite.spritecollide(tank, ai_bullet, True)
    tank.lost_life(len(collide_list))

def tank_wall_collide(tank_group, wall_group):
    collide_list = pygame.sprite.groupcollide(tank_group, wall_group, False, False)
    for tank, walls in collide_list.items():
        for wall in walls:
            tp = tank.get_point()
            wp = wall.get_point()
            td, wd = get_collide_dirct(tp, wp)
            tank.set_collide_dirct(td)


def bullet_wall_collide(bullet_group, wall_group):
    collide_list = pygame.sprite.groupcollide(wall_group, bullet_group, False, True)
    for wall, bullets in collide_list.items():
        if wall.name == 'brickwall':
            wall.lost_life(len(bullets))


def tank_boss_collide(tank_group, boss):
    for tank in tank_group.sprites():
        if pygame.sprite.collide_rect(tank, boss):
            tp = tank.get_point()
            bp = boss.get_point()
            td, bd = get_collide_dirct(tp, bp)
            tank.set_collide_dirct(td)

