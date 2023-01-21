import os
import sys
from itertools import permutations

import pygame

import DB
from lines import lines_indexes
from start_window import StartWindow
from stations import dijkstra, get_key
from stations import stations_indexes, graph, stations_pos

# CONST
pygame.init()
width, height = size = 1200, 800
screen = pygame.display.set_mode(size)
running = True
font = pygame.font.SysFont("Arial", 20)
all_sprites = pygame.sprite.Group()
stations = pygame.sprite.Group()
map_group = pygame.sprite.Group()
button_line_close = pygame.sprite.Group()
button_info_close = pygame.sprite.Group()
tmp_lines = pygame.sprite.Group()
lines = pygame.sprite.Group()
window = pygame.sprite.Group()
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
BUTTON_INFO_STATION = load_image('station_info.jpg')


class Station(pygame.sprite.Sprite):
    image = BUTTON_UP_IMG

    def __init__(self, pos, index):
        super().__init__(stations, all_sprites)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = Station.image
        self.pressed = 0
        self.pressed_info = 0
        self.index = index
        self.is_station_way = False

    def update(self):
        global clicked_stations
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos) and len(clicked_stations) < 2:
                    self.image = BUTTON_DOWN_IMG
                    self.pressed = 1
                else:
                    self.image = BUTTON_UP_IMG
                    self.pressed = 0
            elif event.button == 3:
                if self.rect.collidepoint(event.pos):
                    self.image = BUTTON_INFO_STATION
                    self.pressed_info = 1
                else:
                    self.image = BUTTON_UP_IMG
                    self.pressed_info = 0

        if self.is_station_way:
            self.image = BUTTON_WAY_STATION_IMG


class Line(pygame.sprite.Sprite):

    def __init__(self, line_num):
        # print(line_num)
        super().__init__(lines)
        if line_num < 20:
            self.pre_image = load_image(f'line{line_num}.png')
            self.num = line_num

        else:
            self.pre_image = load_image(f'line_transfer{line_num}.png')
            self.num = line_num
        self.image = pygame.transform.scale(self.pre_image, size)
        self.rect = self.image.get_rect()


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


class ButtonClear(pygame.sprite.Sprite):
    image = load_image('button_close.png')

    def __init__(self, pos):
        super().__init__(button_line_close)
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


class ButtonCloseInfo(pygame.sprite.Sprite):
    image = load_image('button_close.png')

    def __init__(self, pos):
        super().__init__(button_info_close)
        self.image = ButtonClear.image
        self.x, self.y = pos
        self.rect = pygame.Rect(pos, ButtonClear.image.get_size())
        self.pos = pos
        self.pressed = False

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
            else:
                self.pressed = False


class ButtonStart(pygame.sprite.Sprite):
    image = load_image('start_bu.png')

    def __init__(self, pos):
        super().__init__(window)
        self.image = ButtonStart.image
        self.x, self.y = pos
        self.rect = pygame.Rect(pos, ButtonStart.image.get_size())
        self.pos = pos
        self.pressed = False

    def update(self):
        global status
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                status = 1


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Это не игра",
                  "it's navigator (>.<)"]

    fon = pygame.transform.scale(load_image('train1.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50

    window.draw(screen)
    window.update()

    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def info_text(text):
    fon = load_image('info_screen.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 15
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


counter = 0

Map()
pygame.display.flip()
# Station(pos, index)
for index, i in zip(stations_indexes, stations_pos):
    Station(i, index)
button_clear_way = ButtonClear((size[0] - 100, 50))

# Start window
St_w = StartWindow(size, all_sprites, window)
St_b = ButtonStart((size[0] // 2 - 100, size[1] // 2 - 50))
status = 0

button_close_info = ButtonCloseInfo((200, 10))
show_info = True
get_info = [""]
lines_created = False

# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if status == 0:
        start_screen()

    elif status == 1:

        map_group.draw(screen)
        stations.draw(screen)
        stations.update()
        button_info_close.update()

        for i in stations:
            if i.pressed:
                if len(clicked_stations) < 2 and i.index not in clicked_stations:
                    clicked_stations.append(i.index)
            if i.pressed_info:
                # show_info = True
                if show_info:
                    name, station_status, time = DB.get_info_station_by_index(i.index)
                    get_info = [f'{name}', f'{station_status}', f'{time}']
                    info_text(get_info)
                    button_info_close.draw(screen)

            if find_way:
                for j in find_way_func(clicked_stations):
                    if j == stations_indexes[i.index]:
                        i.is_station_way = True
                if not lines_created:
                    for line in search_lines(find_way_func(clicked_stations)):
                        Line(line)
                    counter = search_lines(find_way_func(clicked_stations))
                    lines_created = True
            if button_clear_way.pressed:
                i.is_station_way = False
                clicked_stations.clear()
                find_way = False
                lines_created = False
                lines.empty()
                tmp_lines.empty()

            if button_close_info.pressed:
                # get_info.clear()
                i.pressed_info = False




        if len(clicked_stations) == 2:
            find_way = True
            button_line_close.draw(screen)
            button_line_close.update()
        if lines_created:
            if 0 < len(counter) <= len(lines):
                pygame.time.wait(500)
                current = counter.pop(0)
                for sprite in lines:
                    if current == sprite.num:
                        tmp_lines.add(sprite)
                tmp_lines.draw(screen)
            else:
                lines.draw(screen)

    pygame.display.flip()
pygame.quit()
sys.exit()
