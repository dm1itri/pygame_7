import pygame
import os
import sys

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))




def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (40, 40))
    else:
        image = image.convert_alpha()
        image = pygame.transform.scale(image, (50, 50))
    return image


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
pygame.display.set_caption('Герой двигается!')
clock = pygame.time.Clock()
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png', -1)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)



# основной персонаж
player = None


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def up(k):

    map = [[j for j in i] for i in load_level('map.txt')]
    if k == 1:
        if player.pos_y != 0:
            if map[player.pos_y - 1][player.pos_x] != '#':
                map[player.pos_y - 1][player.pos_x] = '@'
                map[player.pos_y][player.pos_x] = '.'
                player.pos_y -= 1
    elif k == 2:
        if player.pos_y != 9:
            if map[player.pos_y + 1][player.pos_x] != '#':
                map[player.pos_y + 1][player.pos_x] = '@'
                map[player.pos_y][player.pos_x] = '.'
                player.pos_y += 1
    elif k == 3:
        if player.pos_x != 0:
            if map[player.pos_y][player.pos_x - 1] != '#':
                map[player.pos_y][player.pos_x - 1] = '@'
                map[player.pos_y][player.pos_x] = '.'
                player.pos_x -= 1
    elif k == 4:
        if player.pos_x != 9:
            if map[player.pos_y][player.pos_x + 1] != '#':
                map[player.pos_y][player.pos_x + 1] = '@'
                map[player.pos_y][player.pos_x] = '.'
                player.pos_x += 1
    map = [''.join(i) for i in map]
    print('\n'.join(map))
    with open('data/map.txt', 'w') as f:
        f.write('\n'.join(map))



player, level_x, level_y = generate_level(load_level('map.txt'))


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        pygame.display.flip()
        clock.tick(50)

start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up(1)
            if event.key == pygame.K_DOWN:
                up(2)
            if event.key == pygame.K_LEFT:
                up(3)
            if event.key == pygame.K_RIGHT:
                up(4)
    player, level_x, level_y = generate_level(load_level('map.txt'))
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()