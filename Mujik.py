import pygame


class Mujik(pygame.sprite.Sprite):
    GREEN = (0, 255, 0)

    def __init__(self, hp=100, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/mujik.png')
        self.rect = self.image.get_rect()
        self._hp = hp
        self._x = x
        self._y = y
        self.update_rect_centre()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, self.GREEN, pygame.Rect(self.rect[0] - 76, self.rect[1] - 76,
                                                          72*3, 72*3), width=5)

    def update_rect_centre(self):
        self.rect.center = (70+72*self._x, 70+72*self._y)

    def get_location(self):
        return self._x, self._y

    def get_hp(self):
        return self._hp

    def change_hp(self, amount=1):
        self._hp += amount

    def move_up(self, d=1):
        self._y -= d
        self.update_rect_centre()

    def move_down(self, d=1):
        self._y += d
        self.update_rect_centre()

    def move_left(self, d=1):
        self._x -= d
        self.update_rect_centre()

    def move_right(self, d=1):
        self._x += d
        self.update_rect_centre()
