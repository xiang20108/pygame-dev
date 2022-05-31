import pygame
import os
import sys
import random

WIDTH = 800
HEIGHT = 600
FPS = 60

BACKGROUND = (32, 32, 32)


# Initialization
pygame.display.init()
pygame.mixer.init()


# Loading Resource
start_page = pygame.image.load(os.path.join('assets', 'images', 'start_page.png'))
win = pygame.image.load(os.path.join('assets', 'images', 'win.png'))
game_over = pygame.image.load(os.path.join('assets', 'images', 'game_over.png'))
init = pygame.image.load(os.path.join('assets', 'images', 'init.png'))
flag = pygame.image.load(os.path.join('assets', 'images', 'flag.png'))
icon = pygame.image.load(os.path.join('assets', 'images', 'bomb_64px.png'))
bomb_value = {}
for n in range(10):
    bomb_value[n] = pygame.image.load(os.path.join('assets', 'images', f'{n}.png'))
click_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'click.mp3'))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper Game')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.value = None
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.state = 0
        self.image = init
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
    
    def update(self):
        if self.state == 0:
            self.image = init
        elif self.state == 1:
            self.image = bomb_value[self.value]
        elif self.state == 2:
            self.image = flag
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)



def setting_bombs(bombs, pos_x, pos_y):
    random_list = [n for n in range(16 * 16)]
    random.shuffle(random_list)
    bomb_map = [[0 for i in range(18)]for j in range(18)]

    random_list.remove(pos_y * 16 + pos_x)
    if pos_x > 0 and pos_y > 0:
        random_list.remove((pos_y - 1) * 16 + (pos_x - 1))
    if pos_y > 0:
        random_list.remove((pos_y - 1) * 16 + pos_x)
    if pos_x < 15 and pos_y > 0:
        random_list.remove((pos_y - 1) * 16 + (pos_x + 1))
    if pos_x > 0:
        random_list.remove(pos_y * 16 + (pos_x - 1))
    if pos_x < 15:
        random_list.remove(pos_y * 16 + (pos_x + 1))
    if pos_x > 0 and pos_y < 15:
        random_list.remove((pos_y + 1) * 16 + (pos_x - 1))
    if pos_y < 15:
        random_list.remove((pos_y + 1) * 16 + pos_x)
    if pos_x < 15 and pos_y < 15:
        random_list.remove((pos_y + 1) * 16 + (pos_x + 1))
    
    for n in range(40):
        bomb_map[random_list[n]//16 + 1][random_list[n]%16 + 1] = 9


    for j in range(1, 17):
        for i in range(1, 17):
            if bomb_map[j][i] == 9:
                if bomb_map[j - 1][i - 1] != 9:
                    bomb_map[j - 1][i - 1] += 1
                if bomb_map[j - 1][i] != 9:
                    bomb_map[j - 1][i] += 1
                if bomb_map[j - 1][i + 1] != 9:
                    bomb_map[j - 1][i + 1] += 1
                if bomb_map[j][i - 1] != 9:
                    bomb_map[j][i - 1] += 1
                if bomb_map[j][i + 1] != 9:
                    bomb_map[j][i + 1] += 1
                if bomb_map[j + 1][i - 1] != 9:
                    bomb_map[j + 1][i - 1] += 1
                if bomb_map[j + 1][i] != 9:
                    bomb_map[j + 1][i] += 1
                if bomb_map[j + 1][i + 1] != 9:
                    bomb_map[j + 1][i + 1] += 1
                

    for j in range(1, 17):
        for i in range(1, 17):
            bombs[j - 1][i - 1].value = bomb_map[j][i]
            print(bomb_map[j][i], end=' ')
        print()


def expansion(bombs, pos_x, pos_y):
    pass

all_sprites = pygame.sprite.Group()
bombs = [[Bomb((i + 1) * 32, (j + 1) * 32)for i in range(16)]for j in range(16)]
for j in range(16):
    for i in range(16):
        all_sprites.add(bombs[j][i])

game_state = 0
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = event.pos
            # click_sound.play()
            pos_x //= 32
            pos_y //= 32
            if pos_x < 1 or pos_x > 16 or pos_y < 1 or pos_y > 16:
                continue
            if game_state == 0:
                setting_bombs(bombs, pos_x, pos_y)
                game_state = 1
            print(pos_x, pos_y)
            bombs[pos_y - 1][pos_x - 1].state = 1
        
    
        
    screen.fill(BACKGROUND)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()

