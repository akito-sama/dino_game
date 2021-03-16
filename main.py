import pygame
from game import Game
from ennemies import Bird

pygame.init()
pygame.display.set_caption('dino game')
screen = pygame.display.set_mode((600, 300))
running = True

# -------------------- contants ------------------------
COINEVENT = pygame.USEREVENT + 1
black = (0, 0, 0)
DYNOEVENT = pygame.USEREVENT + 2
TREEEVENT = pygame.USEREVENT + 3
UPDATEDIFFICULTY = pygame.USEREVENT + 4
BIRDEVENT = pygame.USEREVENT + 5
DEBUGMODE = False
# ------------------------------------------------------
pygame.time.set_timer(BIRDEVENT, 200, True)
pygame.time.set_timer(COINEVENT, 100)
pygame.time.set_timer(DYNOEVENT, 100)
pygame.time.set_timer(TREEEVENT, 300, True)
pygame.time.set_timer(UPDATEDIFFICULTY, 700, True)
clock = pygame.time.Clock()
game = Game(screen)
while running:
    screen.fill((255, 255, 255))
    for ennemies in game.groupe_ennemies:
        ennemies.draw(screen)
    game.all_coins.draw(screen)
    screen.blit(game.score_surface, (600 - len(str(game.coins)) * 12, 0))
    for coin in game.all_coins:
        if game.stat == "in game":
            coin.run()
        coin.update_animation()
    if game.stat == "in game":
        game.player.saut()
        for tree in game.groupe_ennemies:
            tree.run()
            if DEBUGMODE:
                pygame.draw.rect(screen, (255, 0, 0), tree.rect, 2)
        if DEBUGMODE:
            pygame.draw.rect(screen, (0, 255, 0), game.player.rect, 2)
    elif game.stat == 'game over':
        screen.blit(game.restart.image, game.restart.rect)
    game.player.draw()
    screen.blit(game.current_coin_image, (590 - game.current_coin_image.get_width() - game.score_surface.get_width(), 0))
    clock.tick(60)
    pygame.draw.line(screen, black, (0, 240), (720, 240))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == COINEVENT:
            game.advance_coins()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.stat == 'game over':
            game.restart.event(event)
        elif event.type == DYNOEVENT:
            if game.player.image in game.player_animation:
                game.advance_player()
        if game.stat == "in game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (not game.player.jumping and game.player.rect.y == game.player.initial_y or (game.player.rect.y == game.player.initial_down_y and game.player_stats[3])):
                    game.player.jumping = True
                    game.reset_jump()
                elif event.key == pygame.K_DOWN and not game.player.in_air:
                    game.down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    game.reset_jump()
            elif event.type == TREEEVENT:
                game.spawn_ennemies()
                pygame.time.set_timer(TREEEVENT, 1200, True)
            elif event.type == UPDATEDIFFICULTY:
                game.difficulty += 0.05
                pygame.time.set_timer(UPDATEDIFFICULTY, 700, True)
            elif event.type == BIRDEVENT:
                game.advance_bird()
                for ennemie in game.groupe_ennemies:
                    if isinstance(ennemie, Bird):
                        ennemie.animate()
                pygame.time.set_timer(BIRDEVENT, 200, True)
