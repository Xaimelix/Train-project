import sys
import os
import pygame, DB
from stations import stations_indexes, graph
from stations import dijkstra
from button import Button

# CONST
pygame.init()
width, height = size = 1200, 800
screen = pygame.display.set_mode(size)
running = True
font = pygame.font.SysFont("Arial", 20)
all_sprites = pygame.sprite.Group()
stations = pygame.sprite.Group()
map_group = pygame.sprite.Group()
buttons = pygame.sprite.Group()
clicked_stations = []
find_way = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Map(pygame.sprite.Sprite):
    image = load_image('new_map.jpg')

    def __init__(self):
        super().__init__(map_group)
        self.image = Map.image
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


def find_way_func(stations: list):
    full_way_indexes = []
    start = stations_indexes[stations[0]]
    end = stations_indexes[stations[1]]
    visited = dijkstra(start, end, graph)

    cur_node = end
    if end not in full_way_indexes:
        full_way_indexes.append(end)
    while cur_node != start:
        cur_node = visited[cur_node]
        if cur_node not in full_way_indexes:
            full_way_indexes.append(cur_node)
    return full_way_indexes


# Station consts
BUTTON_UP_IMG = load_image('station_unpressed.jpg')
BUTTON_DOWN_IMG = load_image('station_pressed.jpg')
BUTTON_WAY_STATION_IMG = load_image('station_way.jpg')


class Station(pygame.sprite.Sprite):
    image = BUTTON_UP_IMG

    def __init__(self, pos, index):
        super().__init__(stations, all_sprites)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = Station.image
        self.pressed = 0
        self.index = index
        self.is_station_way = False

    def update(self):
        global clicked_stations
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and len(clicked_stations) < 2:
                self.image = BUTTON_DOWN_IMG
                self.pressed = 1
        if self.is_station_way:
            self.image = BUTTON_WAY_STATION_IMG
        else:
            self.image = past_image


class Button_clear(pygame.sprite.Sprite):
    image = load_image('button_close.png')

    def __init__(self, pos):
        super().__init__(buttons)
        self.image = Button_clear.image
        self.x, self.y = pos
        self.rect = pygame.Rect(pos, Button_clear.image.get_size())
        self.pos = pos
        self.stat = False

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and len(clicked_stations) == 2:
                self.stat = True
            else:
                self.stat = False


Map()
pygame.display.flip()
stations_pos = [(651, 477), (789, 496), (881, 452), (776, 453), (691, 423), (627, 423), (540, 433), (372, 532),
                (897, 433), (796, 335), (765, 306), (686, 280), (593, 310), (541, 367), (553, 410), (860, 299),
                (1018, 308), (1118, 302), (702, 216), (707, 138), (741, 56)]
for index, i in zip(stations_indexes, stations_pos):
    # print(stations_indexes[index])
    Station(i, index)

button_clear_way = Button_clear((100, 100))

# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    map_group.draw(screen)
    stations.draw(screen)
    stations.update()

    for i in stations:
        if i.pressed:
            if len(clicked_stations) < 2 and i.index not in clicked_stations:
                clicked_stations.append(i.index)
        if find_way:
            for j in find_way_func(clicked_stations):
                if j == stations_indexes[i.index]:
                    i.is_station_way = True
        if button_clear_way.stat:
            i.is_station_way = False
    if len(clicked_stations) == 2:
        find_way = True
        buttons.draw(screen)
        buttons.update()

    pygame.display.flip()
pygame.quit()
sys.exit()
