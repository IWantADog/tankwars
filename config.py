from point import Point
import pygame

img_width = 40
img_height = 40
windows_width = 1000
windows_height = 600
area_width = 900
area_height = 600
bullet_width = 5
bullet_height = 5
default_point = (370, 560)
ai_number = 20
start_music = 'music\\start.ogg'
shoot_music = 'music\\shoot.wav'
player_tank_path = ['images\\player_tank\\m1-1-1.png', 'images\\player_tank\\m1-1-2.png',
                    'images\\player_tank\\m1-2-1.png', 'images\\player_tank\\m1-2-2.png',
                    'images\\player_tank\\m1-3-1.png', 'images\\player_tank\\m1-3-2.png',
                    'images\\player_tank\\m1-4-1.png', 'images\\player_tank\\m1-4-2.png']

ai_tank_path = ['images\\ai_tank\\1-1-1.png', 'images\\ai_tank\\1-1-2.png',
                'images\\ai_tank\\1-2-1.png', 'images\\ai_tank\\1-2-2.png',
                'images\\ai_tank\\1-3-1.png', 'images\\ai_tank\\1-3-2.png',
                'images\\ai_tank\\1-4-1.png', 'images\\ai_tank\\1-4-2.png']

bullet_path = ['images\\bullet\\up.png', 'images\\bullet\\down.png',
               'images\\bullet\\right.png', 'images\\bullet\\left.png']

boss_bullet_path = ['images\\final_boss_bullet\\up.png', 'images\\final_boss_bullet\\down.png',
               'images\\final_boss_bullet\\right.png', 'images\\final_boss_bullet\\left.png']

ai_boss_img = 'img\\ai_boss.png'
gift_tank_path = ['images\\gift_tank\\dj1-1-1.png', 'images\\gift_tank\\dj1-1-2.png',
                 'images\\gift_tank\\dj1-2-1.png', 'images\\gift_tank\\dj1-2-2.png',
                 'images\\gift_tank\\dj1-3-1.png', 'images\\gift_tank\\dj1-3-2.png',
                 'images\\gift_tank\\dj1-4-1.png', 'images\\gift_tank\\dj1-4-2.png']

boss_1_path = ['images\\boss_tank\\m21-1-1.png', 'images\\boss_tank\\m21-1-2.png',
               'images\\boss_tank\\m21-2-1.png', 'images\\boss_tank\\m21-2-2.png',
               'images\\boss_tank\\m21-3-1.png', 'images\\boss_tank\\m21-3-2.png',
               'images\\boss_tank\\m21-4-1.png', 'images\\boss_tank\\m21-4-2.png']

boss_2_path = ['images\\final_boss\\boss1-1-1.png', 'images\\final_boss\\boss1-1-2.png',
               'images\\final_boss\\boss1-2-1.png', 'images\\final_boss\\boss1-2-2.png',
               'images\\final_boss\\boss1-3-1.png', 'images\\final_boss\\boss1-3-2.png',
               'images\\final_boss\\boss1-4-1.png', 'images\\final_boss\\boss1-4-2.png']

clock_img = 'images\\others\\clock.png'
one_life_img = 'images\\others\\one_life.png'
birth_img = 'images\\others\\birth.png'
boom_img = 'images\\others\\boom.png'
boss_birth_img = 'images\\others\\boss_birth.png'
boss_boom_img = 'images\\others\\boss_boom.png'
brickwall_img = 'images\\others\\brickwall.png'
steelwall_img = 'images\\others\\steelwall.png'
boss_img= 'images\\others\\boss.png'
background = 'images\\others\\bg.png'
ai_tank_tag = 'images\\others\\ai_tank_tag.png'
player_img = 'images\\others\\player.png'
number_img = 'images\\others\\number.png'
start_img = 'images\\others\\start.png'
gameover_img = 'images\\others\\gameover.png'


def load_images(images_list):
    return [pygame.image.load(item).convert_alpha() for item in images_list]

