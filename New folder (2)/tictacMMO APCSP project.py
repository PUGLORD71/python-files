import pygame
import sys
import random
# Initialize
pygame.init()

# Constants
GRID_SIZE = 7
CELL_SIZE = 80
WIDTH = GRID_SIZE * CELL_SIZE + 400
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 60
print(HEIGHT)
# Colors
BG_COLOR = (50, 50, 60)
GRID_COLOR = (0,0,0) #(30, 30, 35)
X_COLOR = (220, 80, 80)
O_COLOR = (80, 160, 255)
SELECT_COLOR = (255, 255, 255)

#font/text

font = pygame.freetype.Font("MedodicaRegular.otf")#<- not mine
font.size = 75
font.fgcolor = (255,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
X_ACT = ""
O_ACT = ""
RESULT = ""


# misc
O_amnt = 0
x_amnt = 0
gradient = [
    (100, 0, 0),
    (83, 0, 16),
    (66, 0, 33),
    (50, 0, 50),
    (33, 0, 66),
    (16, 0, 83),
    (0, 0, 100)
]
your_turn = True
turns = 1
Xplace = []
Oplace = []
time_offset = 0
X_HEALTH = 400
O_HEALTH = 400
X_DAMAGE = None
O_DAMAGE = None


board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


for i in range(1, 6):
    board[0][i] = "O"


for i in range(1, 6):
    board[GRID_SIZE - 1][i] = "X"

selected = None  

def draw_x(rect):
    padding = 15
    pygame.draw.line(screen, X_COLOR,
                     (rect.left + padding, rect.top + padding),
                     (rect.right - padding, rect.bottom - padding), 16)
    pygame.draw.line(screen, X_COLOR,
                     (rect.right - padding, rect.top + padding),
                     (rect.left + padding, rect.bottom - padding), 16)


def draw_o(rect):
    center = rect.center
    radius = rect.width // 2 - 15
    pygame.draw.circle(screen, O_COLOR, center, radius, 8)

#AI FUNC
def draw_turn(peice):
    t = pygame.time.get_ticks() * 0.003

    # panel area
    panel_x = WIDTH - 400
    panel_rect = pygame.Rect(panel_x + 40, 250, 320, 200)

    # base panel
    #pygame.draw.rect(screen, (10, 10, 15), panel_rect)
    #pygame.draw.rect(screen, (255, 255, 255), panel_rect, 3)

    # pulse effect
    pulse = int(15 * math.sin(t * 3))
    glow_size = 80 + pulse

    cx = panel_rect.centerx
    cy = panel_rect.centery + 10

    # =========================
    # COLOR + GLOW
    # =========================
    if peice == "X":
        main_color = X_COLOR
        glow_color = (100, 0, 80)
    else:
        main_color = O_COLOR
        glow_color = (0, 80, 100)

    # soft glow (background pulse)
    pygame.draw.circle(screen, (255,255,255), (cx, cy), glow_size,20)
    pygame.draw.circle(screen, glow_color, (cx + 10, cy + 10), glow_size)

    # =========================
    # DRAW SYMBOL
    # =========================
    size = 60

    if peice == "X":
        pygame.draw.line(screen, (0, 0, 0),
                         (cx - size + 8, cy - size + 8),
                         (cx + size + 8, cy + size + 8), 40)
        pygame.draw.line(screen, (0, 0, 0),
                         (cx + size + 8, cy - size + 8),
                         (cx - size + 8, cy + size + 8), 40)

        pygame.draw.line(screen, main_color,
                         (cx - size, cy - size),
                         (cx + size, cy + size), 40)
        pygame.draw.line(screen, main_color,
                         (cx + size, cy - size),
                         (cx - size, cy + size), 40)
    else:
        pygame.draw.circle(screen, (0, 0, 0),
                           (cx + 8, cy + 8), size, 32)
        pygame.draw.circle(screen, main_color,
                           (cx, cy), size, 32)

    # =========================
    # TEXT: "TURN"
    # =========================
    ##font.size = 45
   # font.fgcolor = (255, 255, 255)
    #font.render_to(screen, (panel_x + 120, 260), "TURN")

    # outline effect
    #font.fgcolor = (0, 0, 0)
    #font.render_to(screen, (panel_x + 118, 258), "TURN")

    #font.size = 75
    
def draw(clamp = False):
    screen.fill(BG_COLOR)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            piece = board[r][c]
            pygame.draw.rect(screen, gradient[-r + 6], rect)
            if piece == "X":
                pygame.draw.rect(screen, (60,0,0), rect)
                draw_x(rect)
            elif piece == "O":
                pygame.draw.rect(screen, (0,0,60), rect)
                draw_o(rect)
                
            pygame.draw.rect(screen, GRID_COLOR, rect, 6)
    
    if selected:
        r, c = selected
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, SELECT_COLOR, rect, 4)
    pygame.draw.rect(screen, (0,0,0), (WIDTH - 400, 0, 400, HEIGHT))
    font.fgcolor = O_COLOR
    font.render_to(screen, (600, 50), "O " + str(O_amnt))
    font.fgcolor = X_COLOR
    font.render_to(screen, (600, 100), "X " + str(X_amnt))
    font.fgcolor = (255,255,255)
    font.render_to(screen, (600, 200), "TURNS " + str(turns))
    if your_turn:
        draw_turn("X")
    else:
        draw_turn("O")
    if clamp:
        return
    pygame.display.flip()

    

def can_move(dr, dc, point):
    r, c = point
    nr, nc = r + dr, c + dc

    
    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
        if board[nr][nc] == "" or board[nr][nc] == "X":
            return True
        
    return False


def move_selected(dr, dc):
    global selected

    if not selected:
        return

    r, c = selected
    nr, nc = r + dr, c + dc

    
    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
        if board[nr][nc] != "" and board[nr][nc] != board[r][c]:
            vs_intro()
            fade_out(True)
            pygame.time.wait(1000)
            board[nr][nc] = battle_mode()
            print(board[nr][nc])
            board[r][c] = ""
            selected = None
            pygame.time.wait(1000)
            fade_in(True)

        elif board[nr][nc] == "":
            board[nr][nc] = board[r][c]
            board[r][c] = ""

    
    selected = None




# this func is AI
import math
def floor_effect():
    global time_offset

    horizon = HEIGHT // 2
    GRND_COLOR = (200, 0, 120)

    # Horizontal lines
    for i in range(1, 40):
        t = i / 40
        y = horizon + int((t ** 2) * (HEIGHT - horizon))

        wave = math.sin(time_offset + i * 0.3) * 10

        pygame.draw.line(
            screen,
            GRND_COLOR,
            (0, y + wave),
            (WIDTH, y + wave),
            2
        )

    # Vertical lines
    center = WIDTH // 2

    for i in range(-20, 21):
        x = i * 40
        shift = math.sin(time_offset * 0.5 + i * 0.5) * 30

        start_x = center + x * 0.2
        end_x = center + x * 2 + shift

        pygame.draw.line(
            screen,
            GRND_COLOR,
            (start_x, horizon),
            (end_x, HEIGHT),
            2
        )

    time_offset += 0.05
# AI FUNC
def rotate_point(x, y, z, ax, ay):
    # rotate X axis
    cosx = math.cos(ax)
    sinx = math.sin(ax)

    y, z = y * cosx - z * sinx, y * sinx + z * cosx

    # rotate Y axis
    cosy = math.cos(ay)
    siny = math.sin(ay)

    x, z = x * cosy + z * siny, -x * siny + z * cosy

    return x, y, z

#AI FUNC
def project(x, y, z, scale=500, distance=5):
    factor = scale / (z + distance)
    return x * factor + WIDTH * 3 // 4, y * factor + HEIGHT * 0.65

# AI FUnC
def draw_wire_x():
    t = pygame.time.get_ticks() * 0.001

    # make it "farther away"
    #base_depth = random.randint(2, 15)
    base_depth = 3
    # hover effect
    hover = math.sin(t * 2) * 0.4

    # rotation
    ax = t * 0.8
    ay = t * 0.6

    # cube vertices
    size = 1

    vertices = [
        [-size, -size, -size],
        [ size, -size, -size],
        [ size,  size, -size],
        [-size,  size, -size],
        [-size, -size,  size],
        [ size, -size,  size],
        [ size,  size,  size],
        [-size,  size,  size],
    ]

    # rotate + project
    points = []
    for v in vertices:
        x, y, z = rotate_point(v[0], v[1] + hover, v[2], ax, ay)
        x, y = project(x, y, z + base_depth)
        points.append((x + 100, y))

    color = (255, 80,80) #(255, 120, 120)

    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]

    # draw cube edges

    for a, b in edges:
        pygame.draw.line(screen, color, points[a], points[b], 16)

    # 🔥 "X core" (connect opposite corners = makes X identity)
    pygame.draw.line(screen, color, points[0], points[6], 16)
    pygame.draw.line(screen, color, points[1], points[7], 16)
    pygame.draw.line(screen, color, points[2], points[4], 16)
    pygame.draw.line(screen, color, points[3], points[5], 16)

#AI FUNC
def draw_wire_o():
    t = pygame.time.get_ticks() * 0.001

    # position (left side, slightly closer/far like X counterpart)
    base_x = WIDTH // 4
    base_y = HEIGHT * 0.5

    # same style depth as X (slightly far)
    base_depth = 6

    # hover (same vibe as X)
    hover = math.sin(t * 2) * 0.4

    # rotation (can be slower than X for contrast)
    ax = t * 0.6
    ay = t * 0.8

    radius = 1.2  # sphere size

    lat_steps = 10
    lon_steps = 10

    points = []

    # generate sphere points
    for i in range(lat_steps + 1):
        theta = (i / lat_steps) * math.pi

        for j in range(lon_steps):
            phi = (j / lon_steps) * 2 * math.pi

            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.cos(theta) + hover
            z = radius * math.sin(theta) * math.sin(phi)

            rx, ry, rz = rotate_point(x, y, z, ax, ay)

            px, py = project(rx, ry, rz + base_depth)
            points.append((px, py, i, j))

    color = (120, 200, 255)

    # draw latitude lines
    for i in range(lat_steps + 1):
        row = [p for p in points if p[2] == i]
        for k in range(len(row)):
            a = row[k]
            b = row[(k + 1) % len(row)]
            pygame.draw.line(screen, color, (a[0] - 500, a[1] - 100), (b[0] - 500, b[1] - 100), 4)

    # draw longitude lines
    for j in range(lon_steps):
        col = [p for p in points if p[3] == j]
        for k in range(len(col) - 1):
            a = col[k]
            b = col[k + 1]
            pygame.draw.line(screen, color, (a[0] - 500, a[1] - 100), (b[0] - 500, b[1] - 100), 4)

O_MOVES = ["DOUBLE UP", "BIGSHOT", "O-AURA", "HYPERBEAM", "4TH WALL", "CRASH OUT"]
fight_list = [{"name":"DOUBLE UP", "damage":32},
              {"name":"BIGSHOT", "damage":random.randint(75, 110)},
              {"name":"X-AURA", "damage":random.randint(0,50)*4},
              {"name":"HYPERBEAM", "damage":100},
              {"name":"4TH WALL", "damage":random.randint(-200, 200)},
              {"name":"CRASH OUT", "damage":50 * random.randint(1,5)}]

def random_moves():
    return_list = []
    ft_lis = ["DOUBLE UP", "BIGSHOT", "X-AURA", "HYPERBEAM", "4TH WALL", "CRASH OUT"]
    for i in range(4):
        return_list.append(random.choice(ft_lis))
        ft_lis.remove(return_list[len(return_list) - 1])
    return return_list

def handle_health(health, max_health, peicer):
    if peicer == "X":
        rect = pygame.Rect(WIDTH - 400, HEIGHT - 70, 400, 50)
        health_rect = pygame.Rect(WIDTH - 400, HEIGHT - 70, health, 50)
        helth_color = (100,0,80)
        tem_color = (255,80,80)
        
    else:
        rect = pygame.Rect(0, 50, 400, 50)
        health_rect = pygame.Rect(0, 50, health, 50)
        helth_color = (0,80,100)
        tem_color = (120, 200, 255)


    pygame.draw.rect(screen, helth_color, rect)
    pygame.draw.rect(screen, tem_color, health_rect)
    font.size = 35
    font.fgcolor = helth_color
    font.render_to(screen, (rect.x + 23, rect.y + 14), "HP: " + str(health) + "/" + str(max_health))
    font.fgcolor = (0,0,0)
    font.render_to(screen, (rect.x + 20, rect.y + 13), "HP: " + str(health) + "/" + str(max_health))
    pygame.draw.rect(screen, (0,0,0), rect, 8)
    pygame.draw.rect(screen, (255,255,255), rect, 2)

    font.size = 75

#AI FUNC
def text_wave(text, key):
    # create storage dict on first run
    if not hasattr(text_wave, "states"):
        text_wave.states = {}

    if key not in text_wave.states:
        text_wave.states[key] = {"index": 0, "timer": 0}

    state = text_wave.states[key]

    speed = 2
    state["timer"] += 1

    if state["timer"] >= speed:
        state["timer"] = 0
        if state["index"] < len(text):
            state["index"] += 1

    return text[:state["index"]]

def draw_console(line1, line2 = "", line3 = ""):
    #AI START
    # create a surface with per-pixel alpha
    rect_surf = pygame.Surface((550, 150), pygame.SRCALPHA)

    # fill with RGBA (A = transparency)
    rect_surf.fill((0, 0, 0, 170))  # red, semi-transparent

    # draw it onto screen
    screen.blit(rect_surf, (0, 410))
    #AI END
    pygame.draw.rect(screen, (255,255,255), (0, 410, 550, 150), 2)
    font.size = 50
    font.fgcolor = (255,255,255)
    font.render_to(screen, (20, 430), line1)
    font.render_to(screen, (20, 470), line2)
    font.render_to(screen, (20, 510), line3)
    font.size = 75
end_it = False
end_once = True
fight_text = None
line1 = ""
line2 = ""
line3 = ""


def battle_mode():
    fade_in()
    global X_HEALTH
    global end_once
    global X_ACT
    global line1
    global line2
    global line3
    global O_HEALTH
    global O_ACT
    global end_it
    global X_DAMAGE
    global O_DAMAGE
    global cur_but
    global RESULT
    running2 = True
    global fight_text
    fight_text = random_moves()
    
    while running2:
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        floor_effect()
        if O_HEALTH > 0:
            draw_wire_o()
        if X_HEALTH > 0:
            draw_wire_x()




        if X_DAMAGE and O_DAMAGE:
            if O_DAMAGE > X_DAMAGE:
                RESULT = "O DID " + str(O_DAMAGE) + " DAMAGE TO X!"
            if X_DAMAGE >= O_DAMAGE:
                RESULT = "X DID " + str(X_DAMAGE) + " DAMAGE TO O!"
            X_DAMAGE = None
            O_DAMAGE = None
        elif X_DAMAGE:
            RESULT = "X DIDNT DO MUCH . . ."
            X_DAMAGE = None
        elif O_DAMAGE:
            RESULT = "O DAMAGED X SLIGHTLY. . ."
            O_DAMAGE = None
        elif RESULT == "" and O_HEALTH > 0 and X_HEALTH > 0:
        
            RESULT = "START FIGHTING YOU TWO!"
        #AI
        if X_ACT != "":
            line1 = text_wave(X_ACT, "line1")

            # only start line2 after line1 finishes
            if len(line1) == len(X_ACT):
                line2 = text_wave(O_ACT, "line2")
            else:
                line2 = ""

            # only start line3 after line2 finishes
            if len(line2) == len(O_ACT):
                line3 = text_wave(RESULT, "line3")
            else:
                line3 = ""
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                if end_once:
                    end_once = False
                    line1 = ""
                    line2 = ""
                    line3 = ""
                    text_wave.states = {}
                    X_ACT = ""
                    O_ACT = ""
                    RESULT = ""
                    if X_HEALTH <= 0 or O_HEALTH <= 0:
                        end_it = True
                    else:
                        cur_but = None
                    if X_HEALTH <= 0 and cur_but != "pp":
                        O_ACT = "O IS THE VICTOR!"
                        X_ACT = "YOU LOST. . ."
                        end_it = False
                        cur_but = "pp"
                    if O_HEALTH <= 0 and cur_but != "pp":
                        
                        O_ACT = "X LIVES AND MOVES ON!"
                        X_ACT = "YOU WIN!"
                        end_it = False
                        cur_but = "pp"
                    
                        
            else:
                end_once = True
                
                    
        else:
            line1 = ""
            line2 = ""
            line3 = ""
        #AI END
        draw_console(line1, line2, line3)
        
        if button_handler() or X_HEALTH <= 0 or O_HEALTH <= 0:
            if end_it:
                print("ended")
                X_ACT = ""
                O_ACT = ""
                RESULT = ""
                end_it = False
                cur_but = None
                
                fight_list = [{"name":"DOUBLE UP", "damage":32},
                  {"name":"BIGSHOT", "damage":random.randint(75, 110)},
                  {"name":"X-AURA", "damage":random.randint(0,50)*4},
                  {"name":"HYPERBEAM", "damage":100},
                  {"name":"4TH WALL", "damage":random.randint(-200, 200)},
                  {"name":"CRASH OUT", "damage":50 * random.randint(1,5)}]
                if X_HEALTH <= 0 and O_HEALTH <= 0:
                    fade_out()
                    X_HEALTH = 400
                    O_HEALTH = 400
                    
                    return "O"
            
                elif O_HEALTH <= 0:
                    fade_out()
                    X_HEALTH = 400
                    O_HEALTH = 400
                    
                    return "X"
                else:
                    fade_out()
                    X_HEALTH = 400
                    O_HEALTH = 400
                    
                    return "O"
                
        
        handle_health(X_HEALTH, 400, "X")
        handle_health(O_HEALTH, 400, "O")
        pygame.display.flip()
        

def O_FIGHT(mod = 1):
    global O_ACT
    global X_HEALTH
    global O_DAMAGE
    global O_HEALTH
    
    decider = random.randint(1, 6)
    index = random.randint(1, 5)
    
    if decider > 1:
        if fight_list[index]["name"] == "X-AURA":
            O_ACT = "O USED O-AURA!"
        else:
            O_ACT = "O USED " +fight_list[index]["name"] + "!"
        animation_handler(fight_list[index], "O")
        X_HEALTH -= int(fight_list[index]["damage"] * mod)
        O_DAMAGE = int(fight_list[index]["damage"] * mod)
        
        if X_HEALTH <= 0:
            X_HEALTH = 0
    else:
        O_ACT = "O USED HEAL!"
        animation_handler("heal", "O")
        O_HEALTH += 225
        if O_HEALTH > 400:
            O_HEALTH = 400

    
    
    
#button handler
cur_but = None
once = True
down = False
def button_handler():
    global cur_but
    global fight_text
    global X_HEALTH
    global X_DAMAGE
    global fight_list
    global once
    global end_it
    global O_HEALTH
    global down
    global X_ACT
    top_right = pygame.Rect(290, HEIGHT - 140, 250, 50)
    bottom_left = pygame.Rect(20, HEIGHT - 70, 250, 50)
    bottom_right = pygame.Rect(290, HEIGHT - 70, 250, 50)
    top_left = pygame.Rect(20, HEIGHT - 140, 250, 50)
    buttons = [top_left, top_right, bottom_left, bottom_right]
    menu_text = ["F I G H T < <", "DEFEND  < < ", "H E A L   < <", "FORFEIT < <"]
    if cur_but == None:
        for i in range(4):
            x,y = pygame.mouse.get_pos()
            but_color = (255, 80,80)
            if buttons[i].collidepoint( (x,y) ):
                but_color = (255,230,0)
            if pygame.mouse.get_pressed()[0]:
                if buttons[i].collidepoint( (x,y) ) and not down:
                    cur_but = menu_text[i]
                    down = True
            else:
                down = False
                    
            font.fgcolor = (0,0,0)
            font.size = 50
            pygame.draw.rect(screen, (but_color), buttons[i])
            font.fgcolor = (100,0,80)
            font.render_to(screen, (buttons[i].x + 24, buttons[i].y + 15), menu_text[i])
            font.fgcolor = (0,0,0)
            font.render_to(screen, (buttons[i].x + 20, buttons[i].y + 13), menu_text[i])
            pygame.draw.rect(screen, (0,0,0), buttons[i], 8)
            pygame.draw.rect(screen, (255,255,255), buttons[i], 2)
    font.size = 75
    if cur_but == menu_text[0]:#fight
        for i in range(4):
            x,y = pygame.mouse.get_pos()
            but_color = (255, 80,80)
            if buttons[i].collidepoint( (x,y) ):
                but_color = (255,200,0)# (170,0,0)
            if pygame.mouse.get_pressed()[0]:
                if buttons[i].collidepoint( (x,y) ) and not down:
                    for move in fight_list:
                        if fight_text[i] == move["name"]:

                            animation_handler(move, "X")
                            O_HEALTH -= move["damage"]
                            X_DAMAGE = move["damage"]
                            X_ACT = "X USED " + move["name"] + "!"
                            if fight_text[i] == "DOUBLE UP" and O_HEALTH > 0:
                                move["damage"] *= 2
                            elif O_HEALTH <= 0 and move["name"] == "DOUBLE UP":
                                move["damage"] = 32
                                

                            if O_HEALTH <= 0:
                                O_HEALTH = 0
                            O_FIGHT()
                            cur_but = "ppp"
                    down = True           #^^^ animation here eventually
            else:
                down = False
            font.fgcolor = (0,0,0)
            font.size = 50
            pygame.draw.rect(screen, (but_color), buttons[i])
            font.fgcolor = (100,0,80)
            font.render_to(screen, (buttons[i].x + 24, buttons[i].y + 15), fight_text[i])
            font.fgcolor = (0,0,0)
            font.render_to(screen, (buttons[i].x + 20, buttons[i].y + 13), fight_text[i])
            pygame.draw.rect(screen, (0,0,0), buttons[i], 8)
            pygame.draw.rect(screen, (255,255,255), buttons[i], 2)
        x,y = pygame.mouse.get_pos()
        but_color = (100,0,80)
        rect = pygame.Rect(560, HEIGHT - 140, 50, 50)
        if rect.collidepoint( (x,y) ):
            but_color = (255,200,0)
        
        if pygame.mouse.get_pressed()[0]:
            if rect.collidepoint( (x,y) ):
                cur_but = None
        
        pygame.draw.rect(screen, (but_color), rect)
        font.render_to(screen, (rect.x + 20, rect.y + 13), ">")
        pygame.draw.rect(screen, (0,0,0), rect, 8)
        pygame.draw.rect(screen, (255,255,255), rect, 2)
    if cur_but == menu_text[3]:
        cur_but = None
        end_it = True
        fight_list = [{"name":"DOUBLE UP", "damage":32},
        {"name":"BIGSHOT", "damage":random.randint(75, 110)},
        {"name":"X-AURA", "damage":random.randint(0,50)*4},
        {"name":"HYPERBEAM", "damage":100},
        {"name":"4TH WALL", "damage":random.randint(-200, 200)},
        {"name":"CRASH OUT", "damage":50 * random.randint(1,5)}]
        return True
    elif cur_but == menu_text[2]:
        #cur_but = None
        if once:
            animation_handler("heal", "X")
            X_HEALTH += 125
            if X_HEALTH > 400:
                X_HEALTH = 400
            once = False
            X_ACT = "X USED HEAL!"
            
            O_FIGHT()
    elif cur_but == menu_text[1]:
        #cur_but = None
        if once:
            
            once = False
            X_ACT = "X USED DEFEND!"
            animation_handler("DEFEND", "X")
            O_FIGHT(0.25)
    else:
        once = True

#AI FUNC
def animation_handler(move, peice):
    global line1
    global line2
    global line3
    if move == "heal":
        name = move
    elif move == "DEFEND":
        name = move
    else:
        name = move["name"]
    duration = 120  # frames

    for frame in range(duration):
        clock.tick(FPS)

        floor_effect()
        
        draw_wire_o()
        
        draw_wire_x()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # dark fade overlay (makes effects pop)
        fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fade.fill((0, 0, 0, 60))
        screen.blit(fade, (0, 0))
        if peice == "X":
            if name == "heal" or name == "DEFEND":
                cx, cy = (815, 379)
            else:
                cx,cy = (220, 271)

        elif peice == "O":
            if name == "heal":
                cx,cy = (220, 271)
            else:
                cx, cy = (815, 379)
        else:
            return

        # =========================
        # DOUBLE UP (pulse + duplicate flash)
        # =========================
        if name == "DOUBLE UP":
            radius = 50 + frame * 3
            pygame.draw.circle(screen, (255, 80, 80), (cx - 50, cy), radius, 5)
            pygame.draw.circle(screen, (255, 80, 80), (cx + 50, cy), radius, 5)

        # =========================
        # BIGSHOT (screen shake + blast)
        # =========================
        elif name == "BIGSHOT":
            shake_x = random.randint(-10, 10)
            shake_y = random.randint(-10, 10)

            pygame.draw.circle(screen, (255, 200, 0),
                               (cx + shake_x, cy + shake_y),
                               30 + frame * 4)

        # =========================
        # X-AURA (spinning lines)
        # =========================
        elif name == "X-AURA":
            for i in range(6):
                angle = frame * 0.2 + i
                x = cx + int(120 * math.cos(angle))
                y = cy + int(120 * math.sin(angle))
                if peice == "X":
                    pygame.draw.line(screen, (255, 80, 80), (cx, cy), (x, y), 28)
                else:
                    pygame.draw.line(screen, (120, 200, 255), (cx, cy), (x, y), 28)
        # =========================
        # HYPERBEAM (laser beam)
        # =========================
        elif name == "HYPERBEAM":
            width = 10 + frame
            pygame.draw.rect(screen, (255, 255, 255),
                             (0, cy - width // 2, WIDTH, width))

        # =========================
        # 4TH WALL (glitch rectangles)
        # =========================
        elif name == "4TH WALL":
            for _ in range(10):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                w = random.randint(20, 100)
                h = random.randint(10, 50)
                color = random.choice([(255,0,0), (0,255,255), (255,255,255)])
                pygame.draw.rect(screen, color, (x, y, w, h))

        # =========================
        # CRASH OUT (explosion particles)
        # =========================
        elif name == "CRASH OUT":
            for _ in range(20):
                angle = random.random() * 2 * math.pi
                speed = random.randint(2, 8)
                x = cx + int(frame * speed * math.cos(angle))
                y = cy + int(frame * speed * math.sin(angle))
                if peice == "X":
                    pygame.draw.circle(screen, (255, 80,80), (x, y), 20)
                else:
                    pygame.draw.circle(screen, (120, 200, 255), (x, y), 20)

        # =========================
        # HEAL (shrinking white ring)
        # =========================
        elif name == "heal":
            max_radius = 200
            radius = max_radius - int((frame / duration) * max_radius)

            if radius > 0:
                pygame.draw.circle(screen, (255, 255, 255), (cx, cy), radius, 16)                    
        # =========================
        # DEFEND (shield pulse)
        # =========================
        elif name == "DEFEND":
            progress = frame / duration

            # quick scale pulse
            pulse = 1 + 0.3 * math.sin(progress * math.pi * 6)

            # expanding ring
            radius = int(30 + progress * 190)
        
            # slight glow offset for depth
            glow_offset = 20

            
            pygame.draw.circle(screen, (100,0,80), (cx, cy), int(radius * pulse))

        
            # outer glow (shadow)
            pygame.draw.circle(screen, (0, 0, 0), (cx + glow_offset, cy + glow_offset), int(radius * pulse), 30)

            
            # main shield ring
            pygame.draw.circle(screen, (255,80,80), (cx, cy), int(radius * pulse), 30)

            # inner core flash
            

                

        handle_health(X_HEALTH, 400, "X")
        handle_health(O_HEALTH, 400, "O")
        pygame.display.flip()
        

def spawn(peiced):
    global board
    started = True
    while started:
        xr, xc = (random.randint(0, 6), random.randint(0,6))
        if board[xr][xc] == "":
            board[xr][xc] = peiced
            started = False

        
    return

def fade_in(scene = False):
    global running
    global ending
    
    fad = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for j in range(255):
        clock.tick(120)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                ending = False
        screen.fill((0,0,0))
        if scene:
            draw(True)
        else:
            
            floor_effect()
            if O_HEALTH > 0:
                draw_wire_o()
            if X_HEALTH > 0:
                draw_wire_x()
            draw_console("")
            top_right = pygame.Rect(290, HEIGHT - 140, 250, 50)
            bottom_left = pygame.Rect(20, HEIGHT - 70, 250, 50)
            bottom_right = pygame.Rect(290, HEIGHT - 70, 250, 50)
            top_left = pygame.Rect(20, HEIGHT - 140, 250, 50)
            buttons = [top_left, top_right, bottom_left, bottom_right]
            menu_text = ["F I G H T < <", "DEFEND  < < ", "H E A L   < <", "FORFEIT < <"]
            for i in range(4):
                font.fgcolor = (0,0,0)
                font.size = 50
                pygame.draw.rect(screen, (255,80,80), buttons[i])
                font.fgcolor = (100,0,80)
                font.render_to(screen, (buttons[i].x + 24, buttons[i].y + 15), menu_text[i])
                font.fgcolor = (0,0,0)
                font.render_to(screen, (buttons[i].x + 20, buttons[i].y + 13), menu_text[i])
                pygame.draw.rect(screen, (0,0,0), buttons[i], 8)
                pygame.draw.rect(screen, (255,255,255), buttons[i], 2)
            handle_health(X_HEALTH, 400, "X")
            handle_health(O_HEALTH, 400, "O")
            
            
        fad.fill((0, 0, 0, (-j + 255)))
        screen.blit(fad, (0, 0))
        pygame.display.flip()

def fade_out(scene = False):
    global running
    global ending
    
    fad = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for j in range(255):
        clock.tick(120)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                ending = False
        screen.fill((0,0,0))
        if scene:
            screen.fill((255,255,255))
            #draw(True)
        else:
            
            floor_effect()
            if O_HEALTH > 0:
                draw_wire_o()
            if X_HEALTH > 0:
                draw_wire_x()
            draw_console("")
            top_right = pygame.Rect(290, HEIGHT - 140, 250, 50)
            bottom_left = pygame.Rect(20, HEIGHT - 70, 250, 50)
            bottom_right = pygame.Rect(290, HEIGHT - 70, 250, 50)
            top_left = pygame.Rect(20, HEIGHT - 140, 250, 50)
            buttons = [top_left, top_right, bottom_left, bottom_right]
            menu_text = ["F I G H T < <", "DEFEND  < < ", "H E A L   < <", "FORFEIT < <"]
            for i in range(4):
                font.fgcolor = (0,0,0)
                font.size = 50
                pygame.draw.rect(screen, (255,80,80), buttons[i])
                font.fgcolor = (100,0,80)
                font.render_to(screen, (buttons[i].x + 24, buttons[i].y + 15), menu_text[i])
                font.fgcolor = (0,0,0)
                font.render_to(screen, (buttons[i].x + 20, buttons[i].y + 13), menu_text[i])
                pygame.draw.rect(screen, (0,0,0), buttons[i], 8)
                pygame.draw.rect(screen, (255,255,255), buttons[i], 2)
            handle_health(X_HEALTH, 400, "X")
            handle_health(O_HEALTH, 400, "O")
            
        fad.fill((0, 0, 0, j))
        screen.blit(fad, (0, 0))
        pygame.display.flip()
        
        
        
    return




#AI FUNC
def vs_intro():
    duration = 240
    shake_frames = 60

    for frame in range(duration):
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        t = frame / duration

        # =========================
        # SLIDE IN
        # =========================
        left_offset = int((1 - min(t * 2, 1)) * -WIDTH)
        right_offset = int((1 - min(t * 2, 1)) * WIDTH)

        # =========================
        # SCREEN SHAKE (END)
        # =========================
        shake_x = shake_y = 0
        if frame > duration - shake_frames:
            shake_x = random.randint(-10, 10)
            shake_y = random.randint(-10, 10)

        screen.fill((0, 0, 0))

        # =========================
        # BACKGROUND GRADIENT
        # =========================
        for x in range(WIDTH):
            
            if x < WIDTH // 2:
                # NOW RED on left
                color = (120 + int(80 * (x / (WIDTH//2))), 0, 0)
            else:
                # NOW BLUE on right
                color = (0, 0, 120 + int(80 * ((x - WIDTH//2)/(WIDTH//2))))
                
            pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))
        pygame.draw.line(screen, (0,0,0), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 75)

        # =========================
        # PANELS
        # =========================
        left_poly = [
            (left_offset, 0),
            (WIDTH//2 - 80 + left_offset, 0),
            (WIDTH//2 - 200 + left_offset, HEIGHT),
            (left_offset, HEIGHT)
        ]

        right_poly = [
            (WIDTH + right_offset, 0),
            (WIDTH//2 + 80 + right_offset, 0),
            (WIDTH//2 + 200 + right_offset, HEIGHT),
            (WIDTH + right_offset, HEIGHT)
        ]

        pygame.draw.polygon(screen, (0,0,0), left_poly)
        pygame.draw.polygon(screen, (0,0,0), right_poly)

        # =========================
        # GLOW LINES
        # =========================
        def glow(points, color):
            for i in range(6, 0, -1):
                pygame.draw.lines(screen, color, False, points, i * 4)

        glow(left_poly, (255, 80, 80))
        glow(right_poly, (80, 160, 255))
        
        # =========================
        # BIG X AND O (SLIDE WITH PANELS)
        # =========================
        x_center = (WIDTH//4 + left_offset, HEIGHT//2)
        o_center = (WIDTH*3//4 + right_offset, HEIGHT//2)

        size = 120
        offset = 20
        # DRAW X


        pygame.draw.line(screen, (100, 0, 80),
                         (x_center[0]-size - offset, x_center[1]-size + offset),
                         (x_center[0]+size - offset, x_center[1]+size + offset), 60)
        pygame.draw.line(screen, (100, 0, 80),
                         (x_center[0]+size - offset, x_center[1]-size +offset),
                         (x_center[0]-size - offset, x_center[1]+size +offset), 60)


        pygame.draw.line(screen, (255, 80, 80),
                         (x_center[0]-size, x_center[1]-size),
                         (x_center[0]+size, x_center[1]+size), 60)
        pygame.draw.line(screen, (255, 80, 80),
                         (x_center[0]+size, x_center[1]-size),
                         (x_center[0]-size, x_center[1]+size), 60)

                

        # DRAW O

        circx, circy = o_center
        pygame.draw.circle(screen, (0,80,100),
                           (circx + offset, circy + offset), size, 50)
        
        pygame.draw.circle(screen, (120, 200, 255),
                           o_center, size, 50)
        

        # =========================
        # VS TEXT (WITH SHAKE)
        # =========================
        cx = WIDTH // 2 + shake_x
        cy = HEIGHT // 2 + shake_y

        vs_font = pygame.freetype.Font(None, 200)

        # glow
        for i in range(5, 0, -1):
            vs_font.render_to(
                screen,
                (cx - 110 - i*5, cy - 80 - i*5),
                "VS",
                (0, 0, 0)
            )

        vs_font.render_to(screen, (cx - 150, cy - 110), "VS", (255, 255, 255))

        # =========================
        # CENTER BURST
        # =========================
        if frame > duration - shake_frames:
            progress = (frame - (duration - shake_frames)) / shake_frames

            # expanding radius (BIG so it covers screen)
            p = progress ** 2
            radius = int(50 + p * max(WIDTH, HEIGHT))

            # =========================
            # SHADOW CIRCLE (offset)
            # =========================
            pygame.draw.circle(screen, (0, 0, 0), (cx - 20, cy + 20), radius)

            # =========================
            # MAIN WHITE CIRCLE
            # =========================
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), radius)
        pygame.display.flip()





#AI FUNC
def winner(peice):
    t = 0
    particles = []

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # =========================
        # BACKGROUND GRADIENT
        # =========================
        for x in range(WIDTH):
            if peice == "X":
                color = (120 + int(100 * (x / WIDTH)), 0, 0)
            else:
                color = (0, 0, 120 + int(100 * (x / WIDTH)))
            pygame.draw.line(screen, color, (x, 0), (x, HEIGHT))

        cx, cy = WIDTH // 2, HEIGHT // 2
        # =========================
        # PARTICLES (BURST LOOP)
        # =========================
        if random.random() < 0.3:
            angle = random.random() * 2 * math.pi
            speed = random.randint(2, 6)
            particles.append([cx, cy, angle, speed])

        for p in particles[:]:
            p[0] += math.cos(p[2]) * p[3]
            p[1] += math.sin(p[2]) * p[3]

            if peice == "X":
                color = (255, 80, 80)
            else:
                color = (120, 200, 255)

            pygame.draw.circle(screen, color, (int(p[0]), int(p[1])), 15)

            # remove far particles
            if abs(p[0] - cx) > 400 or abs(p[1] - cy) > 400:
                particles.remove(p)




        # =========================
        # ENERGY PANELS (SLIDING)
        # =========================
        slide = int((math.sin(t * 2) * 100))

        if peice == "X":
            panel_color = (0, 0, 0)
        else:
            panel_color = (0, 0, 0)

        pygame.draw.rect(screen, panel_color,
                         (0 - 200 + slide, 0, 200, HEIGHT))
        pygame.draw.rect(screen, panel_color,
                         (WIDTH - slide, 0, 200, HEIGHT))

        # =========================
        # BIG CENTER SYMBOL (PULSE)
        # =========================
        cx, cy = WIDTH // 2, HEIGHT // 2
        pulse = int(20 * math.sin(t * 4))

        size = 120 + pulse

        if peice == "X":

            pygame.draw.line(screen, (0,0,0),
                             (cx - size + 20, cy - size+20),
                             (cx + size+20, cy + size+20), 100)
            pygame.draw.line(screen, (0,0,0),
                             (cx + size+20, cy - size+20),
                             (cx - size+20, cy + size+20), 100)
            pygame.draw.line(screen, (255, 255, 255),
                             (cx - size, cy - size),
                             (cx + size, cy + size), 100)
            pygame.draw.line(screen, (255, 255, 255),
                             (cx + size, cy - size),
                             (cx - size, cy + size), 100)

            
        else:
            pygame.draw.circle(screen, (0,0,0),
                               (cx+20, cy+20), size, 70)
            pygame.draw.circle(screen, (255, 255, 255),
                               (cx, cy), size, 70)

    
        # =========================
        # WIN TEXT (WAVE)
        # =========================
        font.size = 120

        if peice == "X":
            text = "  X WINS"
            font.fgcolor = (255, 80, 80)
        else:
            text = "  O WINS"
            font.fgcolor = (120, 200, 255)
        font.fgcolor = (255,255,255)
        offset = int(math.sin(t * 3) * 10)
        font.render_to(screen, (cx - 200, cy + 180 + offset), text)

        # shadow
        font.fgcolor = (0, 0, 0)
        font.render_to(screen, (cx - 205, cy + 185 + offset), text)

        font.size = 75

        pygame.display.flip()

        t += 0.05



won = None
ending = True
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            ending = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if mx < GRID_SIZE* CELL_SIZE and my< GRID_SIZE * CELL_SIZE:
                c = mx // CELL_SIZE
                r = my //CELL_SIZE

                if board[r][c] == "X" and your_turn:
                    selected = (r, c)
                

        elif event.type == pygame.KEYDOWN:
            if selected and your_turn:
                if event.key == pygame.K_UP:
                    move_selected(-1, 0)
                    your_turn = False
                    
                elif event.key == pygame.K_DOWN:
                    move_selected(1, 0)
                    your_turn = False
                    
                elif event.key == pygame.K_LEFT:
                    move_selected(0, -1)
                    your_turn = False
                    
                elif event.key == pygame.K_RIGHT:
                    move_selected(0, 1)
                    your_turn = False
                elif event.key == pygame.K_SPACE:
                    winner("X")
                    pass
    
    
    
    X_amnt = 0
    O_amnt = 0
    Xplace = []
    Oplace = []
    for r in range(7):
        for c in range(7):
            if board[r][c] == "X": 
                X_amnt += 1
                Xplace.append( (r, c) )
            if board[r][c] == "O":
                O_amnt += 1
                Oplace.append( (r, c) )

    if X_amnt <= 0:
        running = False
        won = False
        winner("O")
        break
    elif O_amnt <= 0:
        running = False
        won = True
        winner("X")
        break
    for c in range(7):
        
        if board[0][c] == "X":
            if board[1][c] == "X":
                if board[2][c] == "X":
                    if board[3][c] == "X":
                        if board[4][c] == "X":
                            if board[5][c] == "X":
                                if board[6][c] == "X":
                                    running = False
                                    won = True
                                    winner("X")
                                    



    
    
    #AI TURN
    if running == True:
        if not selected and not your_turn:
            index = random.randint(0, len(Oplace) - 1)
            selected = Oplace[index]
            passed = False
            while not passed:
                if can_move(-1, 0, selected):
                    passed = True
                elif can_move(1, 0, selected):
                    passed = True
                elif can_move(0, -1, selected):
                    passed = True
                elif can_move(0, 1, selected):
                    passed = True
                else:
                    index = random.randint(0, len(Oplace) - 1)
                    selected = Oplace[index]
            draw()
            pygame.time.wait(500)
            #move_dir = random.randint(1,4)
            #chatgpt
            if not your_turn:
                possible_moves = []

                # Check all directions and store valid ones
                if can_move(-1, 0, selected):
                    possible_moves.append((-1, 0))

                if can_move(1, 0, selected):
                    possible_moves.append((1, 0))

                if can_move(0, -1, selected):
                    possible_moves.append((0, -1))

                if can_move(0, 1, selected):
                    possible_moves.append((0, 1))

                # Pick a random move if any exist
                if possible_moves:
                    dr, dc = random.choice(possible_moves)
                    move_selected(dr, dc)
                    your_turn = True
                # else: do nothing (no valid moves)
                #end of chatgpt code
            if turns % 25 == 0:
                if X_amnt < 10:
                    spawn("X")
                if O_amnt < 10:
                    spawn("O")
            turns += 1
        
         



    draw()
    



while False: # ending
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ending = False

    screen.fill((0,0,0,))
    font.fgcolor = (255,255,255)
    font.size = 100
    if won:
        font.render_to(screen, (100,200), "YOU WIN!")
    else:
        font.render_to(screen, (100,200), "YOU LOSE. . .")
    pygame.display.flip()
    
pygame.quit()
sys.exit()

























