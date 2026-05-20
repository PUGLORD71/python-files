import pygame
import math
import sys

# -------------------
# Settings
# -------------------
WIDTH, HEIGHT = 800, 600
FPS = 70
FOV = math.pi / 3  # 60 degrees
RUN_FOV = math.pi / 5  # 60 degrees
CUR_FOV = FOV
NUM_RAYS = WIDTH
MAX_DEPTH = 2000
SCALE = 1
TILE = 100
TINY_TILE = TILE // 2
brightness = 250
WALL_LENGTH = 200
walk_speed = 7
run_speed = 11
player_speed = walk_speed  # start walking
end_text = "PAUSED  (press M to resume)"
# Wall shading settings
shade_mode = [True,True,True]  # options: 'gray', 'red', 'green', 'blue'
shade = 0
# Colors
BLACK = (0, 0, 0)
FLOOR_COLOR = (60, 60, 60)
SKY_COLOR = (220, 220, 220)

# Jump / Vertical
player_z = 0
z_velocity = 0
gravity = 1
jump_strength = -10
ground_level = 0

# Mouse look / Menu
mouse_sensitivity = 0.006
vertical_sensitivity = 1.0
player_look = 0
max_look_up = HEIGHT//1.5
max_look_down = -HEIGHT//1.5
menu_open = False
settings_open = False

# -------------------
# Maze layout (1 = wall, 0 = empty)
# -------------------
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,1,1,1],
    [1,0,1,1,1,1,0,0,0,1,1,0,1,1,1],
    [1,0,0,0,1,1,1,1,1,1,1,0,1,1,1],
    [1,0,1,0,1,1,1,1,1,0,0,0,1,1,1],
    [1,0,1,0,1,1,1,0,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Goal tile (walkable)
goal_tile = (-1,-1)  # (row, col) 6,6
#maze[goal_tile[0]][goal_tile[1]] = 0  # ensure walkable

# -------------------
# Player
# -------------------
player_x = TILE + TILE // 2
player_y = TILE + TILE // 2
player_angle = 0
player_speed = 3
rotation_speed = 0.04

# -------------------
# Pygame init
# -------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycast Maze with Goal")
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.get_rel()  # reset relative movement

# -------------------
# Raycasting
# -------------------
def raycast():
    start_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * (FOV / NUM_RAYS)
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        for depth in range(0, MAX_DEPTH, 5):
            x = player_x + depth * cos_a
            y = player_y + depth * sin_a

            i = int(x // TILE)
            j = int(y // TILE)

            max_cols = max(len(row) for row in maze)
            if i < 0 or i >= max_cols or j < 0 or j >= len(maze):
                break

            if maze[j][i] == 1 or (j, i) == goal_tile:
                


                depth_corrected = depth * math.cos(player_angle - angle)
                wall_height = 5000 / (depth_corrected + 0.0001)

                # Jump + mouse look
                jump_shift = -player_z * 5 / (0.1 + depth_corrected * 0.01)
                look_shift = int(player_look)
                camera_shift = jump_shift + look_shift

                line_top = HEIGHT//2 - wall_height//2 + camera_shift
                line_bottom = HEIGHT//2 + wall_height//2 + camera_shift

                top_extra = int(WALL_LENGTH / (0.1 + depth_corrected * 0.01))
                line_top -= top_extra

                # Color: green for goal, shaded gray for walls
                shade = brightness / (1 + depth_corrected * 0.01)
                shade = max(20, min(255, int(shade)))
                if (j, i) == goal_tile:
                    color = (0, shade, shade)
                else:
                    if shade_mode == [True,True,True]:
                        color = (shade, shade, shade)
                    if shade_mode == [False,True,False]:
                        color = (0, shade, 0)
                    if shade_mode == [True,False,False]:
                        color = (shade, 0, 0)
                    if shade_mode == [False,False,True]:
                        color = (0, 0, shade)
                    if shade_mode == [True,False,True]:
                        color = (shade, 0, shade)
                    if shade_mode == [False,True,True]:
                        color = (0, shade, shade)
                    if shade_mode == [True,True,False]:
                        color = (shade, shade, 0)
                    if shade_mode == [False,False,False]:
                        color = (0, 0, 0)
                    
                midpoint = (line_top + line_bottom) // 2
                
                #pygame.draw.line(screen, (shade,0,200),
                 #                (ray, 0),
                  #               (ray, HEIGHT), 2)


                pygame.draw.line(screen, color,
                                 (ray, line_top),
                                 (ray, line_bottom), 2)
                
                
                #pygame.draw.line(screen, (shade,0,0),
                 #                (ray, midpoint),
                  #               (ray, line_bottom), 2)
                break

# -------------------
# Minimap
# -------------------
def draw_minimap():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 20, 180))
    screen.blit(overlay, (0, 0))
    mini_scale = 0.4
    offx = 100
    offy = 50
    for j, row in enumerate(maze):
        for i, cell in enumerate(row):
            shade = 200
            if shade_mode == [True,True,True]:
                color = (shade, shade, shade)
            if shade_mode == [False,True,False]:
                color = (0, shade, 0)
            if shade_mode == [True,False,False]:
                color = (shade, 0, 0)
            if shade_mode == [False,False,True]:
                color = (0, 0, shade)
            if shade_mode == [True,False,True]:
                color = (shade, 0, shade)
            if shade_mode == [False,True,True]:
                 color = (0, shade, shade)
            if shade_mode == [True,True,False]:
                color = (shade, shade, 0)
            if shade_mode == [False,False,False]:
                color = (60, 60, 60)
            loc_color = color if cell == 1 else (0, 0, 0)
            pygame.draw.rect(screen, loc_color,
                             (i*TILE*mini_scale + offx, j*TILE*mini_scale + offy, TILE*mini_scale, TILE*mini_scale))

    # Draw goal
    #gi, gj = goal_tile[1], goal_tile[0]
    #pygame.draw.rect(screen, (0, 255, 0), 
     #                (gi*TILE*mini_scale, gj*TILE*mini_scale, TILE*mini_scale, TILE*mini_scale))

    # Player
    pygame.draw.circle(screen, loc_color,
                       (int(player_x*mini_scale + offx), int(player_y*mini_scale+offy)), 10)

# -------------------
# Floor & ceiling
# -------------------
def draw_surfaces():
    camera_shift = -int(player_z) + int(player_look)
    floor_rect = pygame.Rect(0, HEIGHT//2 + camera_shift, WIDTH, HEIGHT//2 - camera_shift)
    pygame.draw.rect(screen, FLOOR_COLOR, floor_rect)

# -------------------
# Menu
# -------------------
def draw_menu():
    pygame.draw.rect(screen, (0,0,0, 0.3), (0, HEIGHT // 4, WIDTH, HEIGHT // 2))
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("PAUSED  (press M to resume)", True, (255, 255, 255))
    screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))

def draw_pause_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 20, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont("Arial", 40)
    if settings_open:
        txt1 = font.render("SETTINGS", True, (255, 255, 255))
        txt2 = font.render(f"Shade Mode: {shade_mode} (Press 1-3)", True, (255, 255, 255))
        txt3 = font.render("Walk Speed: " + str(int(walk_speed)) + " (UP/DOWN)", True, (255, 255, 255))
        txt4 = font.render("Run Speed: " + str(int(run_speed)) + " (LEFT/RIGHT)", True, (255, 255, 255))
        txt5 = font.render(f"Brightness: {brightness} (I/K)", True, (255, 255, 255))
        
        screen.blit(txt1, (WIDTH//2 - txt1.get_width()//2, 100))
        screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 180))
        screen.blit(txt3, (WIDTH//2 - txt3.get_width()//2, 260))
        screen.blit(txt4, (WIDTH//2 - txt4.get_width()//2, 340))
        screen.blit(txt5, (WIDTH//2 - txt5.get_width()//2, 420))
        txt6 = font.render("Press M to go back", True, (255, 255, 255))
        screen.blit(txt6, (WIDTH//2 - txt5.get_width()//2, 500))
    else:
        txt = font.render("PAUSED (M to resume, S for settings)", True, (255, 255, 255))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
    pygame.display.flip()


# -------------------
# Collision
# -------------------
def can_move(x, y):
    i = int(x // TILE)
    j = int(y // TILE)
    if i < 0 or i >= len(maze[0]) or j < 0 or j >= len(maze):
        return False
    return maze[j][i] == 0

# -------------------
# Main loop
# -------------------
running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    pygame.mouse.get_rel()  # reset relative movement at start of frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                menu_open = not menu_open
                if menu_open:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                else:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mouse.get_rel()
            if menu_open and event.key == pygame.K_s:
                settings_open = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if settings_open:
                keys = pygame.key.get_pressed()
                # Change shading
                if keys[pygame.K_1]: shade_mode[0] = not shade_mode[0]
                if keys[pygame.K_2]: shade_mode[1] = not shade_mode[1]
                if keys[pygame.K_3]: shade_mode[2] = not shade_mode[2]

                # Adjust speeds
                if keys[pygame.K_UP]: walk_speed += 1
                if keys[pygame.K_DOWN]: walk_speed -= 1
                if keys[pygame.K_RIGHT]: run_speed += 1
                if keys[pygame.K_LEFT]: run_speed -= 1
                
                if keys[pygame.K_i]: brightness += 10
                if keys[pygame.K_k]: brightness -= 10


    if menu_open:
       draw_pause_menu()
       continue


    keys = pygame.key.get_pressed()
    if not menu_open:
        # ---------- MOUSE LOOK ----------
        mx, my = pygame.mouse.get_rel()
        player_angle += mx * mouse_sensitivity
        player_angle %= math.tau
        player_look += -my * vertical_sensitivity
        player_look = max(max_look_down, min(max_look_up, player_look))

        # ---------- MOVEMENT ----------
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dx += math.cos(player_angle) * player_speed
            dy += math.sin(player_angle) * player_speed
        if keys[pygame.K_s]:
            dx -= math.cos(player_angle) * player_speed
            dy -= math.sin(player_angle) * player_speed
        if keys[pygame.K_a]:
            dx -= math.cos(player_angle + math.pi/2) * player_speed
            dy -= math.sin(player_angle + math.pi/2) * player_speed
        if keys[pygame.K_d]:
            dx += math.cos(player_angle + math.pi/2) * player_speed
            dy += math.sin(player_angle + math.pi/2) * player_speed

        # Jump
        if keys[pygame.K_SPACE] and player_z == ground_level:
            z_velocity = jump_strength
        z_velocity += gravity
        player_z += z_velocity
        if player_z > ground_level:
            player_z = ground_level
            z_velocity = 0
        # Sprint
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            CUR_FOV = RUN_FOV
            player_speed = run_speed
        else:
            player_speed = walk_speed
            CUR_FOV = FOV
        # Collision
        if can_move(player_x + dx, player_y):
            player_x += dx
        if can_move(player_x, player_y + dy):
            player_y += dy

    # ---------- Check Win ----------
    player_tile_i = int(player_x // TILE)
    player_tile_j = int(player_y // TILE)
    if (player_tile_j, player_tile_i) == goal_tile:
        end_text = "You Win!"
        menu_open = True
    else:
        end_text = "PAUSED  (press M to resume)"

    # ---------- RENDER ----------

    #draw_surfaces()
    
    raycast()
    if keys[pygame.K_e]:
        draw_minimap()
    pygame.display.flip()

    
   
    
pygame.quit()
sys.exit()
