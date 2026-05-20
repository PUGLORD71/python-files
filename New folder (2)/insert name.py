import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# -----------------------------------------------
# Basic Data
# -----------------------------------------------
player_pos = pygame.Vector2(400, 300)
player_speed = 3

npc_pos = pygame.Vector2(200, 200)
enemy_pos = pygame.Vector2(600, 300)

enemy_alive = True
show_text = False
sword_swing = False
sword_angle = 0
sword_cooldown = 0

FONT = pygame.font.SysFont("consolas", 24)

# -----------------------------------------------
# Helper: Distance
# -----------------------------------------------
def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

# -----------------------------------------------
# Dialogue Box
# -----------------------------------------------
def draw_text_box(text):
    box = pygame.Rect(100, HEIGHT - 150, WIDTH - 200, 100)
    pygame.draw.rect(screen, (0, 0, 0), box)
    pygame.draw.rect(screen, (255, 255, 255), box, 3)

    rendered = FONT.render(text, True, (255, 255, 255))
    screen.blit(rendered, (box.x + 20, box.y + 35))

# -----------------------------------------------
# Sword Collision (simple arc check)
# -----------------------------------------------
def sword_hits_enemy():
    if not enemy_alive:
        return False

    reach = 60  
    ang = math.radians(sword_angle)
    sx = player_pos.x + math.cos(ang) * reach
    sy = player_pos.y + math.sin(ang) * reach

    return dist(pygame.Vector2(sx, sy), enemy_pos) < 30

# -----------------------------------------------
# Main Loop
# -----------------------------------------------
while True:
    dt = clock.tick(60)
    screen.fill((40, 50, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Interact with NPC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if dist(player_pos, npc_pos) < 60:
                    show_text = not show_text

            # Sword attack
            if event.key == pygame.K_SPACE and sword_cooldown == 0:
                sword_swing = True
                sword_angle = 0
                sword_cooldown = 15

    # ------------------------
    # Movement
    # ------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos.y -= player_speed
    if keys[pygame.K_s]: player_pos.y += player_speed
    if keys[pygame.K_a]: player_pos.x -= player_speed
    if keys[pygame.K_d]: player_pos.x += player_speed

    # ------------------------
    # Sword Swing Animation
    # ------------------------
    if sword_swing:
        sword_angle += 20
        if sword_angle >= 120:
            sword_swing = False

        if sword_hits_enemy():
            enemy_alive = False

    if sword_cooldown > 0:
        sword_cooldown -= 1

    # ------------------------
    # Draw NPC
    # ------------------------
    pygame.draw.circle(screen, (200, 200, 50), npc_pos, 25)

    # ------------------------
    # Draw Enemy
    # ------------------------
    if enemy_alive:
        pygame.draw.circle(screen, (200, 50, 50), enemy_pos, 30)

    # ------------------------
    # Draw Player
    # ------------------------
    pygame.draw.circle(screen, (50, 200, 255), player_pos, 25)

    # Draw sword
    if sword_swing:
        ang = math.radians(sword_angle)
        sx = player_pos.x + math.cos(ang) * 50
        sy = player_pos.y + math.sin(ang) * 50
        pygame.draw.line(screen, (255,255,255), player_pos, (sx, sy), 5)

    # ------------------------
    # Dialogue Text
    # ------------------------
    if show_text:
        draw_text_box("Hello traveler! Press E to close.")

    pygame.display.update()
