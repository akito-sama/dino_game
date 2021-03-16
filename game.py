import pygame
import player
from itertools import cycle
from ennemies import Tree, Bird
import random
import coins
from buttons import Restart


class Game:
    """docstring for Game"""

    def __init__(self, screen):
        self.player = player.Player(self)
        self.coin_animation = cycle([pygame.transform.scale(pygame.image.load(f"sprites/coin/l0_sprite_{i}.png"), (32, 32)).convert_alpha() for i in range(1, 9)])
        self.player_animation = [pygame.transform.scale(pygame.image.load(f"sprites/dino walk/dino{f'{(2 - len(str(i))) * str(0)}{i}'}.png"), (64, 64)).convert_alpha() for i in range(0, 16)]
        self.player_stats = (self.player_animation[0], pygame.transform.scale(pygame.image.load("sprites/dino image/jump.png"), (64, 64)).convert_alpha(), pygame.transform.scale(pygame.image.load("sprites/dino image/game over.png"), (64, 64)).convert_alpha(), pygame.transform.scale(pygame.image.load('sprites/minidino.png'), (64, 38)))
        self.images = {
        "tree": pygame.transform.scale(pygame.image.load('sprites/tree.png'), (30, 51)).convert_alpha(),
        "bird": pygame.image.load("sprites/bird/bird0.png")
        }
        self.animation_bird = tuple(pygame.image.load(f"sprites/bird/bird{i}.png") for i in range(6))
        self.animation_bird = cycle((*self.animation_bird, *tuple(self.animation_bird)[::-1]))
        self.screen = screen
        self.stat = "in game"
        self.index = 0
        self.groupe_ennemies = pygame.sprite.Group()
        self.advance_player()
        self.advance_coins()
        self.coins = 0
        self.advance_bird()
        self.nbr_font = pygame.font.SysFont('arial', 25, bold=True)
        self.score_surface = self.nbr_font.render(str(self.coins), False, (0, 0, 0))
        self.all_coins = pygame.sprite.Group()
        self.restart = Restart(self)
        self.last_place = 800
        self.difficulty = 4.5
        self.all_ennemie_class = (Tree, Bird)

    def advance_coins(self):
    	self.current_coin_image = next(self.coin_animation)

    def advance_bird(self):
        self.current_bird_image = next(self.animation_bird)

    def advance_player(self):
        self.player.image = self.player_animation[self.index]
        if self.index != len(self.player_animation) - 1:
            self.index += 1
        else:
            self.index = 0

    def spawn_ennemies(self):
        coord = (random.randint(self.last_place, self.last_place + 60), 240)
        self.last_place = coord[0]
        ennemie = random.choice(self.all_ennemie_class)(self, coord, self.difficulty)
        self.groupe_ennemies.add(ennemie)
        self.last_place = random.randint(self.last_place + 75, self.last_place + 120)
        self.all_coins.add(coins.Coin(self, (random.randint(self.last_place, self.last_place + 300), coord[1] - 10), self.difficulty))

    def restarte(self):
        self.__init__(self.screen)
        pygame.time.set_timer(pygame.USEREVENT + 3, 300, True)
        pygame.time.set_timer(pygame.USEREVENT + 4, 700, True)
        pygame.time.set_timer(pygame.USEREVENT + 5, 200, True)
        self.last_place = 800

    def reset_jump(self):
        self.player.image = self.player_stats[0]
        self.player.rect = pygame.Rect(50, 185, 40, 55)
        self.player.spacing = (10, 10)

    def down(self):
        self.player.image = self.player_stats[3]
        self.player.rect = self.player.down_rect
        self.player.spacing = (0, 10)
