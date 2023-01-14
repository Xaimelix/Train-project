import sys
import os
import pygame, DB
from stations import stations_indexes, graph
from stations import dijkstra

# CONST
pygame.init()
width, height = size = 1200, 800
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
stations = pygame.sprite.Group()
map_group = pygame.sprite.Group()
clicked_stations = []


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


# Click consts
BUTTON_UP_IMG = load_image('station_unpressed.jpg')
BUTTON_DOWN_IMG = load_image('station_pressed.jpg')


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

    def update(self):
        global clicked_stations
        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        # if self.rect.collidepoint(pygame.mouse.get_pos()):
        #     if pygame.mouse.get_pressed()[0] and self.pressed == 1:
        #         self.pressed = 0
        #         self.image = load_image('station_pressed.jpg')
        # if pygame.mouse.get_pressed() == (0, 0, 0):
        #     self.pressed = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and len(clicked_stations) < 2:
                self.image = BUTTON_DOWN_IMG
                self.pressed = 1

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     # if event.button == 1:
        #     #     self.image = BUTTON_UP_IMG


Map()
pygame.display.flip()
stations_pos = [(651, 477), (789, 496), (881, 452), (776, 453), (691, 423), (627, 423), (540, 433), (372, 532),
                (897, 433), (796, 335), (765, 306), (686, 280), (593, 310), (541, 367), (553, 410), (860, 299),
                (1018, 308), (1118, 302), (702, 216), (707, 138), (741, 56)]
for index, i in zip(stations_indexes, stations_pos):
    # print(stations_indexes[index])
    Station(i, index)

# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     stations_pos.append(event.pos)
    map_group.draw(screen)
    stations.draw(screen)
    for i in stations:
        if i.pressed:
            if len(clicked_stations) < 2 and i.index not in clicked_stations:
                clicked_stations.append(i.index)
    stations.update()
    pygame.display.flip()

start = stations_indexes[clicked_stations[0]]
end = stations_indexes[clicked_stations[1]]
visited = dijkstra(start, end, graph)

cur_node = end
print(end)
while cur_node != start:
    cur_node = visited[cur_node]
    print(cur_node)


pygame.quit()
sys.exit()
