import sys
import os
import pygame, DB

# CONST
pygame.init()
width, height = size = 1200, 800
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
stations = pygame.sprite.Group()
map_group = pygame.sprite.Group()


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


BUTTON_UP_IMG = load_image('station_unpressed.jpg')
BUTTON_DOWN_IMG = load_image('station_pressed.jpg')
st1 = False
st2 = False


class Station(pygame.sprite.Sprite):
    image = BUTTON_UP_IMG

    def __init__(self, pos):
        super().__init__(stations, all_sprites)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image = Station.image
        self.pressed = 1

    def update(self):
        global st1, st2
        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        # if self.rect.collidepoint(pygame.mouse.get_pos()):
        #     if pygame.mouse.get_pressed()[0] and self.pressed == 1:
        #         self.pressed = 0
        #         self.image = load_image('station_pressed.jpg')
        # if pygame.mouse.get_pressed() == (0, 0, 0):
        #     self.pressed = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = BUTTON_DOWN_IMG

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     # if event.button == 1:
        #     #     self.image = BUTTON_UP_IMG


Map()
pygame.display.flip()
stations_pos = [(372, 531), (539, 435), (627, 425), (692, 427), (779, 454), (883, 454), (792, 498), (651, 480),
                (555, 412), (543, 369), (595, 310), (688, 280), (766, 306), (799, 336), (898, 432), (1122, 305),
                (1023, 312), (861, 301), (705, 217), (711, 143), (745, 55)]
for i in stations_pos:
    Station(i)

# MAIN LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    map_group.draw(screen)
    stations.draw(screen)
    stations.update()
    pygame.display.flip()
pygame.quit()
sys.exit()
