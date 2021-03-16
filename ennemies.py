import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, pos, velocity, name, group, spacing=(0, 0)):
        super().__init__()
        self.game = game
        self.image = self.game.images[name]
        self.rect = self.image.get_rect(left=pos[0], top=pos[1] - self.image.get_height()//2, height=self.image.get_height() - 10)
        self.velocity = velocity
        self.x = self.rect.x
        self.group = group
        self.spacing = spacing

    def run(self):
        if self.rect.x > -100:
            self.x -= self.velocity
            self.rect.x = round(self.x)
        else:
            self.group.remove(self)
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.stat = 'game over'
            self.game.player.image = self.game.player_stats[2]
            self.game.player.rect = pygame.Rect(50, 185, 40, 55)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - self.spacing[0], self.rect.y - self.spacing[1]))


class Tree(Obstacle):
    """docstring for Tree"""

    def __init__(self, game, pos, velocity):
        super().__init__(game, pos, game.difficulty, 'tree', game.groupe_ennemies, (0, 10))
        nbr = random.randint(1, 3)
        self.surface = pygame.Surface((self.image.get_width() * nbr, self.image.get_height()))
        self.surface.fill((255, 255, 255))
        [self.surface.blit(self.image.convert_alpha(), (i * self.image.get_width(), 0)) for i in range(nbr)]
        self.image = self.surface.copy().convert_alpha()
        self.rect = self.image.get_rect(left=pos[0], top=pos[1] - self.image.get_height() + 10, height=self.image.get_height() - 10)



class Bird(Obstacle):
    """docstring for Bird"""

    def __init__(self, game, pos, velocity):
        super().__init__(game, (pos[0], pos[1] - 50), game.difficulty + 0.5, 'bird', game.groupe_ennemies)


    def animate(self):
        self.image = self.game.current_bird_image
        
