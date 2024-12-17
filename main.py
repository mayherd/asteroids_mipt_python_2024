import pygame, sys, math, random
import numpy as np
from pygame import SurfaceType


class RectangularObject:
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def collided (t1: RectangularObject, t2: RectangularObject):
    if t2.x <= t1.x <= t2.x + t2.width and t2.y <= t1.y <= t2.y + t2.height:
        return True
    if t2.x <= t1.x + t1.width <= t2.x + t2.width and t2.y <= t1.y <= t2.y + t2.height:
        return True
    if t2.x <= t1.x <= t2.x + t2.width and t2.y <= t1.y + t1.height <= t2.y + t2.height:
        return True
    if t2.x <= t1.x + t1.width <= t2.x + t2.width and t2.y <= t1.y  + t1.height <= t2.y + t2.height:
        return True
    return False

class MovingObject(RectangularObject):
    def __init__(self, x: float, y: float, v_x: float, v_y: float, width: int, height: int, speed : float):
        RectangularObject.__init__(self, x, y, width, height)
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
        MovingObject.__init__(self, x, y, v_x, v_y, 3, 3, speed = 10)



class Asteroid(MovingObject):
    def __init__(self, x: float, y: float, v_x: float, v_y: float, sprite_size: str, sprite_num: int, width: int = 60, height: int = 60, speed: int = 5):
        MovingObject.__init__(self, x, y, v_x, v_y, width, height, speed)
        self.sprite_size = sprite_size
        self.sprite_num = sprite_num
        self.angle_number = 0
        self.frames = 3
    #determines if asteroid will enter the surf
    def check_coll_with_surf(self, surf: SurfaceType):
        dims = surf.get_size()
        if -100 < self.x < dims[0] + 100 and -100 < self.y < dims[1] + 100:
            return True
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
            if 0 <= sol[0] <= 1 and sol[1] >= 0:
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
        self.points = 0
        self.bullet_sprite = pygame.image.load("misc/bullet.png")
        self.las = [pygame.image.load("misc/large1.png"), pygame.image.load("misc/large2.png"), pygame.image.load("misc/large3.png")]
        self.mas = [pygame.image.load("misc/medium1.png"), pygame.image.load("misc/medium2.png"),
                                       pygame.image.load("misc/medium3.png")]
        self.large_asteroid_sprites = [[pygame.transform.rotate(self.las[i], j * 2) for j in range (180)] for i in range (3)]
        self.medium_asteroid_sprites = [[pygame.transform.rotate(self.mas[i], j * 2) for j in range (180)] for i in range (3)]
        self.asteroid_delay = 150.0
    def make_asteroid(self, surf: SurfaceType):
        if pygame.time.get_ticks() - self.timer < self.asteroid_delay:
            return
        self.asteroid_delay -= 0.2
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
        self.asteroids.append(Asteroid(dims[0]/2 + dims[0]*r_rx/math.sqrt(2), dims[1] / 2 + dims[1]*r_ry/math.sqrt(2), v_rx, v_ry, "large", random.choice([0, 1, 2])))
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
        asteroids_destroyed = set()
        for i in range (self.l_bullets):
            for j in range (self.l_aster):
                if collided(self.bullets[i], self.asteroids[j]):
                    bullets_destroyed.append(self.bullets[i])
                    asteroids_destroyed.add(self.asteroids[j])
                    self.points += 1
                    break
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
            self.asteroids.append(Asteroid(p_x - 10, p_y - 10, v_rx, v_ry, "medium", random.choice([0, 1, 2]), width = 25, height = 25))
            v_rx, v_ry = random.uniform(-1, 1), random.uniform(-1, 1)
            if v_rx == 0 or v_ry == 0:
                v_rx += 0.12
                v_ry += 0.12
            v_rx, v_ry = v_rx / math.sqrt(v_rx ** 2 + v_ry ** 2), v_ry / math.sqrt(v_rx ** 2 + v_ry ** 2)
            self.asteroids.append(Asteroid(p_x + 10, p_y + 10,  v_rx, v_ry, "medium", random.choice([0, 1, 2]), width=25, height=25))
            self.l_aster += 2

    def make_saucers(self):
        return
    def delete_saucer(self):
        return

    def draw(self, surf: SurfaceType):
        #change to normal scoreboard later
        myfont = pygame.font.SysFont("Times New Roman", 18)
        score = myfont.render(str(self.points), 1, pygame.color.THECOLORS["white"])
        surf.blit(score, (10, 480))

        for asteroid in self.asteroids:
            #pygame.draw.rect(surf, pygame.color.THECOLORS['green'], (asteroid.x, asteroid.y, asteroid.width, asteroid.height))
            if asteroid.frames == 0:
                asteroid.angle_number = (asteroid.angle_number + 1) % 180
                asteroid.frames = 3
            if asteroid.sprite_size == "large":
                spr = self.large_asteroid_sprites[asteroid.sprite_num][asteroid.angle_number]
            if asteroid.sprite_size == "medium":
                spr = self.medium_asteroid_sprites[asteroid.sprite_num][asteroid.angle_number]
            surf.blit(spr, (asteroid.x + asteroid.width // 2 - spr.get_width() // 2, asteroid.y + asteroid.height // 2 - spr.get_height() // 2))
            asteroid.frames -= 1
        for bullet in self.bullets:
            #pygame.draw.rect(surf, pygame.color.THECOLORS['orange'], (bullet.x, bullet.y, bullet.width, bullet.height))
            surf.blit(self.bullet_sprite, (bullet.x + bullet.width // 2 - self.bullet_sprite.get_width() // 2, bullet.y + bullet.height // 2 - self.bullet_sprite.get_height() // 2))

    def update(self, surf: SurfaceType):
        self.make_asteroid(surf)
        for i in range (self.l_aster):
            self.asteroids[i].update()
        for i in range (self.l_saucer):
            self.saucers[i].update()
        deleted_bullets = []
        for i in range(self.l_bullets):
            self.bullets[i].update()
            dims = surf.get_size()
            if (self.bullets[i].x > dims[0] + 100 or self.bullets[i].x < -100) and (self.bullets[i].y > dims[1] + 100 or self.bullets[i].y < -100):
                deleted_bullets.append(self.bullets[i])
        for bullet in deleted_bullets:
            self.bullets.pop(self.bullets.index(bullet))
            self.l_bullets -= 1
        self.delete_asteroids_outside(surf)
        self.destroy_asteroids()

class Player(RectangularObject):
    def __init__(self, x: float, y: float, now: int, width: int = 20, height: int = 20):
        RectangularObject.__init__(self, x, y, width, height)
        self.vel = 5
        self.timer = now
        self.inv_frames = 0
        self.sprite = pygame.image.load("misc/ship.png")
        self.angle = 0
        self.lives = 3

    def update_pos(self, keys_pressed, surf: SurfaceType):
        dims = surf.get_size()
        if keys_pressed[pygame.K_a]:
            if self.x > 10:
                self.x -= self.vel
        if keys_pressed[pygame.K_d]:
            if self.x < dims[0] - 10 - self.width:
                self.x += self.vel
        if keys_pressed[pygame.K_s]:
            if self.y < dims[1] - 10 - self.height:
                self.y += self.vel
        if keys_pressed[pygame.K_w]:
            if self.y > 10:
                self.y -= self.vel

    def check_collision(self, rects: list[RectangularObject]):
        for rect in rects:
            if collided(self, rect) and self.inv_frames == 0:
                self.inv_frames = 110
                self.lives -= 1




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
            nature.bullets.append(Projectile(self.x + self.width / 2, self.y + self.height / 2, v_x, v_y))
            nature.l_bullets += 1
            if v_x == -1 :
                self.angle = 180 + v_y * 45
            if v_x == 0:
                self.angle = -1 * v_y * 90
            if v_x == 1:
                self.angle = -1 * v_y * 45
            self.timer = pygame.time.get_ticks()


    def draw(self, surf: SurfaceType):
        if (self.inv_frames // 10) % 2 == 0:
            #pygame.draw.rect(surf, pygame.color.THECOLORS['red'], (self.x, self.y, self.width, self.height))
            new_sprite = pygame.transform.rotate(self.sprite, self.angle)
            surf.blit(new_sprite, (self.x + self.width // 2 - new_sprite.get_width() // 2, self.y + self.height // 2 - new_sprite.get_height() // 2))
            if self.inv_frames > 0:
                self.inv_frames -= 1
        else:
            self.inv_frames -= 1
    def update(self, keys_pressed, nature: Nature, surf: SurfaceType):
        self.shoot(keys_pressed, nature)
        self.update_pos(keys_pressed, surf)
        self.check_collision(nature.asteroids)


def redraw_game_window(surf, player: Player, nature: Nature):
    surf.fill((0,0,0))
    nature.draw(surf)
    player.draw(surf)
    pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    player = Player(400,400, pygame.time.get_ticks())
    nature = Nature(pygame.time.get_ticks())

    while True:
        clock.tick(36)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if player.lives > 0:
            keys = pygame.key.get_pressed()
            player.update(keys, nature, screen)
            nature.update(screen)
            redraw_game_window(screen, player, nature)
        else:
            screen.blit(pygame.image.load("misc/end_screen.png"), (0, 0))
            pygame.display.update()