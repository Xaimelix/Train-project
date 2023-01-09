pygame.init()
all_sprites = pygame.sprite.Group()
lines = pygame.sprite.Group()
coords = []
a = DB.get_points()
b, c = 0, 0


class Line(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(lines, all_sprites)


for i in range(len(a)):
    if a[i] == '(':
        b = i
    if a[i] == ')':
        c = i
        line = a[b + 1: c].split(';')
        if ',' in line[0]:
            line[0] = line[0].replace(',', '.')
        if ',' in line[1]:
            line[1] = line[1].replace(',', '.')
        coords.append([(float(line[0])), (float(line[1]))])
        b, c = 0, 0
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
white = pygame.Color('black')
black = pygame.Color('white')
k = 1
coords1 = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
            k *= 2
        if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
            k /= 2
    for i in coords:
        # координаты отрицательные, потому что в пайгейм другая система (0,0) это край экрана
        x, y = i[0], -i[1]
        coords1.append([float(x * k + size[0] / 2), float(y * k + size[1] / 2)])
    screen.fill(black)
    pygame.draw.polygon(screen, white, coords1, 3)
    coords1 = []
    pygame.display.flip()
