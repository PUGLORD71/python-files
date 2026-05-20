import pygame
import pygame.freetype
import math
import sys
import random

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
brightness = 650
WALL_LENGTH = 200
Wave = 1
walk_speed = 7
player_damage = 0.1
gameover = False
kills = 0
run_speed = 11
Center = False
player_speed = walk_speed  # start walking
end_text = "PAUSED  (press M to resume)"
# Wall shading settings
shade_mode = [True,True,True]  # options: 'gray', 'red', 'green', 'blue'
shade = 0
# enemys / health

enemies = [
{"x": 9.3 * TILE, "y": 2.8 * TILE, "speed": 0.025, "color":[False,True,False], "health":50},
{"x": 4.3 * TILE, "y": 4.8 * TILE, "speed": 0.03, "color":[False,False,True], "health":50}


]
color_list = [[False, False, False], [False, False, True], [False, True, False], [False, True, True], [True, False, False], [True, False, True], [True, True, False], [True, True, True]]
ENEMY_DAMAGE = 2
enemy_x = 9.3 * TILE     # any exact world coordinate
enemy_y = 2.8 * TILE
HEALTH = 400
CUR_ENEMY = None

# Colors
BLACK = (0, 0, 0)
FLOOR_COLOR = (60, 60, 60)
SKY_COLOR = (220, 220, 220)
color = 0
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
    [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
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
pygame.display.set_caption("FPS Game")
clock = pygame.time.Clock()
pygame.freetype.init()
FONT = pygame.freetype.Font("MedodicaRegular.otf", 32)   # 32 = font size



pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.get_rel()  # reset relative movement

# -------------------
# Raycasting
# -------------------
def raycast():
    Center = False
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

            cell = maze[j][i]

            # -----------------------------
            # New: ENEMY = small cube inside tile
            # -----------------------------
            # --- ENEMY BLOCK USING TRUE WORLD COORDS ---
            enemy_hit = False
            for enemy in enemies:
                # physical size of enemy cube
                ENEMY_SIZE = TILE * 0.35
                half_size = ENEMY_SIZE / 2

                # enemy bounding box in world-space
                min_x = enemy["x"] - half_size
                max_x = enemy["x"] + half_size
                min_y = enemy["y"] - half_size
                max_y = enemy["y"] + half_size

                # ray hit test: is the ray coordinate inside the box?
                if min_x <= x <= max_x and min_y <= y <= max_y:

                    depth_corrected = depth * math.cos(player_angle - angle)

                    # enemy height (projected like walls)
                    wall_height = 5000 / (depth_corrected + 0.0001)

                    # camera vertical adjustments
                    jump_shift = -player_z * 5 / (0.1 + depth_corrected * 0.01)
                    look_shift = int(player_look)
                    camera_shift = jump_shift + look_shift

                    # projected vertical line
                    line_top = HEIGHT//2 - wall_height//2 + camera_shift
                    line_bottom = HEIGHT//2 + wall_height//2 + camera_shift

                    # OPTIONAL: make cube appear shorter than walls
                    top_extra = int(WALL_LENGTH / (0.1 + depth_corrected * 0.01))
                    line_top -= top_extra 

                    # shading
                    shade = brightness / (1 + depth_corrected * 0.01)
                    shade = max(20, min(255, int(shade)))
                    if enemy["color"] == [True,True,True]:
                        color = (shade, shade, shade)
                    elif enemy["color"] == [False,True,False]:
                        color = (200, shade, 0)
                    elif enemy["color"] == [True,False,False]:
                        color = (shade, 200, 0)
                    elif enemy["color"] == [False,False,True]:
                        color = (200, 0, shade)
                    elif enemy["color"] == [True,False,True]:
                        color = (0, 200, shade)
                    elif enemy["color"] == [False,True,True]:
                        color = (0, shade, 200)
                    elif enemy["color"] == [True,True,False]:
                        color = (shade, 0, 200)
                    else:
                        color = (0, 0, 0)
                    #color = (shade, 0, 0)
                    
                    if ray == WIDTH//2:
                        Center = True
                    # draw cube slice
                    pygame.draw.line(screen, color,
                                     (ray, line_top),
                                     (ray, line_bottom), 2)

                    enemy_hit = True
                    # stop checking further depth
                    break

            if enemy_hit:
                break  # move to next ray
            if cell == 1 or (j, i) == goal_tile:
                


                depth_corrected = depth * math.cos(player_angle - angle)
                #wall_height = 5000 / (depth_corrected + 0.0001)
                if cell == 1:  # normal wall
                    wall_height = 5000 / (depth_corrected + 0.0001)

                

                # Jump + mouse look
                jump_shift = -player_z * 5 / (0.1 + depth_corrected * 0.01)
                look_shift = int(player_look)
                camera_shift = jump_shift + look_shift

                line_top = HEIGHT//2 - wall_height//2 + camera_shift
                line_bottom = HEIGHT//2 + wall_height//2 + camera_shift

                #top_extra = int(WALL_LENGTH / (0.1 + depth_corrected * 0.01))
                #line_top -= top_extra
                if cell == 1:
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
                        color = (shade, 200, 0)
                

                                        
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

    # ---------------------
    # Draw Maze
    # ---------------------
    for j, row in enumerate(maze):
        for i, cell in enumerate(row):
            shade = 200
            if shade_mode == [True,True,True]:
                color = (shade, shade, shade)
            elif shade_mode == [False,True,False]:
                color = (0, shade, 0)
            elif shade_mode == [True,False,False]:
                color = (shade, 0, 0)
            elif shade_mode == [False,False,True]:
                color = (0, 0, shade)
            elif shade_mode == [True,False,True]:
                color = (shade, 0, shade)
            elif shade_mode == [False,True,True]:
                color = (0, shade, shade)
            elif shade_mode == [True,True,False]:
                color = (shade, shade, 0)
            else:
                color = (60, 60, 60)

            loc_color = color if cell == 1 else (0, 0, 0)

            pygame.draw.rect(
                screen, loc_color,
                (i*TILE*mini_scale + offx, j*TILE*mini_scale + offy,
                 TILE*mini_scale, TILE*mini_scale)
            )

    # ---------------------
    # Draw Enemies
    # ---------------------
    enemy_color = (255, 0, 0)
    enemy_radius = 12

    for enemy in enemies:
        # SUPPORT BOTH dict OR object
        try:
            tile_x = enemy["x"] / TILE
            tile_y = enemy["y"] / TILE
        except:
            tile_x = enemy.x
            tile_y = enemy.y

        # convert TILE coords → world coords
        ex = tile_x * TILE + TILE / 2
        ey = tile_y * TILE + TILE / 2

        mini_x = int(ex * mini_scale + offx)
        mini_y = int(ey * mini_scale + offy)
        enemy_color = (235, 200,0)
        pygame.draw.circle(screen, enemy_color, (mini_x, mini_y), enemy_radius)

    # ---------------------
    # Draw Player  (fixed!)
    # ---------------------
    player_color = (0, 120, 255)

    mini_px = int(player_x * mini_scale + offx)
    mini_py = int(player_y * mini_scale + offy)

    pygame.draw.circle(screen, player_color, (mini_px, mini_py), 10)

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

    font = pygame.freetype.Font("MedodicaRegular.otf", 40)

    # SHORTCUT: draw text like this
    draw = font.render_to

    if settings_open:
        draw(screen, (60, 100), "SETTINGS", (255, 255, 255))
        draw(screen, (60, 180), f"Shade Mode: {shade_mode} (Press 1-3)", (255, 255, 255))
        draw(screen, (60, 260), "Walk Speed: " + str(int(walk_speed)) + " (UP/DOWN)", (255, 255, 255))
        draw(screen, (60, 340), "Run Speed: " + str(int(run_speed)) + " (LEFT/RIGHT)", (255, 255, 255))
        draw(screen, (60, 420), f"Brightness: {brightness} (I/K)", (255, 255, 255))
        draw(screen, (60, 500), "Press M to go back", (255, 255, 255))

    else:
        draw(screen, (60, HEIGHT//2 - 40),
             "PAUSED (M to resume, S for settings)",
             (255, 255, 255))

    pygame.display.flip()



# -------------------
# Collision
# -------------------
def can_move(x, y):
    i = int(x // TILE)
    j = int(y // TILE)
    if i < 0 or i >= len(maze[0]) or j < 0 or j >= len(maze):
        return False
    return maze[j][i] in (0, 2)

#-------
#  UI
#-------

def UI():
    global HEALTH
    pygame.draw.rect(screen, (145, 0, 0), (30, HEIGHT - 70, 400, 40))
    
    if HEALTH > 0:
        pygame.draw.rect(screen, (0, 255, 0), (30, HEIGHT - 70, HEALTH, 40))
    else:
        #future gameover goes here
        pygame.quit()
        sys.exit()

    pygame.draw.rect(screen, (0, 0, 0), (30, HEIGHT - 70, 400, 40), 5)
    pygame.draw.line(screen, (125,125,125), (WIDTH // 2, HEIGHT // 2 + 30), (WIDTH // 2, HEIGHT // 2 + 20), 4)
    pygame.draw.line(screen, (125,125,125), (WIDTH // 2, HEIGHT // 2 - 30), (WIDTH // 2, HEIGHT // 2 - 20), 4)
    pygame.draw.line(screen, (125,125,125), (WIDTH // 2 + 30, HEIGHT // 2), (WIDTH // 2 + 20, HEIGHT // 2), 4)
    pygame.draw.line(screen, (125,125,125), (WIDTH // 2 - 30, HEIGHT // 2), (WIDTH // 2 - 20, HEIGHT // 2), 4)
    pygame.draw.circle(screen, (125,125,125), (WIDTH //2, HEIGHT //2), 2)
    FONT.render_to(screen, (60, HEIGHT - 60), f"{int(HEALTH // 4)} / 100", (0, 0, 0))
    pygame.draw.rect(screen, (75, 0, 0), (30, HEIGHT - 110, 400, 40))
    pygame.draw.rect(screen, (0, 0, 0), (30, HEIGHT - 110, 400, 40), 5)
    
    FONT.render_to(screen, (60, HEIGHT - 100), f"Kills : {kills}      Wave : {Wave}", (255, 0, 0))
    
    if player_touching_enemy(player_x, player_y, enemies):
        HEALTH -= ENEMY_DAMAGE 
    
#------------------
# Enemy Collision
#------------------
def player_touching_enemy(player_x, player_y, enemies):
    
    ENEMY_SIZE = TILE * 0.35
    half = ENEMY_SIZE / 2

    for enemy in enemies:
        if (enemy["x"] - half <= player_x <= enemy["x"] + half and
            enemy["y"] - half <= player_y <= enemy["y"] + half):
            return True  # player is inside this enemy

    return False
#----------------
# Enemy Pew Pew 
#----------------
store = None
press = False
def handle_enemy_shooting(enemies, player_x, player_y, player_angle, screen_width, screen_height, max_center_radius=100, fov=FOV, player_damage=10):
    global player_z
    global store
    global press
    """
    Decreases health of the closest enemy to screen center if left mouse button is pressed.
    Only considers enemies in front of the player.
    """
    #if pygame.mouse.get_pressed()[0]:  # left click held
    if not press:
        #press = True
        center_x = screen_width // 2
        closest_dist = float("inf")
        target_enemy = None

        for enemy in enemies:
            # Angle from player to enemy
            angle_to_enemy = math.atan2(enemy["y"] - player_y, enemy["x"] - player_x)
            relative_angle = angle_to_enemy - player_angle

            # Wrap between -pi and pi
            relative_angle = (relative_angle + math.pi) % (2*math.pi) - math.pi

            # Only consider enemies in player's field of view
            if abs(relative_angle) < fov / 2:
                # Approximate screen x position
                screen_x = int((0.5 + relative_angle / fov) * screen_width)
                dx = screen_x - center_x
                dist = abs(dx)

                if dist <= max_center_radius and dist < closest_dist:
                    closest_dist = dist
                    target_enemy = enemy

            if target_enemy:
                target_enemy["health"] -= player_damage
                store = enemy["color"]
                enemy["color"] = [False,False,False]
                
                raycast()
                UI()
                pygame.display.flip()
                if player_z != ground_level:
                    pygame.time.wait(100)
                else:
                    pygame.time.wait(10)
                        
                
                enemy["color"] = store
                store = None
                print(f"Hit enemy! New health: {target_enemy['health']}")
                
    else:
        press = False

    




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
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_enemy_shooting(enemies, player_x, player_y, player_angle, WIDTH, HEIGHT)
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
    for enemy in enemies:

        
        if player_x < enemy["x"]:
            enemy["x"] -= enemy["speed"] * TILE
        if player_x > enemy["x"]:
            enemy["x"] += enemy["speed"] * TILE
        if player_y < enemy["y"]:
            enemy["y"] -= enemy["speed"] * TILE
        if player_y > enemy["y"]:
            enemy["y"] += enemy["speed"] * TILE
    raycast()
    UI()

    if keys[pygame.K_e]:
        draw_minimap()
    
    pygame.display.flip()
    if enemies == []:
        ran1 = random.randint(0, 1)
        ran2 = random.randint(0, 1)
        ran3 = random.randint(0, 1)
        if ran1 == 1:
            shade_mode[0] = not shade_mode[0]
        if ran2 == 1:
            shade_mode[1] = not shade_mode[1]
        if ran3 == 1:
            shade_mode[2] = not shade_mode[2]


        Wave += 1
        enemies = [
        {"x": random.randint(0,15) * TILE, "y": random.randint(0,8) * TILE, "speed": 0.025, "color":color_list[random.randint(1,7)], "health":50},
        {"x": random.randint(0,15) * TILE, "y": random.randint(0,8) * TILE, "speed": 0.03, "color":color_list[random.randint(1,7)], "health":50},
        #{"x": 9.3 * TILE, "y": 6 * TILE, "speed": 0.02, "color":[False,True,True], "health":50},
        #{"x": 6 * TILE, "y": 7 * TILE, "speed": 0.034, "color":[True,False,False], "health":50},
        #{"x": 12.3 * TILE, "y": 0 * TILE, "speed": 0.02, "color":[True,False,True], "health":70},
        {"x": random.randint(0,15) * TILE, "y": random.randint(0,8) * TILE, "speed": 0.035, "color":color_list[random.randint(1,7)], "health":70}

        
        ]
    
    for enemy in enemies:
        if enemy["health"] <= 0:
            kills += 1
    
    enemies = [enemy for enemy in enemies if enemy["health"] > 0]
   
    
pygame.quit()
sys.exit()
