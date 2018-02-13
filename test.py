import pygame
from pygame.locals import *
from pygame.sprite import Group
from tank import Tank
from ai_tank import AiTank, GiftTank, BossTank_1, BossTank_2
from point import Point
from wall import Brickwall, Steelwall
from gift import Clock, OneLife
from boss import Boss
import sys
from map import load_map_1, load_map_2, load_map_3
from collide import player_ai_collide, player_bullet_collide, tank_wall_collide\
    , bullet_wall_collide, ai_bullent_collide, tank_boss_collide, player_gift_collide
from config import windows_width, windows_height, background, ai_tank_tag,\
    number_img, player_tank_path, ai_tank_path, gift_tank_path, boss_1_path,boss_2_path, bullet_path,\
    start_img, gameover_img, start_music, shoot_music, load_images, player_img, boss_bullet_path,\
    stage_img, stage_number_img


def init_game(player_images, ai_images, stage):
    if stage == 1:
        # wall group loading map
        wall_group = load_map_1()
    elif stage == 2:
        wall_group = load_map_2()
    else:
        wall_group = load_map_3()

    # ai_tank
    if stage == 3:
        ai_number = 1
        now_ai_number = 1
        ai = BossTank_2(ai_images)
        ai_group = Group()
        ai_group.add(ai)
    else:
        ai_number = 3
        now_ai_number = 3
        ai_1 = AiTank(ai_images)
        ai_2 = AiTank(ai_images)
        ai_3 = AiTank(ai_images)
        ai_group = Group()
        ai_group.add(ai_1)
        ai_group.add(ai_2)
        ai_group.add(ai_3)

    # boss
    boss = Boss(450, 560)
    # boss group
    boss_group = Group()
    boss_group.add(boss)

    # player
    player = Tank(player_images)

    # player bullet group
    bullet_group = Group()

    # ai_tank bullet group
    ai_bullet_group = Group()

    # tank group
    player_group = Group()
    player_group.add(player)

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

    stage = pygame.image.load(stage_img).convert_alpha()

    #stage number
    stage_number_master = pygame.image.load(stage_number_img).convert_alpha()

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

    #load images
    player_images = load_images(player_tank_path)
    ai_images = load_images(ai_tank_path)
    gift_images = load_images(gift_tank_path)
    boss_1_images = load_images(boss_1_path)
    boss_2_images = load_images(boss_2_path)
    boss_bullet_images = load_images(boss_bullet_path)

    game_stage = 1
    #init game
    # player, boss, player_group, boss_group, ai_group, bullet_group,\
    #     ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game(player_images, ai_images, game_stage)
    # play_music(music_start)

    # bullent images
    bullet_images = load_images(bullet_path)

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
                game_state = 'load_next'

        elif game_state == 'gameover':
            screen.blit(gameover_image, (270, 100))
            myfont = pygame.font.Font(None, 60)
            textImg = myfont.render("Press 'R' to restart game!", True, (0, 0, 255))
            screen.blit(textImg, (220, 430))
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                game_state = 'running'
                game_stage = 1
                player, boss, player_group, boss_group, ai_group, bullet_group,\
                    ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game(player_images, ai_images, game_stage)
                play_music(music_start)

        elif game_state == 'win':
            myfont_1 = pygame.font.Font(None, 80)
            myfont_2 = pygame.font.Font(None, 30)
            textImg_1 = myfont_1.render("YOU WIN!", True, (0, 0, 255))
            textImg_2 = myfont_2.render("Press 'R' to try again!", True, (250, 0, 0))
            screen.blit(textImg_1, (350, 250))
            screen.blit(textImg_2, (380, 300))
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                game_stage = 1
                game_state = 'load_next'

        elif game_state == 'load_next':
            game_state = 'running'
            if game_stage == 3:
                player, boss, player_group, boss_group, ai_group, bullet_group, \
                    ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game(player_images, boss_2_images, game_stage)
            else:
                player, boss, player_group, boss_group, ai_group, bullet_group, \
                    ai_bullet_group, wall_group, gift_group, now_ai_number, tag_point = init_game(player_images, ai_images, game_stage)
            play_music(music_start)

        elif game_state == 'running':
            framerate.tick(30)
            current_time = pygame.time.get_ticks()

            number_rect = Rect(player.get_life() * 14, 0, 14, 12)
            number_img = number_master_img.subsurface(number_rect)

            stage_number = Rect((game_stage-1) * 13, 0, 13, 12)
            stage_number_img = stage_number_master.subsurface(stage_number)

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
                new_bullet = player.shoot(current_time, bullet_images, 300)
                if new_bullet:
                    play_music(music_shoot)
                    bullet_group.add(new_bullet)

            # add ai tank
            if game_stage != 3 and len(ai_group.sprites()) < 5 and now_ai_number < 20:
                if now_ai_number == 6 or now_ai_number == 15:
                    ai_group.add(GiftTank(gift_images))
                elif now_ai_number == 19:
                    ai_group.add(BossTank_1(boss_1_images))
                else:
                    ai_group.add(AiTank(ai_images))
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

            if not ai_group.sprites():
                if game_stage != 3:
                    game_stage += 1
                    game_state = 'load_next'
                else:
                    game_state = 'win'

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
                if ai.get_name() == 'boss':
                    ai_tank_bullet = ai.ai_shoot(current_time, boss_bullet_images, 300)
                else:
                    ai_tank_bullet = ai.ai_shoot(current_time, bullet_images, 300)

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
            screen.blit(stage, (925, 430))
            screen.blit(stage_number_img, (950, 450))
            for tag in tag_point:
                screen.blit(ai_tag, tag)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()