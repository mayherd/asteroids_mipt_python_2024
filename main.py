import pygame, sys, math, random
import numpy as np
from pygame import SurfaceType


class MovingObject:
    def __init__(self, x: float, y: float, v_x: float, v_y: float, speed : float):
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
    def __init__(self, x: float, y: float, v_x: float, v_y: float):
        MovingObject.__init__(self, x, y, v_x, v_y, speed = 10)
        self.width = 7
        self.height = 7


class Asteroid(MovingObject):
    def __init__(self, x: float, y: float, v_x: float, v_y: float, width: int = 40, height: int = 40, speed: int = 5):
        MovingObject.__init__(self, x, y, v_x, v_y, speed)
        self.width = width
        self.height = height
    #determines if asteroid will enter the surf
    def check_coll_with_surf(self, surf: SurfaceType):
        dims = surf.get_size()
        sols = []
        a13 = np.array([[dims[0], -1 * self.v_x], [0, -1 * self.v_y]])
        b12 = np.array([self.x, self.y])
        sols.append(np.linalg.solve(a13, b12))
        a24 = np.array([[0, -1 * self.v_x], [dims[1], -1 * self.v_y]])
        sols.append(np.linalg.solve(a24, b12))
        b3 = np.array([self.x, self.y - dims[1]])
        sols.append(np.linalg.solve(a13, b3))
        b4 = np.array([self.x - dims[0], self.y])
        sols.append(np.linalg.solve(a24, b4))
        for sol in sols:
            if sol[0] < 0 or sol[0] > 1 or sol[1] < 0:
                return True
        return False

class Nature:
    def __init__(self, now: int):
        self.asteroids = []
        self.l_aster = 0
        self.saucers = []
        self.l_saucer = 0
        self.timer = now
        self.bullets = []
        self.l_bullets = 0
    def make_asteroid(self, surf: SurfaceType):
        if pygame.time.get_ticks() - self.timer < 150:
            return
        dims = surf.get_size()
        r_rx, r_ry = random.uniform(-1, 1), random.uniform(-1, 1)
        if r_rx**2 + r_ry**2 == 0:
            r_rx += 0.12
        r_rx, r_ry = r_rx / math.sqrt(r_rx**2 + r_ry**2) , r_ry / math.sqrt(r_rx**2 + r_ry**2)
        v_rx, v_ry = random.uniform(-1, 1), random.uniform(-1, 1)
        if v_rx == 0 or v_ry == 0:
            v_rx += 0.12
            v_ry += 0.12
        v_rx, v_ry = v_rx / math.sqrt(v_rx**2 + v_ry**2) , v_ry / math.sqrt(v_rx**2 + v_ry**2)
        #generate asteroid with (almost) random velocity a bit outside the surf (doesn't quite work, I see them spawning sometimes)
        self.asteroids.append(Asteroid(dims[0]/2 + dims[0]*r_rx/math.sqrt(2), dims[1] / 2 + dims[1]*r_ry/math.sqrt(2), v_rx, v_ry))
        self.l_aster += 1
        self.timer = pygame.time.get_ticks()
    #delete asteroids that won't enter the surf
    def delete_asteroids_outside(self, surf: SurfaceType):
        new = []
        for i in range (self.l_aster):
            if  self.asteroids[i].check_coll_with_surf(surf):
                new.append(self.asteroids[i])
        self.asteroids = new
        self.l_aster = len(new)
    #destroy asteroids and bullets that collided with each other
    def destroy_asteroids(self):
        bullets_destroyed = []
        asteroids_destroyed =[]
        for i in range (self.l_bullets):
            for j in range (self.l_aster):
                if self.asteroids[j].x <= self.bullets[i].x <= self.asteroids[j].x + self.asteroids[j].width and self.asteroids[j].y <= self.bullets[i].y <= self.asteroids[j].y + self.asteroids[j].height:
                    bullets_destroyed.append(self.bullets[i])
                    asteroids_destroyed.append(self.asteroids[j])
        for bullet in bullets_destroyed:
            self.bullets.pop(self.bullets.index(bullet))
            self.l_bullets -= 1
        for asteroid in asteroids_destroyed:
            p_x, p_y = asteroid.x, asteroid.y
            self.asteroids.pop(self.asteroids.index(asteroid))
            self.l_aster -= 1
            if asteroid.width < 40 and asteroid.height < 40:
                continue
            v_rx, v_ry = random.uniform(-1, 1), random.uniform(-1, 1)
            if v_rx == 0 or v_ry == 0:
                v_rx += 0.12
                v_ry += 0.12
            v_rx, v_ry = v_rx / math.sqrt(v_rx ** 2 + v_ry ** 2), v_ry / math.sqrt(v_rx ** 2 + v_ry ** 2)
            self.asteroids.append(Asteroid(p_x - 10, p_y - 10, v_rx, v_ry, width = 15, height = 15))
            v_rx, v_ry = random.uniform(-1, 1), random.uniform(-1, 1)
            if v_rx == 0 or v_ry == 0:
                v_rx += 0.12
                v_ry += 0.12
            v_rx, v_ry = v_rx / math.sqrt(v_rx ** 2 + v_ry ** 2), v_ry / math.sqrt(v_rx ** 2 + v_ry ** 2)
            self.asteroids.append(Asteroid(p_x + 10, p_y + 10,  v_rx, v_ry, width=15, height=15))
            self.l_aster += 2

    def make_saucers(self):
        return
    def delete_saucer(self):
        return

    def draw(self, surf: SurfaceType):
        for asteroid in self.asteroids:
            pygame.draw.rect(surf, pygame.color.THECOLORS['green'], (asteroid.x, asteroid.y, asteroid.width, asteroid.height))
        for bullet in self.bullets:
            pygame.draw.rect(surf, pygame.color.THECOLORS['orange'], (bullet.x, bullet.y, bullet.width, bullet.height))
    def update(self, surf: SurfaceType):
        self.make_asteroid(surf)
        for i in range (self.l_aster):
            self.asteroids[i].update()
        for i in range (self.l_saucer):
            self.saucers[i].update()
        for i in range(self.l_bullets):
            self.bullets[i].update()
        self.delete_asteroids_outside(surf)
        self.destroy_asteroids()

class Player:
    def __init__(self, x: float, y: float, now: int, width: int = 25, height: int = 25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

        self.timer = now
    def update_pos(self, keys_pressed):
        if keys_pressed[pygame.K_a]:
            self.x -= self.vel
        if keys_pressed[pygame.K_d]:
            self.x += self.vel
        if keys_pressed[pygame.K_s]:
            self.y += self.vel
        if keys_pressed[pygame.K_w]:
            self.y -= self.vel
    def shoot(self, keys_pressed, nature: Nature):
        if pygame.time.get_ticks() - self.timer < 200:
            return
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
            nature.bullets.append(Projectile(self.x, self.y, v_x, v_y))
            nature.l_bullets += 1
            self.timer = pygame.time.get_ticks()
    def draw(self, surf: SurfaceType):
        pygame.draw.rect(surf, pygame.color.THECOLORS['red'], (self.x, self.y, self.width, self.height))
    def update(self, keys_pressed, nature: Nature):
        self.shoot(keys_pressed, nature)
        self.update_pos(keys_pressed)


def redraw_game_window(surf, player: Player, nature: Nature):
    surf.fill((0,0,0))
    player.draw(surf)
    nature.draw(surf)
    pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    player = Player(250,250, pygame.time.get_ticks())
    nature = Nature(pygame.time.get_ticks())

    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        player.update(keys, nature)
        nature.update(screen)
        redraw_game_window(screen, player, nature)