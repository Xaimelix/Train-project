import random
import sys
import os
from itertools import permutations

import pygame, DB
from stations import stations_indexes, graph, stations_pos
from stations import dijkstra, get_key
from button import Button
from lines import lines_indexes

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
lines = pygame.sprite.Group()
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
    if stations:
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
    else:
        return False


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
            else:
                self.image = BUTTON_UP_IMG
                self.pressed = 0
        if self.is_station_way:
            self.image = BUTTON_WAY_STATION_IMG


class Line(pygame.sprite.Sprite):

    def __init__(self, line_num):
        super().__init__(lines)
        if line_num < 20:
            self.pre_image = load_image(f'line{line_num}.png')
            self.num = line_num

        else:
            self.pre_image = load_image(f'line_transfer{line_num}.png')
            self.num = line_num
        self.image = pygame.transform.scale(self.pre_image, size)
        self.rect = self.image.get_rect()


class ButtonClear(pygame.sprite.Sprite):
    image = load_image('button_close.png')

    def __init__(self, pos):
        super().__init__(buttons)
        self.image = ButtonClear.image
        self.x, self.y = pos
        self.rect = pygame.Rect(pos, ButtonClear.image.get_size())
        self.pos = pos
        self.pressed = False

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and len(clicked_stations) == 2:
                self.pressed = True
            else:
                self.pressed = False


Map()
pygame.display.flip()
for index, i in zip(stations_indexes, stations_pos):
    Station(i, index)

button_clear_way = ButtonClear((100, 100))
for_lines = []


def search_lines(stations: list):
    indexes = []
    res_lines = []
    for k, v in lines_indexes.items():
        for st_str in stations:
            if get_key(stations_indexes, st_str) not in indexes:
                indexes.append(get_key(stations_indexes, st_str))
        for i in permutations(indexes, 2):
            if i == v:
                if k not in res_lines:
                    res_lines.append(k)
    return res_lines


lines_drawn = False

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
            if not lines_drawn:
                for line in search_lines(find_way_func(clicked_stations)):
                    Line(line)
                lines_drawn = True
        if button_clear_way.pressed:
            i.is_station_way = False
            clicked_stations.clear()
            find_way = False

            lines_drawn = False
            lines.empty()
    button_clear_way.pressed = False
    if len(clicked_stations) == 2:
        find_way = True
        buttons.draw(screen)
        buttons.update()
    if lines_drawn:
        lines.draw(screen)
    pygame.display.flip()
pygame.quit()
sys.exit()
