import pygame


class Coin(pygame.sprite.Sprite):

    def __init__(self, game, pos, velocity):
        super().__init__()
        self.game = game
        self.image = self.game.current_coin_image
        self.rect = self.image.get_rect(top=pos[1] - 20, left=pos[0])
        self.velocity = velocity
        self.x = self.rect.x

    def run(self):
        if self.rect.x > -50:
            self.x -= self.velocity
            self.rect.x = round(self.x)
        else:
            self.remove(self.game.all_coins)
        if pygame.sprite.collide_rect(self, self.game.player):
            self.remove(self.game.all_coins)
            self.game.coins += 1
            self.game.score_surface = self.game.nbr_font.render(str(self.game.coins), False, (0, 0, 0))

    def update_animation(self):
        self.image = self.game.current_coin_image
