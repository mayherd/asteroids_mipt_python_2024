import pygame, sys, math, random
from pygame import SurfaceType


class MovingObject:
    def __init__(self, x, y, v_x, v_y, speed : int):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.speed = speed
        self.vel_x = self.speed * v_x / math.sqrt(v_x ** 2 + v_y ** 2)
        self.vel_y = self.speed * v_y / math.sqrt(v_x ** 2 + v_y ** 2)
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y


class Projectile(MovingObject):
    def __init__(self, x, y, v_x, v_y):
        MovingObject.__init__(self, x, y, v_x, v_y, speed = 10)
        self.width = 7
        self.height = 7


class Asteroid(MovingObject):
    def __init__(self, x, y, v_x, v_y):
        MovingObject.__init__(self, x, y, v_x, v_y, speed = 5)
        self.width = 40
        self.height = 40


class Nature:
    def __init__(self):
        self.asteroids = []
        self.l_aster = 0
        self.saucers = []
        self.l_saucer = 0
    def make_asteroids(self, surf):
        dims = surf.get_size()
        r_rx, r_ry = random.uniform(-1, 1), random.uniform(-1, 1)
        if r_rx**2 + r_ry**2 == 0:
            r_rx += 0.12
        r_rx, r_ry = r_rx / math.sqrt(r_rx**2 + r_ry**2) , r_ry / math.sqrt(r_rx**2 + r_ry**2)
        v_rx, v_ry = random.uniform(-1, 1), random.uniform(-1, 1)
        if v_rx**2 + v_ry**2 == 0:
            v_rx += 0.12
        v_rx, v_ry = v_rx / math.sqrt(v_rx**2 + v_ry**2) , v_ry / math.sqrt(v_rx**2 + v_ry**2)
        self.asteroids.append(Asteroid(dims[0]/2 + dims[0]*r_rx/math.sqrt(2), dims[1] / 2 + dims[1]*r_ry/math.sqrt(2), v_rx, v_ry))
        self.l_aster += 1
    def delete_asteroid(self):
        return
    def make_saucers(self):
        return
    def delete_saucer(self):
        return

    def draw(self, surf):
        for asteroid in self.asteroids:
            pygame.draw.rect(surf, pygame.color.THECOLORS['green'], (asteroid.x, asteroid.y, asteroid.width, asteroid.height))
        pygame.display.update()
    def update(self, surf):
        self.make_asteroids(surf)
        for i in range (self.l_aster):
            self.asteroids[i].update()
        for i in range (self.l_saucer):
            self.saucers[i].update()
        self.draw(surf)

class Player:
    def __init__(self, x, y, width = 25, height = 25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.bullets = []
        self.l_bullets = 0
    def update_pos(self, keys_pressed):
        if keys_pressed[pygame.K_a]:
            self.x -= self.vel
        if keys_pressed[pygame.K_d]:
            self.x += self.vel
        if keys_pressed[pygame.K_s]:
            self.y += self.vel
        if keys_pressed[pygame.K_w]:
            self.y -= self.vel
    def shoot(self, keys_pressed):
        v_x = 0
        v_y = 0
        if keys_pressed[pygame.K_UP]:
            v_y -= 1
        if keys_pressed[pygame.K_DOWN]:
            v_y += 1
        if keys_pressed[pygame.K_LEFT]:
            v_x -= 1
        if keys_pressed[pygame.K_RIGHT]:
            v_x += 1
        if v_x != 0 or v_y != 0:
            self.bullets.append(Projectile(self.x, self.y, v_x, v_y))
            self.l_bullets += 1
    def update_bullets(self):
        for i in range (self.l_bullets):
            self.bullets[i].update()
    def draw(self, surf):
        pygame.draw.rect(surf, pygame.color.THECOLORS['red'], (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            pygame.draw.rect(surf, pygame.color.THECOLORS['orange'], (bullet.x, bullet.y, bullet.width, bullet.height))
        pygame.display.update()
    def update(self, surf, keys_pressed):
        self.shoot(keys_pressed)
        self.update_bullets()
        self.update_pos(keys_pressed)
        self.draw(surf)



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    player = Player(10,10)
    nature = Nature()

    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        player.update(screen, keys)
        nature.update(screen)