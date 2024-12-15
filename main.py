import pygame
import sys
import math



class Projectile:
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.speed = 10
        self.vel_x = self.speed * v_x / math.sqrt(v_x**2 + v_y**2)
        self.vel_y = self.speed * v_y / math.sqrt(v_x**2 + v_y**2)
        self.width = 4
        self.height = 10


class Player:
    def __init__(self, x, y, width = 25, height = 25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.bullets = []
    def update_pos(self, keys_pressed):
        if keys_pressed[pygame.K_a]:
            self.x -= self.vel
        if keys_pressed[pygame.K_d]:
            self.x += self.vel
        if keys_pressed[pygame.K_s]:
            self.y += self.vel
        if keys_pressed[pygame.K_w]:
            self.y -= self.vel
    def shoot(self):

    def draw(self, surf):
        surf.fill((0,0,0))
        pygame.draw.rect(surf, pygame.color.THECOLORS['red'], (self.x, self.y, self.width, self.height))
        pygame.display.update()
    def update(self, surf, keys_pressed):
        self.update_pos(keys_pressed)
        self.draw(surf)



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    player = Player(10,10)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        player.update(screen, keys)