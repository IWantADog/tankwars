import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank, GiftTank, BossTank
from point import Point
from wall import Brickwall, Steelwall
from gift import Clock, OneLife
from boss import Boss
import sys
from map import load_map
from collide import player_ai_collide, player_bullet_collide, tank_wall_collide\
    , bullet_wall_collide, ai_bullent_collide, tank_boss_collide, player_gift_collide
from config import windows_width, windows_height, background, ai_tank_tag, player_img,\
    ai_number, number_img, tank_img, start_img, gameover_img, start_music, shoot_music


def init_game():
    # boss
    boss = Boss(450, 560)
    # boss group
    boss_group = Group()
    boss_group.add(boss)

    # player
    player = Tank(tank_img)

    # player bullent group
    bullet_group = Group()

    # ai_tank
    now_ai_number = 3
    ai_1 = AiTank()
    ai_2 = AiTank()
    ai_3 = AiTank()

    # ai_tank bullent group
    ai_bullet_group = Group()

    # wall group loading map
    wall_group = load_map()

    # tank group
    player_group = Group()
    player_group.add(player)

    # ai tank group
    ai_group = Group()
    ai_group.add(ai_1)
    ai_group.add(ai_2)
    ai_group.add(ai_3)

    gift_group = Group()

    tag_point = [(925+(i%2)*25, 100+(i//2)*25) for i in range(ai_number)]

    return player, boss, player_group, boss_group, ai_group, bullet_group, ai_bullet_group, wall_group,\
        gift_group, now_ai_number, tag_point


def play_music(music):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(music)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((windows_width, windows_height))

    pygame.display.set_caption('Tank Wars')

    framerate = pygame.time.Clock()

    bg = pygame.image.load(background).convert()

    p_img = pygame.image.load(player_img).convert_alpha()

    ai_tag = pygame.image.load(ai_tank_tag).convert_alpha()

    #start image
    start_image = pygame.image.load(start_img).convert_alpha()

    #gameover image
    gameover_image = pygame.image.load(gameover_img).convert_alpha()

    #player life image
    number_master_img = pygame.image.load(number_img).convert_alpha()

    #start music
    music_start = pygame.mixer.Sound(start_music)

    #shoot music
    music_shoot = pygame.mixer.Sound(shoot_music)

    #init game
    player, boss, player_group, boss_group, ai_group, bullet_group,\
        ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game()
    play_music(music_start)

    start_time = 0
    game_state = 'start'

    while True:
        if game_state == 'start':
            screen.blit(start_image, (140, 50))
            myfont = pygame.font.Font(None, 60)
            textImg = myfont.render("Press 'J' to start game!", True, (0, 0, 255))
            screen.blit(textImg, (295, 430))
            keys = pygame.key.get_pressed()
            if keys[K_j]:
                game_state = 'running'

        elif game_state == 'gameover':
            screen.blit(gameover_image, (270, 100))
            myfont = pygame.font.Font(None, 60)
            textImg = myfont.render("Press 'R' to restart game!", True, (0, 0, 255))
            screen.blit(textImg, (220, 430))
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                game_state = 'running'
                player, boss, player_group, boss_group, ai_group, bullet_group,\
                    ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game()
                play_music(music_start)


        elif game_state == 'running':
            framerate.tick(30)
            current_time = pygame.time.get_ticks()

            rect = Rect(player.get_life() * 14, 0, 14, 12)
            number_img = number_master_img.subsurface(rect)

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
                    play_music(music_shoot)
                    bullet_group.add(new_bullet)

            # add ai tank
            if len(ai_group.sprites()) < 5 and now_ai_number < ai_number:
                if now_ai_number == 6 or now_ai_number == 15:
                    ai_group.add(GiftTank())
                elif now_ai_number == ai_number - 1:
                    ai_group.add(BossTank())
                else:
                    ai_group.add(AiTank())
                now_ai_number += 1

            # clear bullet
            for bullet in bullet_group.sprites():
                if not bullet.islive:
                    bullet_group.remove(bullet)

            # clear player
            if player.get_life() == 0 and player.get_birth() <= 0:
                player_group.remove(player)
                game_state = 'gameover'

            if boss.get_life() == 0:
                game_state = 'gameover'

            # clear ai which boom is 0(表示加载完毕了死亡图片)
            for item in ai_group.sprites():
                if item.boom == 0:
                    if item.name == 'gift':
                        gift_group.add(item.leave_gift())
                    ai_group.remove(item)
                    if tag_point:
                        tag_point.pop()

          # clear wall which wall life is 0
            for item in wall_group.sprites():
                if item.life <= 0:
                    wall_group.remove(item)

            # ai move&shooting module
            for ai in ai_group.sprites():
                ai.ai_move(current_time, player.get_point(), boss.get_point(), rate=3000)
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

            #player gift collide
            start_time = player_gift_collide(player, gift_group, ai_group, current_time, start_time)
            # print('aaaaaa', start_time)
            # for ai in ai_group.sprites():
            #     print(ai.state)

            screen.fill((0,0,0))

            player_group.update(current_time)
            ai_group.update(current_time)

            player_group.draw(screen)
            ai_group.draw(screen)

            wall_group.update()
            wall_group.draw(screen)

            gift_group.update()
            gift_group.draw(screen)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()