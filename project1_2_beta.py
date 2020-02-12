# Ага
import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# инициализация Pygame:
pygame.init()
# размеры окна:
mashtab = 1
gravity = 5
size = width, height = 640 * mashtab, 480 * mashtab
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)

# Groups
all_sprites = pygame.sprite.Group()
Mario_group = pygame.sprite.Group()
Blocks_group = pygame.sprite.Group()


# Gero
class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(Mario_group)
        self.image = load_image("Mario_mini.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.storons = []  # Список сторон в которые он идёт
        self.napravlenie = 1
        self.padenie2 = False
        self.k1 = 1
        self.k11 = 0
        self.pryzhok = False
        self.sel = False
        self.speed = 1  # Скорость
        self.g = 9.8  # Ускорение вниз
        self.image = pygame.transform.flip(self.image, True, False)

    def get_Mario_rect(self):
        return self.rect

    # Обновление героя
    def update(self, *args):
        # Если нажали клавишу
        if self.pryzhok and self.k11 != 1500:
            self.k11 += 10
            if self.k11 % 300 == 0:
                self.k1 += 0
        elif self.k11 == 1500:
            self.k11 = 0
            self.k1 = 1
            self.pryzhok = False
        elif not self.pryzhok:
            self.k11 = 0
            self.k1 = 1
        if args[0].type == pygame.KEYDOWN:
            if args[0].key == 119 or args[0].key == 273 or args[0].key == 32:
                # 'w'
                if not self.padenie2:
                    self.pryzhok = True
                    self.padenie2 = False
            elif args[0].key == 115 or args[0].key == 274:
                # 's'
                self.sel = True
            elif args[0].key == 100 or args[0].key == 275:
                # 'd'
                self.storons.append(args[0])
            elif args[0].key == 97 or args[0].key == 276:
                # 'a'
                self.storons.append(args[0])
        # Если клавишу отпустили
        elif args[0].type == pygame.KEYUP:
            if args[0].key == 119 or args[0].key == 273 or args[0].key == 32:
                # 'w'
                self.pryzhok = False
                self.padenie2 = True
            elif args[0].key == 115 or args[0].key == 274:
                # 's'
                self.sel = False
            elif args[0].key == 100 or args[0].key == 275:
                # 'd'
                for key in self.storons:
                    if key.key == args[0].key:
                        self.storons.remove(key)
            elif args[0].key == 97 or args[0].key == 276:
                # 'a'
                for key in self.storons:
                    if key.key == args[0].key:
                        self.storons.remove(key)

    # Функция падения
    def padenie(self):
        # Пока Марио не сталкивается с кем нибудь, тогда он падает
        if not pygame.sprite.spritecollideany(self, Blocks_group) and not self.pryzhok:
            if self.rect.y + self.speed < height:
                self.padenie2 = True
                self.rect.y += self.speed
            else:
                self.kill()
        else:
            self.padenie2 = False

    # Функция движения
    def Moving(self):
        if self.pryzhok:
            # 'w'
            self.rect.y -= 1 * self.k1
        if self.sel:
            # 's'
            pass
        if self.storons:
            self.storon = self.storons[-1]
            if self.storon.key == 100 or self.storon.key == 275:
                # 'd'
                if self.rect.x + 40 + self.speed <= width:
                    self.rect.x += self.speed
                if self.napravlenie == 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.napravlenie = 1
            elif self.storon.key == 97 or self.storon.key == 276:
                # 'a'
                if self.rect.x - self.speed >= 0:
                    self.rect.x -= self.speed
                if self.napravlenie == 1:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.napravlenie = 0


class Mario_Border(Mario):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect.x = x
        self.rect.y = y

    def padenie(self):
        # Пока Марио не сталкивается с кем нибудь, тогда он падает
        if not pygame.sprite.spritecollideany(self, Blocks_group) and not self.pryzhok:
            if self.rect.y + self.speed < height:
                self.padenie2 = True
                self.rect.y += self.speed
            else:
                self.kill()
        else:
            self.padenie2 = False


# Blocks
class Blocks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(Blocks_group, all_sprites)
        self.image = load_image("pol.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        pass


# Инициализация врагов, героя и блоков, уровень 1
Gero = Mario(80, 0)
for i in range(10):
    Blocks(i * 40, 200)

# ожидание закрытия окна:
clock = pygame.time.Clock()
MYEVENTTYPE = 1
k = 0
pygame.time.set_timer(MYEVENTTYPE, 10)
running = True
screen.fill((0, 0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            k += 10
            Gero.padenie()
            Gero.Moving()
        Mario_group.update(event)
        if event.type != pygame.ACTIVEEVENT:
            # print(event)
            pass
    screen.fill((0, 0, 0))
    Mario_group.draw(screen)
    Blocks_group.draw(screen)
    pygame.display.flip()
    clock.tick(30)
# завершение работы:
pygame.quit()
