import pygame, sys, random
pygame.init()
WIDTH = 1000
HEIGHT = WIDTH // 2
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hollow Knight")
clock = pygame.time.Clock()

# ---------------- CONSTANTS ----------------
GRAVITY = 0.6
PLAYER_SPEED = 4
JUMP_POWER = 11
POGO_BOOST = 12
DASH_SPEED = 14
MAX_HP = 5
MAX_LIVES = 5
DASH_CD_MAX = 40
hit_boxes = False
WALL_SLIDE_SPEED = 0.2
WALL_JUMP_X = 6
WALL_JUMP_Y = 12
restart_pos = (100, 300)
restart_room = 0


# ---------------- DECOR PALETTES ----------------
PALETTES = {
    "forg_roads": {
        "dark": (30, 30, 40),
        "mid": (60, 60, 80),
        "light": (120, 120, 140),
        "accent": (180, 180, 200)
    },
    "greenpath": {
        "dark": (20, 50, 30),
        "mid": (40, 90, 60),
        "light": (100, 160, 120),
        "accent": (160, 220, 180)
    },
    "deepnest": {
        "dark": (30, 30, 35),
        "mid": (50, 50, 60),
        "light": (70, 70, 90),
        "accent": (140, 140, 170)
    }
}

CURRENT_PALETTE = PALETTES["forg_roads"]


# ---------------- GLOBAL FX ----------------
hit_pause = 0
shake = 0
cam_x = cam_y = 0
room_lock = 0
FOCUS_TIMER = 0

# ------------------- SFX -------------------
saw_sound = pygame.mixer.Sound("sawtooth_sfx.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
pogo_sound = pygame.mixer.Sound("dub.wav")
ouch_sound = pygame.mixer.Sound("ouch.wav")
jump_sound = pygame.mixer.Sound("jump.wav")
bg_ =  pygame.mixer.Sound("daw.opus")
live_sound =  pygame.mixer.Sound("live.wav")
bg_.set_volume(0.3)
bg_.play(-1)
# ---------------- TRANSITION ----------------
transition_alpha = 0
transition_dir = 0
next_room = None


# =========================================================
# GAME STATE SYSTEM
# =========================================================
STATE_MENU     = "menu"
STATE_PLAYING  = "playing"
STATE_CONTROLS = "controls"
STATE_PAUSE    = "pause"

game_state = STATE_MENU

# =========================================================
# FONTS
# =========================================================
FONT_BIG   = pygame.font.SysFont("arial", 72)
FONT_MED   = pygame.font.SysFont("arial", 36)
FONT_SMALL = pygame.font.SysFont("arial", 24)
# ---------------- LEVEL EDITOR ----------------
EDITOR_MODE = False
EDITOR_TOOL = "platform"   # "platform" or "saw"
editor_start = None
editor_rects = None
editor_saws = None
GRID = 25
editor_radius = 16
# =========================================================
# MENU DRAW FUNCTIONS
# =========================================================
def draw_menu():
    screen.fill((15, 15, 25))
    title = FONT_BIG.render("HOLLOW KNIGHT", True, (230,230,240))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

    opts = ["ENTER - START", "C - CONTROLS", "ESC - QUIT"]
    for i, txt in enumerate(opts):
        t = FONT_MED.render(txt, True, (200,200,210))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 300 + i*60))


def draw_controls():
    screen.fill((15,15,25))
    title = FONT_BIG.render("CONTROLS", True, (230,230,240))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    lines = [
        "A / D        - Move",
        "SPACE / E - Jump",
        "J            - Attack",
        "S + J        - Down Slash (Pogo)",
        "K            - Dash",
        "L            - Focus (Heal)",
        "ESC          - Pause / Back"
    ]

    for i, line in enumerate(lines):
        t = FONT_SMALL.render(line, True, (210,210,220))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 220 + i*35))


def draw_pause():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,160))
    screen.blit(overlay, (0,0))

    t = FONT_BIG.render("PAUSED", True, (255,255,255))
    screen.blit(t, (WIDTH//2 - t.get_width()//2, 200))

    s = FONT_SMALL.render("SPACE to Resume | ESC to Quit to Menu", True, (220,220,220))
    screen.blit(s, (WIDTH//2 - s.get_width()//2, 300))

def snap(val):
    return (val // GRID) * GRID




def rect_from_points(x1,y1,x2,y2):
    x=min(x1,x2); y=min(y1,y2)
    w=abs(x2-x1); h=abs(y2-y1)
    return pygame.Rect(snap(x),snap(y),snap(w),snap(h))

def export_rects(rects):
    print("\n# -------- COPY BELOW --------")
    print("[")
    for r in rects:
        print(f"    pygame.Rect({r.x}, {r.y}, {r.w}, {r.h}),")
    print("]")
    print("# -------- COPY ABOVE --------\n")

def export_room(room):
    print("\n# ===== COPY BELOW =====")
    print("{")
    print("  \"platforms\": [")
    for r in room["platforms"]:
        print(f"    pygame.Rect({r.x}, {r.y}, {r.w}, {r.h}),")
    print("  ],")

    print("  \"enemies\": [],")

    print("  \"saws\": [")
    for s in room["saws"]:
        print(
            "    Saw("
            f"{int(s.x)}, {int(s.y)}, "
            f"radius={s.radius}, "
            f"vx={s.vx}, "
            f"min_x={s.min_x}, "
            f"max_x={s.max_x}"
            "),"
        )
    print("  ]")
    print("}")
    print("# ===== COPY ABOVE =====\n")

# ---------------- PARTICLES ----------------
class Particle:
    def __init__(self, x, y, color=(255,200,200)):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.life = 100
        self.color = color

    def update(self):
        self.vy += 0.25
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x+cam_x), int(self.y+cam_y)), 8)
# ------ MISC -------
e_down = False
# ---------- BG -----------
def draw_hk_background():
    dark  = CURRENT_PALETTE["dark"]
    mid   = CURRENT_PALETTE["mid"]
    light = CURRENT_PALETTE["light"]
        
    half = HEIGHT // 2
    screen.fill(dark)
    # ---------------- MIRRORED GRADIENT ----------------
    #for y in range(HEIGHT):
     #   d = abs(y - half) / half   # 0 at center, 1 at top/bottom
      #  t = min(d * 2, 1)

       # col = (
        #    int(light[0] * (1 - t) + dark[0] * t),
         #   int(light[1] * (1 - t) + dark[1] * t),
          #  int(light[2] * (1 - t) + dark[2] * t),
        #)

        # soften center with mid tone
        #if d < 0.25:
         #   m = d / 0.25
          #  col = (
           #     int(light[0] * (1 - m) + mid[0] * m),
            #    int(light[1] * (1 - m) + mid[1] * m),
             #   int(light[2] * (1 - m) + mid[2] * m),
            #)

        #pygame.draw.line(screen, col, (0, y), (WIDTH, y))

    # ---------------- TOP & BOTTOM SILHOUETTES ----------------
    far = tuple(max(c - 10, 0) for c in dark)
    near = tuple(max(c - 25, 0) for c in dark)

    # Bottom
    for x in range(-150, WIDTH + 200, 260):
        pygame.draw.ellipse(
            screen, far,
            (x, HEIGHT * 0.65, 320, 220)
        )
        pygame.draw.ellipse(
            screen, near,
            (x + 60, HEIGHT * 0.75, 360, 260)
        )

    # Top (mirrored)
    for x in range(-150, WIDTH + 200, 260):
        pygame.draw.ellipse(
            screen, far,
            (x, -HEIGHT * 0.15, 320, 220)
        )
        pygame.draw.ellipse(
            screen, near,
            (x + 60, -HEIGHT * 0.30, 360, 260)
        )


# ---------------- PLAYER ----------------

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100,300,26,36)
        self.vx = self.vy = 0
        self.on_ground = False
        self.facing = 1
        self.hp = MAX_HP
        self.lives = MAX_LIVES
        self.invuln = 0
        self.dash_timer = 0
        self.dash_cd = 0
        self.walk_timer = 0
        self.walk_switch = False
        self.cur_line_x = 0
        self.cur_line_y = 0
        self.dub_jump = False
        self.wing_timer = 0
        self.SOUL = 0
        self.blue_hp = 0
        self.on_wall = False
        self.wall_dir = 0   # -1 = left wall, 1 = right wall
        self.wall_jump_lock = 0


    def respawn(self):
        for _ in range(16):
            particles.append(Particle(self.rect.centerx,self.rect.centery, (0, 0, 0)))
        
        self.rect.topleft = restart_pos
        
            #self.rect.topleft = (100,300)
        self.vx = self.vy = 0
        self.hp = MAX_HP
        self.blue_hp = 0
        self.invuln = 60
        ouch_sound.play()

    def update(self, platforms):
        
        self.on_wall = False
        self.wall_dir = 0
        if transition_alpha > 0: return
        keys = pygame.key.get_pressed()

        if self.dash_timer > 0:
            self.dash_timer -= 1
            self.vx = DASH_SPEED * self.facing
            self.vy = 0
    
            
        else:
            
            if self.wall_jump_lock > 0:
                self.wall_jump_lock -= 1
            else:
                self.vx = 0
                if keys[pygame.K_a]:
                    self.vx = -PLAYER_SPEED
                    self.facing = -1
                if keys[pygame.K_d]:
                    self.vx = PLAYER_SPEED
                    self.facing = 1

        self.rect.x += self.vx
        if player.wall_jump_lock == 0:
            self.collide(platforms, "x")
        
        if self.dash_timer == 0:
            # ---------- WALL SLIDE ----------
            # ---------- GRAVITY / WALL SLIDE ----------
            if self.on_wall and not self.on_ground and self.vy > 0:
                if (
                    (self.wall_dir == -1 and keys[pygame.K_a]) or
                    (self.wall_dir == 1 and keys[pygame.K_d])
                ):
                    # Controlled wall slide
                    self.vy += 0.05#min(self.vy + GRAVITY * 0.3, WALL_SLIDE_SPEED)
                else:
                    self.vy += GRAVITY
            else:
                self.vy += GRAVITY

            # ---------- ALWAYS MOVE & COLLIDE ----------
        self.rect.y += self.vy
        self.collide(platforms, "y")
                
           
        if self.invuln > 0: self.invuln -= 1
        if self.dash_cd > 0: self.dash_cd -= 1

    def collide(self, platforms, axis):
        self.on_ground = False
        

        for p in platforms:
            if self.rect.colliderect(p):

                # ---------- HORIZONTAL ----------
                if axis == "x":
                    if self.vx > 0:
                        self.rect.right = p.left
                        if not self.on_ground and self.vy != 0:
                            self.on_wall = True
                            self.wall_dir = 1
                    if self.vx < 0:
                        self.rect.left = p.right
                        if not self.on_ground  and self.vy != 0:
                            self.on_wall = True
                            self.wall_dir = -1

                # ---------- VERTICAL ----------
                else:
                    if self.vy > 0:
                        self.rect.bottom = p.top
                        self.vy = 0
                        self.on_ground = True
                        self.dub_jump = True
                    if self.vy < 0:
                        self.rect.top = p.bottom
                        self.vy = 0


    def dash(self):
        if self.dash_cd == 0:
            pogo_sound.play()
            self.dash_timer = 10
            self.dash_cd = DASH_CD_MAX
            self.cur_line_x = (self.rect.x + self.rect.w)
            self.cur_line_y = (self.rect.y)
        else:
            self.vy = 0
        
    

    def attack_box(self, down):
        keys = pygame.key.get_pressed()
        if down:
            return pygame.Rect(self.rect.centerx-66, self.rect.bottom, 132, 68)
        if keys[pygame.K_w]:
            return pygame.Rect(self.rect.centerx-48, self.rect.top - 80, 102, 68)
        if self.facing == 1:
            return pygame.Rect(self.rect.right, self.rect.y-6, 72, 48)
        return pygame.Rect(self.rect.left-72, self.rect.y-6, 72, 48)

    def draw(self):
        if self.wing_timer > 0:
            pygame.draw.ellipse(screen, (230,230,230), pygame.Rect(player.rect.left-72, player.rect.y-16, 168, 48))
            self.wing_timer -= 1
        if self.dash_timer > 0:
            
            pygame.draw.line(screen, (230, 230, 240), (self.cur_line_x, self.cur_line_y - 20), (self.rect.x + self.rect.w, self.rect.y-20), 5)
            pygame.draw.line(screen, (230, 230, 240), (self.cur_line_x, self.cur_line_y + 20), (self.rect.x + self.rect.w, self.rect.y+20), 5)
            pygame.draw.line(screen, (230, 230, 240), (self.cur_line_x, self.cur_line_y), (self.rect.x + self.rect.w, self.rect.y), 5)
        if self.invuln % 10 < 5:
            # Create a temporary surface to draw the knight
            surf = pygame.Surface((self.rect.w + 20, self.rect.h + 80), pygame.SRCALPHA)
            ox, oy = 10, 20  # drawing offset inside surface
            
            # --- DRAW KNIGHT (unchanged, just offset) ---
            pygame.draw.ellipse(
                surf, (0,0,0),
                pygame.Rect(ox + 5, oy, self.rect.w - 10, self.rect.h - 4)
            )
            
            
            

            #foot
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.walk_timer += 1
                if self.walk_timer % 5 == 0:
                    self.walk_switch = not self.walk_switch
                if self.on_ground:
                    if self.walk_switch:
                        pygame.draw.circle(surf, (0,0,0),
                            (ox + self.rect.w / 3 + 1, oy + self.rect.h - 4), 4)
                        pygame.draw.circle(surf, (0,0,0),
                            (ox + self.rect.w * (2/3), oy + self.rect.h - 4), 4)
                    else:
                        pygame.draw.circle(surf, (0,0,0),
                            (ox + self.rect.w / 3 - 3, oy + self.rect.h - 4), 4)
                        pygame.draw.circle(surf, (0,0,0),
                            (ox + self.rect.w * (2/3) + 4, oy + self.rect.h - 4), 4)
                else:
                    pygame.draw.circle(surf, (0,0,0),
                        (ox + self.rect.w / 3 + 1, oy + self.rect.h - 4), 4)
                    pygame.draw.circle(surf, (0,0,0),
                        (ox + self.rect.w * (2/3), oy + self.rect.h - 4), 4)

            elif self.on_ground or not self.on_ground:
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w / 3 + 1, oy + self.rect.h - 4), 4)
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w * (2/3), oy + self.rect.h - 4), 4)

            #cloak
            if not self.on_ground:
                pygame.draw.ellipse(
                    surf, (60,60,80),
                    pygame.Rect(ox -10, oy, self.rect.w + 3, self.rect.h * 0.75)
                )

                pygame.draw.ellipse(
                    surf, (30,30,40),
                    pygame.Rect(ox -10, oy, self.rect.w + 3, self.rect.h * 0.75), 2
                )

                pygame.draw.ellipse(
                    surf, (60,60,80),
                    pygame.Rect(ox + self.rect.w - 13, oy, self.rect.w - 5, self.rect.h*0.75)
                )            


                pygame.draw.ellipse(
                    surf, (30,30,40),
                    pygame.Rect(ox + self.rect.w - 13, oy, self.rect.w - 5, self.rect.h * 0.75),2
                )            

            elif self.on_ground:


                pygame.draw.ellipse(
                    surf, (60,60,80),
                    pygame.Rect(ox +1, oy, self.rect.w - 13, self.rect.h - 4)
                )

                pygame.draw.ellipse(
                    surf, (30,30,40),
                    pygame.Rect(ox +1, oy, self.rect.w - 13, self.rect.h - 4), 2
                )

                pygame.draw.ellipse(
                    surf, (60,60,80),
                    pygame.Rect(ox + self.rect.w - 13, oy, self.rect.w - 15, self.rect.h - 4)
                )            


                pygame.draw.ellipse(
                    surf, (30,30,40),
                    pygame.Rect(ox + self.rect.w - 13, oy, self.rect.w - 15, self.rect.h - 4),2
                )            
            
            pygame.draw.circle(surf, (230,230,230),
                (ox + self.rect.w / 2, oy), 15)

            # Horns
            pygame.draw.line(surf, (230,230,230),
                (ox+5, oy-5), (ox, oy-15), 5)
            pygame.draw.line(surf, (230,230,230),
                (ox+5, oy-20), (ox, oy-15), 5)

            pygame.draw.line(surf, (230,230,230),
                (ox + self.rect.w - 5, oy-5),
                (ox + self.rect.w , oy-15), 5)
            pygame.draw.line(surf, (230,230,230),
                (ox + self.rect.w - 5, oy-20),
                (ox + self.rect.w, oy-15), 5)
            if keys[pygame.K_w]:
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w / 4+ 4, oy - 3), 5)
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w * 0.75+4, oy-3), 5)
            elif keys[pygame.K_s]:
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w / 4+ 4, oy+3), 5)
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w * 0.75+4, oy+3), 5)
            else:
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w / 4+ 4, oy), 5)
                pygame.draw.circle(surf, (0,0,0),
                    (ox + self.rect.w * 0.75+4, oy), 5)

            if hit_boxes:
                pygame.draw.rect(
                    surf, (255,255,0),
                    pygame.Rect(ox, oy, self.rect.w, self.rect.h - 4), 5
                )

            # --- FLIP IF FACING LEFT ---
            if self.facing == -1:
                surf = pygame.transform.flip(surf, True, False)

            # Draw to screen
            screen.blit(
                surf,
                (self.rect.x + cam_x - ox, self.rect.y + cam_y - oy)
            )


# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,28,28)
        self.vx = random.choice([-2,2])
        self.vy = 0
        self.on_ground = False
        self.hp = 3

    def update(self, platforms):
        # Horizontal movement with wall collisions
        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0 and self.rect.right > p.left and self.rect.left < p.left:
                    self.rect.right = p.left
                    self.vx *= -1
                if self.vx < 0 and self.rect.left < p.right and self.rect.right > p.right:
                    self.rect.left = p.right
                    self.vx *= -1

        # Gravity + vertical collisions
        self.vy += GRAVITY
        self.rect.y += self.vy
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0 and self.rect.bottom > p.top and self.rect.top < p.top:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                if self.vy < 0 and self.rect.top < p.bottom and self.rect.bottom > p.bottom:
                    self.rect.top = p.bottom
                    self.vy = 0

        # Turn around at platform edges
        if self.on_ground:
            grounded = False
            test_rect = self.rect.move(self.vx,1)
            for p in platforms:
                if test_rect.colliderect(p):
                    grounded = True
                    break
            if not grounded:
                self.vx *= -1

        # Stay inside screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx *= -1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vx *= -1

    def draw(self):
        local = self.rect.move(cam_x, cam_y)
        cx = local.centerx
        cy = local.centery

        # --- SHADOW ---
        pygame.draw.ellipse(
            screen, (30,30,40),
            (local.x + 2, local.bottom - 6, local.w - 4, 8)
        )

        # --- OUTER SHELL ---
        pygame.draw.ellipse(
            screen, (20,20,30),
            local
        )

        # --- INNER BODY ---
        pygame.draw.ellipse(
            screen, (220,220,230),
            (local.x + 3, local.y + 4, local.w - 6, local.h - 8)
        )

        # --- FACE PLATE ---
        pygame.draw.ellipse(
            screen, (200,200,210),
            (local.x + 6, local.y + 8, local.w - 12, local.h - 14)
        )

        # --- EYES ---
        eye_offset = 6 * (1 if self.vx > 0 else -1)

        for ex in (-6, 6):
            pygame.draw.circle(
                screen, (20,20,20),
                (cx + ex + eye_offset, cy - 2),
                5
            )
            pygame.draw.circle(
                screen, (255,170,0),
                (cx + ex + eye_offset, cy - 2),
                3
            )

        # --- MANDIBLES / TEETH ---
        pygame.draw.line(
            screen, (30,30,30),
            (cx - 4, local.bottom - 8),
            (cx - 8, local.bottom),
            2
        )
        pygame.draw.line(
            screen, (30,30,30),
            (cx + 4, local.bottom - 8),
            (cx + 8, local.bottom),
            2
        )
        #pygame.draw.line(screen, (230,230,230), (self.rect.x+5, self.rect.y+5), (self.rect.x-5, self.rect.y-5), 4)
        if hit_boxes:
            pygame.draw.rect(screen,(230,170,0), self.rect.move(cam_x,cam_y), 5)


def draw_platform_decor(rect):
    """
    Deep scalable decor with bushes and rocks.
    Everything derived from rect math (iteration-style).
    """

    r = rect.move(cam_x, cam_y)

    dark   = CURRENT_PALETTE["dark"]
    mid    = CURRENT_PALETTE["mid"]
    light  = CURRENT_PALETTE["light"]
    accent  = CURRENT_PALETTE["accent"]

    w, h = r.w, r.h

    

    # =========================================================
    #  BUSHES 
    # =========================================================
    if w >= 40 and h >= 16:
        bush_w = w * 0.25
        bush_h = h * 0.3

        # left bush
        pygame.draw.ellipse(
            screen, light,
            (
                r.x + w * 0.15,
                r.y - bush_h * 0.6,
                bush_w,
                bush_h
            )
        )
        pygame.draw.ellipse(
            screen, (0,0,0),
            (
                r.x + w * 0.15,
                r.y - bush_h * 0.6,
                bush_w,
                bush_h
            ), 5
        )

        # right bush
        pygame.draw.ellipse(
            screen, light,
            (
                r.x + w * 0.55,
                r.y - bush_h * 0.5,
                bush_w,
                bush_h
            )
        )
        pygame.draw.ellipse(
            screen, (0,0,0),
            (
                r.x + w * 0.55,
                r.y - bush_h * 0.5,
                bush_w,
                bush_h
            ),5
        )

        # bush shadow
        pygame.draw.ellipse(
            screen, dark,
            (
                r.x + w * 0.18,
                r.y - bush_h * 0.15,
                bush_w * 0.9,
                bush_h * 0.3
            )
        )
        pygame.draw.ellipse(
            screen, (0,0,0),
            (
                r.x + w * 0.18,
                r.y - bush_h * 0.15,
                bush_w * 0.9,
                bush_h * 0.3
            ), 5
        )

    # =========================================================
    # 🪨 ROCK PROTRUSIONS (UNDERSIDE / SIDES)
    # =========================================================
    if h >= 20 and w > 150:
        rock_w = w * 0.2
        rock_h = h * 0.25

        # center hanging rock
        pygame.draw.rect(
            screen, dark,
            (
                r.x + w * 0.4,
                r.bottom - rock_h * 0.2,
                rock_w,
                rock_h
            ),
            border_radius=4
        )

        # inner highlight
        pygame.draw.rect(
            screen, mid,
            (
                r.x + w * 0.43,
                r.bottom,
                rock_w * 0.7,
                rock_h * 0.7
            ),
            border_radius=3
        )

    # ---------- SIDE ROCK (WALLS) ----------
    if h > w:
        pygame.draw.rect(
            screen, dark,
            (
                r.x,
                r.y + h * 0.3,
                w * 0.3,
                h * 0.4
            ),
            border_radius=4
        )
    # ---------- DEPTH SHADING (CONTAINED & VISIBLE) ----------

    if False:
        # Fixed pixel insets (safe for small platforms)
        accent_inset = 0
        dark_inset   = 8
        mid_inset    = 16
        core_inset   = 36

        # Accent base (fills rect)
        pygame.draw.rect(
            screen,
            accent,
            r,
            border_radius=8
        )

        # Dark layer
        if w > dark_inset * 2 and h > dark_inset * 2:
            pygame.draw.rect(
                screen,
                mid,
                r.inflate(-dark_inset * 2, -dark_inset * 2),
                border_radius=7
            )
        
        # Mid layer
        if w > mid_inset * 2 and h > mid_inset * 2:
            pygame.draw.rect(
                screen,
                dark,
                r.inflate(-mid_inset * 2, -mid_inset * 2),
                border_radius=6
            )

        # Core (deep interior)
        if w > core_inset * 2 and h > core_inset * 2:
            pygame.draw.rect(
                screen,
                (10, 10, 14),
                r.inflate(-core_inset * 2, -core_inset * 2),
                border_radius=5
            )

            if CURRENT_PALETTE == PALETTES["greenpath"]:
                # ---------- TOP LIGHT ----------
                rim_h = max(2, min(h * 0.25, 8))
                pygame.draw.rect(
                    screen, dark,
                    (r.x + w * 0.05, r.y, w * 0.9, rim_h),
                    border_radius=8
                )
            
def uniform(rect, uni):
    """
    Deep scalable decor with bushes and rocks.
    Everything derived from rect math (iteration-style).
    """

    r = rect.move(cam_x, cam_y)

    dark   = CURRENT_PALETTE["dark"]
    mid    = CURRENT_PALETTE["mid"]
    light  = CURRENT_PALETTE["light"]
    accent  = CURRENT_PALETTE["accent"]

    w, h = r.w, r.h

    # ---------- DEPTH SHADING (CONTAINED & VISIBLE) ----------

    # Fixed pixel insets (safe for small platforms)
    accent_inset = 0
    dark_inset   = 8
    mid_inset    = 16
    core_inset   = 36
    if uni == 1:
        # Accent base (fills rect)
        pygame.draw.rect(
            screen,
            accent,
            r,
            border_radius=8
        )
    if uni == 2:
        # Dark layer
        if w > dark_inset * 2 and h > dark_inset * 2:
            pygame.draw.rect(
                screen,
                mid,
                r.inflate(-dark_inset * 2, -dark_inset * 2),
                border_radius=7
            )
    if uni == 3:
        # Mid layer
        if w > mid_inset * 2 and h > mid_inset * 2:
            pygame.draw.rect(
                screen,
                dark,
                r.inflate(-mid_inset * 2, -mid_inset * 2),
                border_radius=6
            )
    if uni == 4:
        # Core (deep interior)
        if w > core_inset * 2 and h > core_inset * 2:
            pygame.draw.rect(
                screen,
                (10, 10, 14),
                r.inflate(-core_inset * 2, -core_inset * 2),
                border_radius=5
            )

            if CURRENT_PALETTE == PALETTES["greenpath"]:
                # ---------- TOP LIGHT ----------
                rim_h = max(2, min(h * 0.25, 8))
                pygame.draw.rect(
                    screen, dark,
                    (r.x + w * 0.05, r.y, w * 0.9, rim_h),
                    border_radius=8
                )
            


class Bench:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 50)

    def interact(self, index):
        global restart_room, restart_pos

        if index == room_index:
            px, py = player.rect.center

            if self.rect.collidepoint(px, py):
                if restart_pos != (self.rect.centerx, self.rect.y) or player.hp < MAX_HP:
                     loc_blue = player.blue_hp
                     saw_sound.play()
                     restart_room = room_index
                     restart_pos = (self.rect.centerx, self.rect.y)
                     player.respawn()
                     player.blue_hp = loc_blue

               

    def draw(self, index):
        if index == room_index:
            local = self.rect.move(cam_x, cam_y)
            # bars

            pygame.draw.rect(screen, (100, 100, 110), pygame.Rect(local.x+12, local.y + 5,76, 15))
            pygame.draw.rect(screen, (150, 150, 170), pygame.Rect(local.x+12, local.y,76, 7))
            
            pygame.draw.rect(screen, (100,100,110), pygame.Rect(local.x + 12, local.y, 10, local.h))
            pygame.draw.rect(screen, (150,150,170), pygame.Rect(local.x + 17, local.y, 5, local.h))

            pygame.draw.rect(screen, (100,100,110), pygame.Rect(local.x - 17+local.w, local.y, 10, local.h))
            pygame.draw.rect(screen, (150,150,170), pygame.Rect(local.x - 12+local.w, local.y, 5, local.h))

            
            
            # seat
            pygame.draw.rect(screen, (150, 150, 170), pygame.Rect(local.x, local.y + local.h/2,100, 10))
            pygame.draw.rect(screen, (100, 100, 110), pygame.Rect(local.x, local.y + local.h/2 + 5,100, 5))

            
            if hit_boxes:
                pygame.draw.rect(screen, (255, 255,255), local, 5)

# ---------------- SAW BLADE ----------------
class Saw:
    def __init__(self, x, y, radius=16, vx=0, min_x=None, max_x=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.min_x = min_x
        self.max_x = max_x

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def update(self):
        if self.vx != 0:
            self.x += self.vx
            if self.min_x is not None and self.x < self.min_x:
                self.x = self.min_x
                self.vx *= -1
            if self.max_x is not None and self.x > self.max_x:
                self.x = self.max_x
                self.vx *= -1

    def draw(self):
        # Outer blade
        pygame.draw.circle(
            screen, (160,160,160),
            (int(self.x + cam_x), int(self.y + cam_y)),
            self.radius
        )
        # Inner hub
        pygame.draw.circle(
            screen, (80,80,80),
            (int(self.x + cam_x), int(self.y + cam_y)),
            self.radius // 2
        )
        # Teeth
        for i in range(8):
            ang = i * 45
            dx = int(self.radius * 0.9 * pygame.math.Vector2(1,0).rotate(ang).x)
            dy = int(self.radius * 0.9 * pygame.math.Vector2(1,0).rotate(ang).y)
            pygame.draw.circle(
                screen, (210,210,210),
                (int(self.x + cam_x + dx), int(self.y + cam_y + dy)),
                self.radius/4
            )

        if hit_boxes:
            if self.min_x and self.max_x:
                pygame.draw.line(screen, (255,0,255), (self.min_x, self.y), (self.max_x, self.y), 5)
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.x - self.radius, self.y-self.radius, self.radius*2,self.radius*2), 5)

class LifebloodCocoon:
    def __init__(self, x, y, amount=2):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.amount = amount
        self.broken = False

    def break_open(self, player):
        if self.broken:
            return
        self.broken = True
        hit_sound.play()
        MAX_BLUE_HP = 4
        player.blue_hp = player.blue_hp + self.amount
        for _ in range(12):
            particles.append(
                Particle(
                    self.rect.centerx,
                    self.rect.centery,
                    (80, 180, 255)
                )
            )

    def draw(self):
        if self.broken:
            return

        r = self.rect.move(cam_x, cam_y)

        # Outer shell
        pygame.draw.ellipse(screen, (80, 160, 220), r)
        # Inner glow
        pygame.draw.ellipse(
            screen, (180, 230, 255),
            r.inflate(-10, -10)
        )
        # Outline
        pygame.draw.ellipse(screen, (30, 80, 120), r, 3)

        if hit_boxes:
            pygame.draw.rect(screen, (0, 255, 255), r, 5)



# ---------------- ROOMS ----------------
def enemies(y, amnt = 7):
    local = [Enemy(150+i*120,y) for i in range(amnt)]
    local.append(Enemy(450, -50))
    return local

rooms = [
    # Room 1: Some walls/platforms to test edge collisions
    {"platforms":[pygame.Rect(0,380,1000,250),
            pygame.Rect(350, 300, 300, 400),
            pygame.Rect(350, 100, 200, 400),
            pygame.Rect(0,0, 1000, 25),
            pygame.Rect(100, 300, 75, 25),
            pygame.Rect(0, 225, 75, 25),
            pygame.Rect(100, 150, 75, 25),
            pygame.Rect(0,0,15, 500),
            pygame.Rect(900,0,100,300)],
             
     "enemies":enemies(50, 10),
     "saws": [
            Saw(750, 260, radius = 32),
            Saw(630, 170, radius = 32)

            
        ]
     },
    # Room 2: Custom designed platform room
    {"platforms":[
        pygame.Rect(0,380,200, 200),
        pygame.Rect(850, 150, 150, 250),
        pygame.Rect(200, 160, 10, 350),
        pygame.Rect(0,0,140, 300),
        pygame.Rect(900,100,100, 500),
        pygame.Rect(0,0, 1000, 25),
        pygame.Rect(300,0, 300, 300)
        
    ],"enemies":[],
     "saws": [
            #Saw(450, 450, vx=1, min_x=400, max_x=650),
            Saw(450, 420, radius = 48,vx=1, min_x=450, max_x=650),
            #Saw(450, 390, vx=1, min_x=400, max_x=650),
            Saw(205, 160),
            Saw(800, 170),
            Saw(750, 380),
            Saw(205, 380, radius = 24)
        ]},
    {"platforms":[
        pygame.Rect(0, 100, 15, 500),
        pygame.Rect(0, 400, 1000, 150),
        pygame.Rect(0, 0, 1000, 25),
        pygame.Rect(600, 0, 200, 300),
        pygame.Rect(900, 100, 100, 400),
        pygame.Rect(125, 175, 275, 150),
        pygame.Rect(375, 75, 25, 125),
        pygame.Rect(100, 0, 100, 350),
    ],"enemies":enemies(300, 9),
     "saws": [
            #Saw(460, 100, radius = 32),
            
            Saw(760, 400, radius = 32),
            Saw(460, 300, radius = 32),
            Saw(885, 250, radius = 8),
        ]},
    {"platforms":[
    
        pygame.Rect(0, 100, 15, 500),
        pygame.Rect(0, 400, 150, 150),
        pygame.Rect(450, 100, 20, 300),
        pygame.Rect(0,0, 1000, 25),
        pygame.Rect(440, 100, 40, 20),
        pygame.Rect(100, 0, 200, 300),
        pygame.Rect(600, 0, 200, 300),
       # pygame.Rect(0,0, 900, 25)
        pygame.Rect(900,0,100, 300),
        
    ],"enemies":[],
     "saws": [
            #Saw(460, 100, radius = 32),
            Saw(460, 400, radius = 64),
            Saw(760, 400, radius = 32),
            Saw(460, 250, vx=3, min_x=350, max_x=550),
            Saw(100, 250)
        ]},
    {"platforms":[
    
        pygame.Rect(0, 450, 150, 50),
        
        pygame.Rect(0,0, 1000, 25),


        #pygame.Rect(350,200, 100, 25),
        #pygame.Rect(200,350, 100, 25),
        #pygame.Rect(700,150, 100, 25),
        pygame.Rect(900,100,100, 500),
        pygame.Rect(315,150,20, 500),
        pygame.Rect(390,0,20, 250),
        pygame.Rect(0,0,150, 300),
       
        
        
    ],"enemies":[],
     "saws": [
            Saw(200, 350, vx = 2, min_x = 200, max_x = 300, radius = 32),
            Saw(325, 150),
            Saw(325, 500, radius = 64),
            Saw(425, 350),
            Saw(700, 250, vx = 2, min_x = 450, max_x = 800, radius = 32),
            Saw(775, 250, vx = 2, min_x = 450, max_x = 800, radius = 32),
        ]},
    {"platforms":[
        
        pygame.Rect(0,0, 1000, 25),
        
        pygame.Rect(0,100,50, 500),
        pygame.Rect(850,100,150, 500),
       # pygame.Rect(0,0, 900, 25)
        pygame.Rect(0, 400, 150, 200),
        
        
    ],"enemies":[],
     "saws": [
         

         Saw(100, 200, vx= 4, radius = 48, min_x = 100, max_x = 800),
         Saw(900, 300, vx= 4, radius = 48, min_x = 200, max_x = 900),

         

         
         Saw(200, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(300, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(400, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(500, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(600, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(700, 450, radius = 48, min_x = 100, max_x = 850),
         Saw(800, 450, radius = 48, min_x = 100, max_x = 850),
        ]},
    {"platforms":[
        
        pygame.Rect(0,0, 1000, 25),
        
        pygame.Rect(150,350,700, 50),
        pygame.Rect(300,150,700, 50),
        pygame.Rect(0,100,50, 500),
        pygame.Rect(150,0,50, 400),
        pygame.Rect(950,100,50, 500),
       
        
        
    ],"enemies":[],
     "saws": [
         

         
         Saw(800, 0, vx= 4, radius = 64, min_x = 250, max_x = 800),
         Saw(800, 300, vx= 4, radius = 48, min_x = 250, max_x = 800),
         Saw(100, 175, vx= 4, radius = 94, min_x = 250, max_x = 800),
         Saw(50, 250, radius = 32),
         
         Saw(50, 500, radius = 48),

         Saw(250, 500),
         Saw(500, 500),
         Saw(750, 500),
         Saw(350, 400),
         Saw(650, 400),
        
        ]},
    {
      "platforms": [
        pygame.Rect(0, 0, 1000, 25),
        pygame.Rect(0, 100, 50, 500),
        pygame.Rect(950, 100, 50, 500),
        pygame.Rect(125, 0, 50, 200),
        pygame.Rect(125, 150, 100, 50),
        pygame.Rect(175, 150, 50, 275),
        pygame.Rect(0, 300, 125, 25),
        pygame.Rect(100, 400, 100, 25),
        pygame.Rect(500, 75, 50, 425),
        pygame.Rect(525, 475, 100, 25),
        pygame.Rect(625, 125, 50, 175),
        pygame.Rect(750, 0, 50, 425),
        pygame.Rect(850, 475, 125, 25),
        pygame.Rect(500, 375, 175, 50),
        pygame.Rect(900, 375, 25, 25),
        pygame.Rect(800, 275, 25, 25),
        pygame.Rect(900, 175, 25, 25),
        pygame.Rect(800, 75, 25, 25),
        pygame.Rect(25, 475, 100, 25),
        pygame.Rect(200, 475, 25, 25),
        pygame.Rect(300, 475, 25, 25),
        pygame.Rect(400, 475, 25, 25),
        pygame.Rect(300, 0, 50, 275),
        pygame.Rect(450, 75, 100, 175),
        pygame.Rect(175, 325, 250, 100),
      ],
      "enemies": [],
      "saws": [
        Saw(50, 275, radius=48, vx=0, min_x=None, max_x=None),
        Saw(175, 200, radius=48, vx=0, min_x=None, max_x=None),
        Saw(50, 200, radius=32, vx=0, min_x=None, max_x=None),
        Saw(50, 150, radius=24, vx=0, min_x=None, max_x=None),
        Saw(75, 100, radius=16, vx=0, min_x=None, max_x=None),
        Saw(175, 300, radius=16, vx=0, min_x=None, max_x=None),
        Saw(175, 400, radius=16, vx=0, min_x=None, max_x=None),
        Saw(200, 350, radius=32, vx=0, min_x=None, max_x=None),
        Saw(25, 400, radius=40, vx=0, min_x=None, max_x=None),
        Saw(50, 475, radius=8, vx=0, min_x=None, max_x=None),
        Saw(225, 275, radius=16, vx=0, min_x=None, max_x=None),
        Saw(300, 250, radius=16, vx=0, min_x=None, max_x=None),
        Saw(225, 200, radius=16, vx=0, min_x=None, max_x=None),
        Saw(300, 175, radius=16, vx=0, min_x=None, max_x=None),
        Saw(225, 125, radius=16, vx=0, min_x=None, max_x=None),
        Saw(300, 75, radius=16, vx=0, min_x=None, max_x=None),
        Saw(250, 25, radius=32, vx=0, min_x=None, max_x=None),
        Saw(200, 475, radius=8, vx=0, min_x=None, max_x=None),
        Saw(300, 475, radius=8, vx=0, min_x=None, max_x=None),
        Saw(400, 475, radius=8, vx=0, min_x=None, max_x=None),
        Saw(375, 225, radius=24, vx=0, min_x=None, max_x=None),
        Saw(425, 100, radius=24, vx=0, min_x=None, max_x=None),
        Saw(350, 175, radius=8, vx=0, min_x=None, max_x=None),
        Saw(350, 100, radius=8, vx=0, min_x=None, max_x=None),
        Saw(450, 250, radius=8, vx=0, min_x=None, max_x=None),
        Saw(450, 150, radius=8, vx=0, min_x=None, max_x=None),
        Saw(550, 125, radius=24, vx=0, min_x=None, max_x=None),
        Saw(550, 175, radius=24, vx=0, min_x=None, max_x=None),
        Saw(550, 225, radius=24, vx=0, min_x=None, max_x=None),
        Saw(550, 275, radius=24, vx=0, min_x=None, max_x=None),
        Saw(550, 325, radius=24, vx=0, min_x=None, max_x=None),
        Saw(550, 400, radius=40, vx=0, min_x=None, max_x=None),
        Saw(625, 125, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 225, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 150, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 175, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 200, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 250, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 275, radius=8, vx=0, min_x=None, max_x=None),
        Saw(600, 375, radius=8, vx=0, min_x=None, max_x=None),
        Saw(625, 375, radius=8, vx=0, min_x=None, max_x=None),
        Saw(675, 200, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 275, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 225, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 250, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 175, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 125, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 125, radius=16, vx=0, min_x=None, max_x=None),
        Saw(675, 150, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 125, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 150, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 175, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 200, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 225, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 250, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 275, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 300, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 325, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 350, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 375, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 400, radius=16, vx=0, min_x=None, max_x=None),
        Saw(750, 425, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 250, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 275, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 300, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 325, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 400, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 375, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 350, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 425, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 200, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 175, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 150, radius=16, vx=0, min_x=None, max_x=None),
        Saw(925, 225, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 125, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 100, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 75, radius=16, vx=0, min_x=None, max_x=None),
        Saw(800, 50, radius=16, vx=0, min_x=None, max_x=None),
        Saw(950, 275, radius=32, vx=0, min_x=None, max_x=None),
        Saw(800, 175, radius=32, vx=0, min_x=None, max_x=None),
        Saw(800, 375, radius=32, vx=0, min_x=None, max_x=None),
        Saw(925, 475, radius=32, vx=0, min_x=None, max_x=None),
      ]
    }

]
rooms[0].setdefault("cocoons", []).append(
    LifebloodCocoon(120, 260, amount=4)
)

rooms[2].setdefault("cocoons", []).append(
    LifebloodCocoon(275, 100, amount=2)
)

rooms[4].setdefault("cocoons", []).append(
    LifebloodCocoon(60, 410, amount=3)
)




benches = [{"ben":Bench(875, 50), "index":5}, {"ben":Bench(25, 330), "index":1}]

room_index = 0
player = Player()
particles = []

# ---------------- MAIN LOOP ----------------
while True:
    clock.tick(60)
    

    #screen.fill((60,60,70))
    draw_hk_background()
    for p in rooms[room_index]["platforms"]:
        draw_platform_decor(p)
    for i in range(4):
        for p in rooms[room_index]["platforms"]:
            uniform(p, i+1)
        
            if hit_boxes:
                pygame.draw.rect(screen, (0,0,255), p.move(cam_x, cam_y), 5)
    # -------- SCREEN SHAKE / HIT PAUSE --------
    if hit_pause > 0:
        hit_pause -= 1
    else:
        if shake > 0:
            shake -= 1
            cam_x = random.randint(-6,6)
            cam_y = random.randint(-6,6)
        else:
            cam_x = cam_y = 0
    if room_lock > 0:
        room_lock -= 1

    for e in pygame.event.get():
        event = e
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            

            if event.key == pygame.K_TAB:
                EDITOR_MODE = not EDITOR_MODE
                editor_rects = rooms[room_index]["platforms"]
                editor_saws  = rooms[room_index]["saws"]
                print(room_index)

            if EDITOR_MODE:
                if event.key == pygame.K_1:
                    EDITOR_TOOL = "platform"
                if event.key == pygame.K_2:
                    EDITOR_TOOL = "saw"
                if event.key == pygame.K_p:
                    export_room(rooms[room_index])
                if event.key == pygame.K_UP:
                    editor_radius += 8
                if event.key == pygame.K_DOWN:
                    editor_radius -= 8
            
            if game_state == STATE_MENU:
                if event.key == pygame.K_RETURN:
                    game_state = STATE_PLAYING
                elif event.key == pygame.K_c:
                    game_state = STATE_CONTROLS
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

            elif game_state == STATE_CONTROLS:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU
                    player.blue_hp = 67

            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_PAUSE

            elif game_state == STATE_PAUSE:
                if event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU
                if event.key == pygame.K_SPACE:
                    game_state = STATE_PLAYING
                        

            # ---------- WALL JUMP ----------
            if not e_down and player.on_wall and not player.on_ground and keys[pygame.K_SPACE] or not e_down and player.on_wall and not player.on_ground and keys[pygame.K_e]:
                if not e_down:
                    player.vy = -WALL_JUMP_Y
                    player.vx = -player.wall_dir * WALL_JUMP_X
                    #player.dub_jump = True
                    player.wall_jump_lock = 6
                    player.on_wall = False
                    jump_sound.play()
                    pogo_sound.play()
            elif not e_down and (keys[pygame.K_e] or keys[pygame.K_SPACE]) and player.on_ground or player.dub_jump and (keys[pygame.K_e] or keys[pygame.K_SPACE]):
                if not e_down:
                    if player.on_ground:
                        player.dub_jump = True
                        jump_sound.play()
                    elif not player.on_ground and player.dash_timer == 0:
                        player.dub_jump = False
                        player.wing_timer = 10
                        pogo_sound.play()
                    player.vy = -JUMP_POWER
            if e.key == pygame.K_k: player.dash()
                
            if e.key == pygame.K_h: hit_boxes = not hit_boxes
            if e.key == pygame.K_j:
                down = pygame.key.get_pressed()[pygame.K_s]
                atk = player.attack_box(down)
                pygame.draw.ellipse(screen, (255,255,255), atk)
                for en in rooms[room_index]["enemies"][:]:
                    if atk.colliderect(en.rect):
                        
                        player.dub_jump = True
                        en.hp -= 1
                        hit_pause = 6
                        shake = 10
                        player.SOUL += 7
                        if player.SOUL > 60:
                            player.SOUL = 60
                        hit_sound.play()
                        if down and not player.on_ground:
                            player.vy = -POGO_BOOST
                            for _ in range(12):
                                particles.append(Particle(en.rect.centerx,en.rect.bottom,(230,230,230)))
                            
                        if en.hp <= 0:
                            rooms[room_index]["enemies"].remove(en)
                            
                            
                            #if MAX_HP < 8:
                             #   MAX_HP += 1
                            #else:
                             #   player.hp += 1
                            for _ in range(16):
                                particles.append(Particle(en.rect.centerx,en.rect.centery, (255, 170, 0)))
                            
                        if not down and en.hp > 0:
                            for _ in range(16):
                                particles.append(Particle(en.rect.centerx,en.rect.centery, (255, 170, 0)))
                for saw in rooms[room_index]["saws"]:
                    # POGO check (downward attack)
                    down = pygame.key.get_pressed()[pygame.K_s]
                    if down and player.attack_box(True).colliderect(saw.rect) and not player.on_ground:
                        player.dub_jump = True
                        player.vy = -POGO_BOOST
                        saw_sound.play()
                        hit_pause = 5
                        shake = 10
                    
                        player.SOUL += 1
                        if player.SOUL > 60:
                            player.SOUL = 60
                        for _ in range(4):
                            particles.append(
                                Particle(saw.x, saw.y, (80,80,80))
                            )
                        for _ in range(4):
                            particles.append(
                                Particle(saw.x, saw.y, (160,160,160))
                            )
                        for _ in range(4):
                            particles.append(
                                Particle(saw.x, saw.y, (210,210,210))
                            )
                for cocoon in rooms[room_index].get("cocoons", []):
                    if not cocoon.broken and atk.colliderect(cocoon.rect):
                        cocoon.break_open(player)
        if EDITOR_MODE:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                mx -= cam_x; my -= cam_y

                # ---------- PLATFORM ----------
                if EDITOR_TOOL == "platform":
                    if event.button == 1:
                        editor_start = (mx,my)
                    if event.button == 3:
                        for r in editor_rects[:]:
                            if r.collidepoint(mx,my):
                                editor_rects.remove(r)

                # ---------- SAW ----------
                if EDITOR_TOOL == "saw":
                    if event.button == 1:
                        editor_saws.append(Saw(snap(mx), snap(my), radius = editor_radius))
                    if event.button == 3:
                        for s in editor_saws[:]:
                            if s.rect.collidepoint(mx,my):
                                editor_saws.remove(s)

            if event.type == pygame.MOUSEBUTTONUP:
                if EDITOR_TOOL == "platform" and event.button == 1 and editor_start:
                    mx,my = pygame.mouse.get_pos()
                    mx -= cam_x; my -= cam_y
                    r = rect_from_points(editor_start[0],editor_start[1],mx,my)
                    if r.w>0 and r.h>0:
                        editor_rects.append(r)
                    editor_start = None


    if game_state == STATE_MENU:
        draw_menu()
        pygame.display.flip()
        continue

    if game_state == STATE_CONTROLS:
        draw_controls()
        pygame.display.flip()
        continue

    if game_state == STATE_PAUSE:
        draw_pause()
        pygame.display.flip()
        continue
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        for b in benches: b["ben"].interact(b["index"])
    if keys[pygame.K_e] or keys[pygame.K_SPACE]:
        e_down = True
    else:
        e_down = False
    only_focus = (
    keys[pygame.K_l] and
        not (
            keys[pygame.K_a] or
            keys[pygame.K_d] or
            keys[pygame.K_w] or
            keys[pygame.K_s] or
            keys[pygame.K_SPACE] or
            keys[pygame.K_k] or
            keys[pygame.K_j] or
            keys[pygame.K_e]
        )
    )




    if only_focus and player.on_ground:
        FOCUS_TIMER +=1
    else:
        FOCUS_TIMER = 0

    if FOCUS_TIMER > 25 and player.hp < MAX_HP and player.SOUL >= 20:
        live_sound.play()
        player.hp += 1
        FOCUS_TIMER = 0
        player.SOUL -= 20
    for saw in rooms[room_index]["saws"]:
        # Player damage
        if player.rect.colliderect(saw.rect) and player.invuln == 0:
            ouch_sound.play()
            if player.blue_hp > 0:
                player.blue_hp -= 1
            else:
                player.hp -= 1
            player.invuln = 60
            hit_pause = 6
            shake = 14
    if player.rect.y > 600:# or player.rect.y < -30:
        player.rect.topleft = (100,300)
        player.vx = player.vy = 0
        if player.blue_hp > 0:
            player.blue_hp -= 1
        else:
            player.hp -= 1
        player.invuln = 60
        hit_pause = 6
        shake = 14
        
    player.update(rooms[room_index]["platforms"])

    for en in rooms[room_index]["enemies"]:
        en.update(rooms[room_index]["platforms"])
        if player.rect.colliderect(en.rect) and player.invuln == 0:
            if player.blue_hp > 0:
                player.blue_hp -= 1
            else:
                player.hp -= 1
            ouch_sound.play()
            player.invuln = 60
            hit_pause = 6
            shake = 12
    for saw in rooms[room_index]["saws"]:
        saw.update()

    # -------- DEATH / RESPAWN --------
    if player.hp <= 0:
        player.lives -= 1
        player.SOUL = 0
        shake = 20
        for i in range(len(rooms)):
            for coc in rooms[i].get("cocoons", []):
                coc.broken = False
        for i, r in enumerate(rooms):
            if r["enemies"] != []:
                r["enemies"] = enemies(50, amnt = 10)
        if player.hp <= 0:
            player.hp = MAX_HP
            room_index = restart_room
            #for i, r in enumerate(rooms):
                
             #   r["enemies"] = enemies(250, amnt = 10)
        player.respawn()
        

    # -------- ROOM TRANSITION --------
    if transition_dir != 0:
        transition_alpha += transition_dir * 20
        if transition_alpha >= 255:

            room_index = next_room
            if player.rect.left < 0:
                player.rect.x = WIDTH -30
            if player.rect.right > WIDTH:
                player.rect.x = 1
            transition_dir = -transition_dir
            room_lock = 15
        if transition_alpha <= 0:
            transition_alpha = 0
            transition_dir = 0

    if transition_dir == 0 and room_lock == 0:
        if player.rect.right > WIDTH:
            
            next_room = room_index + 1#min(room_index+1,len(rooms)-1)
            transition_dir = 1
            
            
        if player.rect.left < 0:
            
            next_room = room_index - 1#max(room_index-1,0)
            
            transition_dir = 1
        

    # ---------------- DRAW ----------------

    
    for cocoon in rooms[room_index].get("cocoons", []):
        cocoon.draw()

    for en in rooms[room_index]["enemies"]: en.draw()
    for saw in rooms[room_index]["saws"]:
        saw.draw()
    
    if EDITOR_MODE:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # grid
        for x in range(0, WIDTH, GRID):
            pygame.draw.line(screen, (40,40,60), (x,0), (x,HEIGHT))
        for y in range(0, HEIGHT, GRID):
            pygame.draw.line(screen, (40,40,60), (0,y), (WIDTH,y))

        # preview rect
        if editor_start:
            mx, my = pygame.mouse.get_pos()
            preview = rect_from_points(
                editor_start[0], editor_start[1],
                mx - cam_x, my - cam_y
            )
            pygame.draw.rect(
                screen, (0,255,0),
                preview.move(cam_x, cam_y), 2
            )

        label = FONT_SMALL.render(f"EDITOR MODE (TAB) | LMB draw | RMB delete | Current Tool: {EDITOR_TOOL} | Saw Radius: {editor_radius} | P export", True, (220,220,220))
        screen.blit(label, (20, 20))

    for b in benches: b["ben"].draw(b["index"])
    player.draw()
    


    

    if FOCUS_TIMER > 0 and player.hp != MAX_HP and player.SOUL >= 20:
        pygame.draw.circle(screen, ( 255,255,255), (player.rect.centerx, player.rect.centery), 100 + (FOCUS_TIMER *-4), 10)
    if hit_boxes:
        down = pygame.key.get_pressed()[pygame.K_s]
        pygame.draw.rect(screen, (255,0,0), player.attack_box(down), 5)

    for pt in particles[:]:
        pt.update(); pt.draw()
        if pt.life<=0: particles.remove(pt)

    if not EDITOR_MODE:
        # ---------------- UI ----------------
        pygame.draw.circle(screen, (0,0,0), (50, 50), 41)
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(20,(player.SOUL * -1) + 80, 60, player.SOUL))
        pygame.draw.circle(screen, (120,120,120), (50, 50), 41, 11)
        pygame.draw.circle(screen, (0,0,0), (50, 50), 43, 3)
        pygame.draw.circle(screen, (0,0,0), (35, 50), 10)
        pygame.draw.circle(screen, (0,0,0), (65, 50), 10)

        for i in range(MAX_HP + player.blue_hp):
            if i <= 4:
                pygame.draw.circle(screen, (255,255,255) if i<player.hp else (120,120,120), (120+i*30,30),10)
                pygame.draw.circle(screen, (255,255,255) if i<player.hp else (120,120,120), (120+i*30,35),9)
            else:
                pygame.draw.circle(screen, (60, 150, 225), (120+i*30,30),10)
                pygame.draw.circle(screen, (60, 150, 225), (120+i*30,35),9)
            pygame.draw.circle(screen, (0, 0, 0), (125+i*30,30),4)
            pygame.draw.circle(screen, (0, 0, 0), (115+i*30,30),4)
        #for i in range(MAX_LIVES):
         #   pygame.draw.rect(screen, (200,200,255) if i<player.lives else (70,70,90), (90+i*20,55,14,10))

        pygame.draw.rect(screen,(120,120,120),(100,50,100,10))
        fill = 1-(player.dash_cd/DASH_CD_MAX)
        pygame.draw.rect(screen,(230,230,230),(100,50,100*fill,10))

    if transition_alpha > 0:
        fade = pygame.Surface((WIDTH,HEIGHT))
        fade.fill((0,0,0))
        fade.set_alpha(transition_alpha)
        screen.blit(fade,(0,0))

    pygame.display.flip()
