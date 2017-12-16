import pygame

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Tank Wars')
    tank = pygame.image.load('ttank.png').convert()

    while 1:

        screen.blit(tank, (100, 100))
        pygame.display.update()