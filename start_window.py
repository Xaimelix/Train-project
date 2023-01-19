import os
import sys
import pygame

pygame.init()
size = width, height = 200, 200
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class StartWindow(pygame.sprite.Sprite):
    image = load_image('start.png')

    def __init__(self, size, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = StartWindow.image
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass


# class StartButton(pygame.sprite.Sprite):
#     image = load_image('start_bu.png')
#
#     def __init__(self, pos, *sprite_groups):
#         super().__init__(*sprite_groups)
#         self.image = StartWindow.image
#         self.x, self.y = pos
#         self.rect = pygame.Rect(pos, StartButton.image.get_size())
#         self.rect.x = 0
#         self.rect.y = 0
#         self.pressed = False
#
#     def update(self):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.rect.collidepoint(event.pos):
#                 self.pressed = True
#             else:
#                 self.pressed = False


# a = pygame.sprite.Group()
# StartButton((0, 0), a)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         a.draw(screen)
#         a.update()
