import pygame
from math import ceil
from itertools import accumulate


class Player(pygame.sprite.Sprite):
    """docstring for Player"""

    def __init__(self, game):
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load("sprites/dino.png"), (64, 64)).convert_alpha()
        self.rect = pygame.Rect(50, 185, 40, 55)
        self.initial_rect = self.rect.copy()
        self.initial_y = self.rect.y + 2
        self.gravity_value = None
        self.jumping = False
        self.y_velocity = 1
        self.gravity_down = [0, 0, 0, *accumulate([1] * 13)]
        self.gravity_up = [*accumulate([-0.8] * 11)][::-1]
        self.y = self.rect.y
        self.index = 0
        self.dico_direc = {True: self.gravity_up, False: self.gravity_down}
        self.advance_gravity()
        self.counter = 0
        self.in_air = True
        self.down_rect = pygame.Rect((40, 211), (48, 28))
        self.spacing = (10, 10)
        self.initial_down_y = 211

    def draw(self):
        self.game.screen.blit(self.image, (self.rect.x - self.spacing[0], self.rect.y - self.spacing[1]))

    def saut(self):
        if self.jumping:
            self.in_air = True
            self.image = self.game.player_stats[1]
            self.gravity()
            if self.rect.y <= 108:
                self.jumping = False
                self.index = 0
                self.rect.y = 108
        elif self.rect.y <= 186:
            self.gravity()
            self.in_air = True
            if self.rect.y >= 187:
                self.index = 0
                self.rect.y = 187
                self.counter = 0
                self.advance_gravity()
                self.image = self.game.player_stats[0]
                self.game.index = 0
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.game.down()
        else:
            self.in_air = False

    def gravity(self):
        self.y = (self.rect.y + self.gravity_value)
        self.rect.y = ceil(self.y)
        if self.counter == 5 or self.gravity_value == 0:
            self.advance_gravity()
            self.counter = 0
        self.counter += 1
        if pygame.key.get_pressed()[pygame.K_DOWN] and not self.jumping:
            self.gravity_value = self.dico_direc[self.jumping][-1]

    def advance_gravity(self):
        try:
            self.gravity_value = self.dico_direc[self.jumping][self.index]
            self.index += 1
        except IndexError:
            self.__init__(self.game)
