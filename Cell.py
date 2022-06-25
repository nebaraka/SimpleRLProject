import pygame


class Cell(pygame.sprite.Sprite):
    WHITE = (255, 255, 255)
    PURPLE = (166, 21, 206)
    YELLOW = (240, 240, 20)
    ORANGE = (240, 151, 20)
    RED = (255, 0, 0)

    def __init__(self, state=0, previous_state=None, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image.fill(self.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (70+72*x, 70+72*y)
        self._state = state
        self._previous_state = previous_state

    def draw(self, surface):
        if self._state == 0:
            pygame.draw.rect(surface, self.WHITE, self.rect, width=3)
        elif self._state == 1:
            pygame.draw.rect(surface, self.PURPLE, self.rect)
        elif self._state == 2:
            pygame.draw.rect(surface, self.YELLOW, self.rect)
        elif self._state == 3:
            pygame.draw.rect(surface, self.ORANGE, self.rect)
        elif self._state == 4:
            pygame.draw.rect(surface, self.RED, self.rect)

    def set_state(self, state):
        self._previous_state = self._state
        self._state = state
        return self._previous_state

    def get_state(self):
        return self._state

    def get_previous_state(self):
        return self._previous_state

    def __str__(self):
        return self._state
