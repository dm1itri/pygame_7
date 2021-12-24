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


def load_image(name, color_key=None, size=(50, 50)):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = pygame.transform.scale(image, (40, 40))
    else:
        image = image.convert_alpha()
        image = pygame.transform.scale(image, size)
    return image


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
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


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


def up(k, MAP):
    if k == 1:
        if player.pos_y != 0:
            if MAP[player.pos_y - 1][player.pos_x] != '#':
                #MAP[player.pos_y - 1][player.pos_x] = '@'
                MAP[player.pos_y][player.pos_x] = '.'
                player.pos_y -= 1
    elif k == 2:
        if player.pos_y < 10:
            if MAP[player.pos_y + 1][player.pos_x] != '#':
                #MAP[player.pos_y + 1][player.pos_x] = '@'
                MAP[player.pos_y][player.pos_x] = '.'
                player.pos_y += 1
    elif k == 3:
        if player.pos_x != 0:
            if MAP[player.pos_y][player.pos_x - 1] != '#':
                #MAP[player.pos_y][player.pos_x - 1] = '@'
                MAP[player.pos_y][player.pos_x] = '.'
                player.pos_x -= 1
    elif k == 4:
        if player.pos_x < 10:
            if MAP[player.pos_y][player.pos_x + 1] != '#':
                #MAP[player.pos_y][player.pos_x + 1] = '@'
                MAP[player.pos_y][player.pos_x] = '.'
                player.pos_x += 1
    #print(*MAP, sep='\n', end='\n\n')
    return MAP


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.init()
    intro_text = 'Введите название уровня через консоль'

    fon = load_image('fon.jpg', size=size)
    screen.blit(fon, (0, 0))
    #pygame.display.flip()

    font = pygame.font.Font(None, 30)
    text = font.render(intro_text, True, (0, 0, 0))

    screen.blit(text, (50, 20))
    pygame.display.flip()
    #running = True
    #while running:
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #terminate()
            #elif event.type == pygame.KEYDOWN or \
                    #event.type == pygame.MOUSEBUTTONDOWN:
    return load_level(input())


size = width, height = 550, 550
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

# основной персонаж
player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


try:
    player, level_x, level_y = generate_level(MAP := start_screen())
    MAP = [[j for j in i] for i in MAP]
    print(2)
except Exception as e:
    print(e)

else:
    print(1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    MAP = up(1, MAP)
                if event.key == pygame.K_DOWN:
                    MAP = up(2, MAP)
                if event.key == pygame.K_LEFT:
                    MAP = up(3, MAP)
                if event.key == pygame.K_RIGHT:
                    MAP = up(4, MAP)
            # screen.fill('white')
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
