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
    print(x,'   ', y)

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
        if pygame.sprite.collide_rect(player, item):
            pp = player.get_point()
            ip = item.get_point()
            pd, ad = get_collide_dirct(pp, ip)
            print(pd, '   ', ad)
            player.set_collide_dirct(pd)
            item.set_collide_dirct(ad)


def player_bullet_collide(play_bullet, ai_group):
    for item in ai_group.sprites():
        collide_list = pygame.sprite.spritecollide(item, play_bullet, True)
        item.lost_life(len(collide_list))





