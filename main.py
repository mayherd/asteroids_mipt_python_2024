import classes, pygame, sys

def redraw_game_window(surf: pygame.SurfaceType, player: classes.Player, nature: classes.Nature):
    surf.fill((0,0,0))
    nature.draw(surf)
    player.draw(surf)
    pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    player = classes.Player(400,400, pygame.time.get_ticks())
    nature = classes.Nature(pygame.time.get_ticks())

    checker = True
    while True:
        clock.tick(36)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if player.lives > 0:
            player.update(keys, nature, screen)
            nature.update(screen)
            redraw_game_window(screen, player, nature)
        else:
            #screen.blit(pygame.image.load("misc/end_screen.png"), (0, 0))
            if keys[pygame.K_SPACE]:
                player = classes.Player(400, 400, pygame.time.get_ticks())
                nature = classes.Nature(pygame.time.get_ticks())
                checker = True
                continue
            if checker:
                n1font = pygame.font.Font("misc/munro.ttf", 150)
                fin1 = n1font.render("GAME OVER", 1, pygame.color.THECOLORS["white"])
                n2font = pygame.font.Font("misc/munro.ttf", 60)
                fin2 = n2font.render("PRESS \"SPACE\" TO PLAY AGAIN", 1, pygame.color.THECOLORS["white"])
                checker = False
            screen.blit(fin1, (screen.get_width() // 2 - fin1.get_width() // 2, screen.get_height() // 2 - fin1.get_height() // 2 - 50))
            screen.blit(fin2, (screen.get_width() // 2 - fin2.get_width() // 2, screen.get_height() // 2 - fin2.get_height() // 2 + 50))
            pygame.display.update()