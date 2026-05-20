import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (255,80,80)
GREEN = (80,255,80)
BLUE = (80,80,255)
BLACK = (20,20,20)

GRAVITY = 0.5

# Camera
camera_x = 0
camera_y = 0

# Player
class Player:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.w = 30
        self.h = 40
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.tool = "grapple"

    def update(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:
            self.vel_x = -5
        elif keys[pygame.K_d]:
            self.vel_x = 5
        else:
            self.vel_x *= 0.8

        # Jump
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = -10

        # Gravity
        self.vel_y += GRAVITY

        # Apply movement
        self.x += self.vel_x
        self.y += self.vel_y

        # Ground collision
        if self.y + self.h > 500:
            self.y = 500 - self.h
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self):
        pygame.draw.rect(screen, WHITE,
            (self.x - camera_x, self.y - camera_y, self.w, self.h))

player = Player()

# Enemy
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 30
        self.h = 30
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, RED,
                (self.x - camera_x, self.y - camera_y, self.w, self.h))

enemies = [Enemy(random.randint(400,1200), 470) for _ in range(5)]

# Bullet
bullets = []

# Bomb
bombs = []

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 60
        self.radius = 100

    def update(self):
        self.timer -= 1
        return self.timer <= 0

    def explode(self):
        # Physics blast
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dist < self.radius:
            force = (self.radius - dist) / self.radius
            angle = math.atan2(dy, dx)
            player.vel_x += math.cos(angle) * force * 15
            player.vel_y += math.sin(angle) * force * 15

    def draw(self):
        pygame.draw.circle(screen, BLUE,
            (int(self.x - camera_x), int(self.y - camera_y)), 6)

# Grapple
grapple_point = None

# Main loop
running = True
while running:
    screen.fill(BLACK)

    mouse = pygame.mouse.get_pos()
    world_mouse = (mouse[0] + camera_x, mouse[1] + camera_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.tool = "gun"
            if event.key == pygame.K_2:
                player.tool = "bomb"
            if event.key == pygame.K_3:
                player.tool = "grapple"

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = world_mouse

            if player.tool == "gun":
                dx = mx - player.x
                dy = my - player.y
                angle = math.atan2(dy, dx)
                bullets.append([player.x, player.y, angle])

                # recoil jump if shooting downward
                if dy > 0:
                    player.vel_y -= 5

            elif player.tool == "bomb":
                bombs.append(Bomb(player.x, player.y))

            elif player.tool == "grapple":
                grapple_point = (mx, my)

    # Update player
    player.update()

    # Grapple physics
    if grapple_point:
        gx, gy = grapple_point
        dx = gx - player.x
        dy = gy - player.y
        dist = math.hypot(dx, dy)

        if dist > 10:
            player.vel_x += dx * 0.01
            player.vel_y += dy * 0.01

        pygame.draw.line(screen, GREEN,
            (player.x - camera_x, player.y - camera_y),
            (gx - camera_x, gy - camera_y), 2)

    # Bullets
    for b in bullets[:]:
        b[0] += math.cos(b[2]) * 10
        b[1] += math.sin(b[2]) * 10

        for e in enemies:
            if e.alive and pygame.Rect(e.x,e.y,e.w,e.h).collidepoint(b[0], b[1]):
                e.alive = False
                bullets.remove(b)
                break

        pygame.draw.circle(screen, WHITE,
            (int(b[0] - camera_x), int(b[1] - camera_y)), 3)

    # Bombs
    for bomb in bombs[:]:
        if bomb.update():
            bomb.explode()
            bombs.remove(bomb)
        bomb.draw()

    # Camera follow
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    # Draw ground
    pygame.draw.rect(screen, GREEN,
        (0 - camera_x, 500 - camera_y, 2000, 100))

    # Draw enemies
    for e in enemies:
        e.draw()

    # Draw player
    player.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
