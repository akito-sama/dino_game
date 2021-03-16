import pygame


class Button:
    """docstring for button"""

    def __init__(self, image_path, pos, func):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(left=pos[0] - self.image.get_width()//2, top=pos[1])
        self.func = func

    def event(self, event):
        if self.rect.collidepoint(event.pos):
            self.func()


class Restart(Button):

    def __init__(self, game):
        self.game = game
        super().__init__('sprites/restart.png', (300, 50), self.game.restarte)
