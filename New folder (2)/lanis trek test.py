import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

GRAVITY = 0.5
FRICTION = 0.85
GRAPPLE_SPEED = 25
PULL_SPEED = 15

# ------------------------
# Player
# ------------------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 0.8
        self.jump_power = -12
        self.on_ground = False
        self.facing = 1

        # Grapple states
        self.state = "normal"  # normal, shooting, pulling
        self.grapple_pos = None
        self.grapple_dir = None
        self.grapple_target_block = None

    def handle_input(self):
        if self.state != "normal":
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.vel.x -= self.speed
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.vel.x += self.speed
            self.facing = 1

    def jump(self):
        if self.state == "normal":
            self.vel.y = self.jump_power

    def apply_physics(self):
        if self.state == "normal":
            self.vel.y += GRAVITY
            self.vel.x *= FRICTION

            self.rect.x += self.vel.x
            collide(self, boxes, "x")

            self.rect.y += self.vel.y
            collide(self, boxes, "y")

        elif self.state == "pulling":
            # Pull directly toward grapple point
            direction = pygame.Vector2(
                self.grapple_pos.x - self.rect.centerx,
                self.grapple_pos.y - self.rect.centery
            )

            if direction.length() > 5:
                direction = direction.normalize()
                self.rect.center += direction * PULL_SPEED
            else:
                self.state = "normal"

    def update_grapple(self):
        if self.state == "shooting":
            self.grapple_pos += self.grapple_dir * GRAPPLE_SPEED

            point_rect = pygame.Rect(
                self.grapple_pos.x, self.grapple_pos.y, 4, 4
            )

            hit = False
            for box in boxes:
                if box.colliderect(point_rect):
                    self.state = "pulling"
                    self.grapple_target_block = box
                    hit = True
                    break

            # If off screen and no hit → return
            if not hit and not screen.get_rect().collidepoint(self.grapple_pos):
                self.state = "normal"

        elif self.state == "pulling":
            # If player touches hooked block → cancel
            if self.rect.colliderect(self.grapple_target_block):
                self.vel.y = -10
                self.state = "normal"

    def draw(self):
        pygame.draw.rect(screen, (50, 200, 255), self.rect)

        if self.state in ["shooting", "pulling"]:
            pygame.draw.line(
                screen,
                (255,255,255),
                self.rect.center,
                self.grapple_pos,
                2
            )


# ------------------------
# Collision
# ------------------------
def collide(player, boxes, direction):
    player.on_ground = False
    for box in boxes:
        if player.rect.colliderect(box):
            if direction == "x":
                if player.vel.x > 0:
                    player.rect.right = box.left
                if player.vel.x < 0:
                    player.rect.left = box.right
                player.vel.x = 0

            if direction == "y":
                if player.vel.y > 0:
                    player.rect.bottom = box.top
                    player.on_ground = True
                if player.vel.y < 0:
                    player.rect.top = box.bottom
                player.vel.y = 0


# ------------------------
# Level
# ------------------------
player = Player(200, 300)

boxes = [
    pygame.Rect(0, 550, 1000, 50),
    pygame.Rect(300, 450, 200, 30),
    pygame.Rect(650, 350, 200, 30),
    pygame.Rect(500, 250, 150, 30)
]

# ------------------------
# Main Loop
# ------------------------
running = True
while running:
    clock.tick(60)
    screen.fill((20, 20, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.jump()
            if event.key == pygame.K_x:
                if player.state == "normal":
                    player.state = "shooting"
                    player.grapple_pos = pygame.Vector2(player.rect.center)
                    player.grapple_dir = pygame.Vector2(player.facing, 0)

    player.handle_input()
    player.apply_physics()
    player.update_grapple()

    for box in boxes:
        pygame.draw.rect(screen, (200, 200, 200), box)

    player.draw()

    pygame.display.flip()

pygame.quit()
