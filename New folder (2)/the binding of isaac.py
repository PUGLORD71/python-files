# =========================================================
# ISAAC FLASH STYLE PROTOTYPE
# ROCKS + REAL DOORS + ENEMY COLLISION
# =========================================================

import pygame
import random
import math

pygame.init()

# =========================================================
# WINDOW
# =========================================================
#WIDTH, HEIGHT = 1000, 680
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Binding Of Isaac")
clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================
BLACK = (20, 20, 20)
GRAY = (60, 60, 60)
LIGHT = (180, 180, 180)
WHITE = (240, 240, 240)

RED = (220, 60, 60)
GREEN = (80, 200, 100)
BLUE = (80, 140, 255)
YELLOW = (255, 220, 80)
PURPLE = (170, 80, 255)

MAP_GRAY = (90, 90, 90)
BROWN = (120, 95, 70)

# =========================================================
# WINDOW
# =========================================================
ROOM_W = 960
ROOM_H = 540

ROOM_X = (WIDTH - ROOM_W) // 2
ROOM_Y = (HEIGHT - ROOM_H) // 2

# =========================================================
# DOORS
# =========================================================
TOP_DOOR = pygame.Rect(WIDTH//2 - 45, ROOM_Y, 90, 20)
BOTTOM_DOOR = pygame.Rect(WIDTH//2 - 45, ROOM_Y + ROOM_H-20, 90, 20)
LEFT_DOOR = pygame.Rect(ROOM_X, HEIGHT//2 - 45, 20, 90)
RIGHT_DOOR = pygame.Rect(ROOM_X + ROOM_W-20, HEIGHT//2 - 45, 20, 90)

# =========================================================
# WALLS
# =========================================================
TOP_WALL_LEFT = pygame.Rect(ROOM_X, ROOM_Y, ROOM_W//2 - 50, 20)
TOP_WALL_RIGHT = pygame.Rect(WIDTH//2 + 50, ROOM_Y, ROOM_W//2 - 50, 20)

BOTTOM_WALL_LEFT = pygame.Rect(ROOM_X, ROOM_Y + ROOM_H - 20, ROOM_W//2 - 50, 20)
BOTTOM_WALL_RIGHT = pygame.Rect(WIDTH//2 + 50, ROOM_Y + ROOM_H - 20, ROOM_W//2 - 50, 20)

LEFT_WALL_TOP = pygame.Rect(ROOM_X, ROOM_Y, 20, ROOM_H//2 - 50)
LEFT_WALL_BOTTOM = pygame.Rect(ROOM_X, HEIGHT//2 + 50, 20, ROOM_H//2 - 50)

RIGHT_WALL_TOP = pygame.Rect(ROOM_X + ROOM_W - 20, ROOM_Y, 20, ROOM_H//2 - 50)
RIGHT_WALL_BOTTOM = pygame.Rect(ROOM_X + ROOM_W - 20, HEIGHT//2 + 50, 20, ROOM_H//2 - 50)

BASE_WALLS = [
    TOP_WALL_LEFT,
    TOP_WALL_RIGHT,

    BOTTOM_WALL_LEFT,
    BOTTOM_WALL_RIGHT,

    LEFT_WALL_TOP,
    LEFT_WALL_BOTTOM,

    RIGHT_WALL_TOP,
    RIGHT_WALL_BOTTOM
]

global_blood = []
hitboxes = False
# =========================================================
# HELPERS
# =========================================================
def move_with_collision(rect, dx, dy, colliders):

    rect.x += dx

    for collider in colliders:

        if rect.colliderect(collider):

            if dx > 0:
                rect.right = collider.left

            elif dx < 0:
                rect.left = collider.right

    rect.y += dy

    for collider in colliders:

        if rect.colliderect(collider):

            if dy > 0:
                rect.bottom = collider.top

            elif dy < 0:
                rect.top = collider.bottom

# =========================================================
# ROCK
# =========================================================
class Rock:

    def __init__(self, x, y, size=50):

        self.rect = pygame.Rect(x, y, size, size)

    def draw(self):
        pygame.draw.rect(screen, (0,0,0),
            pygame.Rect(self.rect.x - 5, self.rect.y - 5,
                    self.rect.w + 10, self.rect.h + 10))
        pygame.draw.rect(screen, (55, 42, 38), self.rect)
        pygame.draw.rect(screen, (92, 68, 63), pygame.Rect(self.rect.x, self.rect.y, self.rect.w - 20, self.rect.h-20))
        pygame.draw.rect(screen, (55, 42, 38), self.rect,4)

# =========================================================
# BULLET
# =========================================================
class Tear:

    def __init__(self, x, y, dx, dy):

        self.x = x
        self.y = y
        self.size = 1
        self.damage = 1
        length = math.hypot(dx, dy)
        self.SPEED = 8
        
        if length == 0:
            length = 1

        dx /= length
        dy /= length

        self.vx = dx * self.SPEED
        self.vy = dy * self.SPEED

        self.radius = 12*self.size
        self.rect = pygame.Rect(
            x - self.radius, y - self.radius,
            self.radius*2, self.radius*2)
        self.dead = False

    def update(self, room):

        self.x += self.vx
        self.y += self.vy

        # update hitbox position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        # OR cleaner:
        # self.rect.center = (self.x, self.y)

        if (
            self.x < ROOM_X or
            self.x > ROOM_X + ROOM_W or
            self.y < ROOM_Y or
            self.y > ROOM_Y + ROOM_H
        ):
            self.dead = True

        # rectangle collision
        for rock in room.rocks:

            if self.rect.colliderect(rock.rect):
                self.dead = True

    def draw(self):
        pygame.draw.circle(
            screen,
            (0,0,0),
            (int(self.x), int(self.y)),
            (self.radius)+5
            
        )
        pygame.draw.circle(
            screen,
            (164, 226, 248),
            (int(self.x), int(self.y)),
            self.radius
        )

        #pygame.draw.rect(screen, (255,0,0), self.rect, 5)


class Blood:

    def __init__(self, x, y, dx, dy):

        self.x = x
        self.y = y

        length = math.hypot(dx, dy)
        self.SPEED = 8
        
        if length == 0:
            length = 1

        dx /= length
        dy /= length

        self.vx = dx * self.SPEED
        self.vy = dy * self.SPEED

        self.radius = 12

        self.dead = False

    def update(self, room, player):

        self.x += self.vx
        self.y += self.vy

        # hit player
        if player.rect.collidepoint(self.x, self.y):

            player.hp -= 1

            self.dead = True

        # outside room
        if (
            self.x < ROOM_X or
            self.x > ROOM_X + ROOM_W or
            self.y < ROOM_Y or
            self.y > ROOM_Y + ROOM_H
        ):
            self.dead = True

        # rock collision
        for rock in room.rocks:

            if rock.rect.collidepoint(self.x, self.y):
                self.dead = True
                
    def draw(self):
        pygame.draw.circle(
            screen,
            (0,0,0),
            (int(self.x), int(self.y)),
            self.radius + 4
        )
        pygame.draw.circle(
            screen,
            (212, 30, 0),
            (int(self.x), int(self.y)),
            self.radius
        )

# =========================================================
# ENEMY SEPARATION
# =========================================================
def enemy_collision(enemy, enemies):

    for other in enemies:

        # don't collide with self
        if other == enemy:
            continue

        if enemy.rect.colliderect(other.rect):

            dx = enemy.rect.centerx - other.rect.centerx
            dy = enemy.rect.centery - other.rect.centery

            dist = math.hypot(dx, dy)

            if dist == 0:
                dist = 1

            dx /= dist
            dy /= dist

            push_strength = 2

            enemy.rect.x += dx * push_strength
            enemy.rect.y += dy * push_strength
# =========================================================
# ENEMY BASE
# =========================================================
class Enemy:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 40, 40)

        self.speed = 2
        self.hp = 3
        self.dead = False
        self.flying = False
        self.color = RED

    def move_toward_player(self, player, room):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        dist = math.hypot(dx, dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        move_x = dx * self.speed
        move_y = dy * self.speed

        colliders = BASE_WALLS if self.flying else room.get_colliders()

        if self.flying:
            # flying ignores rocks completely → direct movement
            self.rect.x += move_x
            self.rect.y += move_y
        else:
            # grounded uses collision system
            move_with_collision(
                self.rect,
                move_x,
                move_y,
                colliders
            )

    
    def update(self, player, room):

        self.move_toward_player(player, room)

        if self.hp <= 0:
            self.dead = True

    def draw(self):
        if hitboxes:
            pygame.draw.rect(screen, self.color, self.rect,4)

# =========================================================
# WALKER
# =========================================================
class fly(Enemy):

    def __init__(self, x, y):

        super().__init__(x, y)
        self.rect = pygame.Rect(x,y,25,25)
        self.color = RED
        self.speed = 3
        self.hp = 2
        self.timer = 0
        self.flying = True
        self.flap = False
        self.flap_timer = 0
        self.MAX_FLAP = 3
        self.MAX_TIME = 20
        self.blink = False
    def draw(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.MAX_TIME
            self.blink = not self.blink
        self.flap_timer -= 1
        if self.flap_timer <= 0:
            self.flap_timer = self.MAX_FLAP
            self.flap = not self.flap

        if self.flap:
            pygame.draw.circle(screen,(0,0,0),
                (self.rect.x, self.rect.y), 14, 5)
            pygame.draw.circle(screen,(0,0,0),
                (self.rect.x+self.rect.w, self.rect.y), 14, 5)
        else:
            pygame.draw.circle(screen,(0,0,0),
                (self.rect.x-5, self.rect.y +10), 14, 5)
            pygame.draw.circle(screen,(0,0,0),
                (self.rect.x+self.rect.w+5, self.rect.y+10), 14, 5)
            
        pygame.draw.ellipse(screen, (0,0,0),
            pygame.Rect(self.rect.x -5, self.rect.y-5,
                        self.rect.w + 10,self.rect.h + 10))
        
        if self.blink:
            pygame.draw.ellipse(screen, RED, self.rect)
        else:
            pygame.draw.ellipse(screen, (40,40,40), self.rect)

# =========================================================
# CHARGER
# =========================================================
class ChargerEnemy(Enemy):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.color = YELLOW
        self.speed = 4
        self.hp = 2
    def draw(self):

        pygame.draw.rect(screen, self.color, self.rect)
        


class Horf(Enemy):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.color = YELLOW
        self.speed = 4
        self.hp = 2
    def update(self, player, room):
        pass

    def shoot(self, dx, dy):


        global_blood.append(
            Blood(
                self.rect.centerx,
                self.rect.centery - 20,
                dx,
                dy
            )
        )
    def draw(self):
        head_x = self.rect.x + self.rect.w // 2
        head_y = self.rect.y + self.rect.h // 2 
        pygame.draw.circle(
            screen,
            (239, 193, 193),
            (head_x, head_y),
            35
        )

        # =====================================================
        # TEAR STREAKS
        # =====================================================

        
        pygame.draw.line(
                screen,
                (212, 30, 0),
                (self.rect.x+4, self.rect.y+20),
                (self.rect.x+4, self.rect.y+26+20),
                13
        )

        pygame.draw.line(
                screen,
                (212, 30, 0),
                (self.rect.x + self.rect.w-5, self.rect.y+20),
                (self.rect.x + self.rect.w-5, self.rect.y+26+20),
                13
        )

        # =====================================================
        # EYES
        # =====================================================


        pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x+4, self.rect.y + 20),
                9
        )

            


        pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x + self.rect.w-5, self.rect.y+20),
                9
        )

            

        # =====================================================
        # FRONT MOUTH
        # =====================================================

        pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2-20+30),
                8
        )
        pygame.draw.circle(
            screen,
            (0,0,0),
            (head_x, head_y),
            35, 5
        )
        #pygame.draw.rect(screen, self.color, self.rect,1)
# =========================================================
# WANDERER
# =========================================================
class WanderEnemy(Enemy):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.color = GREEN
        self.speed = 2
        self.rect = pygame.Rect(x, y, 50, 50)

        self.timer = 0
        
        self.dir_x = 0
        self.dir_y = 0
    def shoot(self, dx, dy):


        global_blood.append(
            Blood(
                self.rect.centerx,
                self.rect.centery - 20,
                dx,
                dy
            )
        )
    def draw(self):
        selfx = self.rect.centerx
        selfy = self.rect.centery
        pygame.draw.ellipse(screen, BLACK,
            pygame.Rect(self.rect.x-5, selfy-5, self.rect.w+10, self.rect.h/2+10+10))
        pygame.draw.ellipse(screen, BLACK,
            pygame.Rect(self.rect.x+10 - 5, self.rect.y + 10 - 5, self.rect.w, self.rect.h))

        
        pygame.draw.ellipse(screen, (145, 35, 35),
            pygame.Rect(self.rect.x, selfy, self.rect.w, self.rect.h/2+10))
        pygame.draw.ellipse(screen, (145, 35, 35),
            pygame.Rect(self.rect.x+10, self.rect.y + 10, self.rect.w-10, self.rect.h -10))
        
        pygame.draw.circle(screen, BLACK, (selfx - 10,selfy+20), 9)
        pygame.draw.circle(screen, WHITE, (selfx - 13,selfy+17), 3)

        pygame.draw.circle(screen, BLACK, (selfx + 10,selfy+16), 10)
        
    def update(self, player, room):

        self.timer -= 1

        if self.timer <= 0:
            
            self.timer = random.randint(60, 100)
            self.shoot(0, 1)
            self.shoot(0, -1)
            self.shoot(1, 0)
            self.shoot(-1, 0)
            self.dir_x = random.choice([-1, 0, 1])
            self.dir_y = random.choice([-1, 0, 1])

        colliders = room.get_colliders()

        move_with_collision(
            self.rect,
            self.dir_x * self.speed,
            self.dir_y * self.speed,
            colliders
        )

        if self.hp <= 0:
            self.dead = True
        


# =========================================================
# ISAAC HEALTH UI
# BIGGER HEARTS
# hp = current half-hearts
# max_health = max half-hearts
# =========================================================
def isaac_health(x, y, hp, max_health = 6):

    heart_spacing = 58

    # total heart containers
    total_hearts = math.ceil(max_health / 2)

    for i in range(total_hearts):

        hx = x + i * heart_spacing
        hy = y

        # =================================================
        # EMPTY HEART CONTAINER
        # =================================================
        pygame.draw.circle(
            screen,
            (0,0,0),
            (hx + 14, hy + 14),
            14
        )

        pygame.draw.circle(
            screen,
            (0,0,0),
            (hx + 36, hy + 14),
            14
        )

        pygame.draw.polygon(
            screen,
            (0,0,0),
            [
                (hx - 2, hy + 16),
                (hx + 25, hy + 48),
                (hx + 52, hy + 16)
            ]
        )

        # inside gray
        pygame.draw.circle(
            screen,
            (50,50,50),
            (hx + 14, hy + 14),
            10
        )

        pygame.draw.circle(
            screen,
            (50,50,50),
            (hx + 36, hy + 14),
            10
        )

        pygame.draw.polygon(
            screen,
            (50,50,50),
            [
                (hx + 4, hy + 18),
                (hx + 25, hy + 42),
                (hx + 46, hy + 18)
            ]
        )

        # =================================================
        # CURRENT HEART VALUE
        # =================================================
        remaining_hp = hp - (i * 2)

        # FULL HEART
        if remaining_hp >= 2:

            color = (220,40,40)

            pygame.draw.circle(
                screen,
                color,
                (hx + 14, hy + 14),
                10
            )

            pygame.draw.circle(
                screen,
                color,
                (hx + 36, hy + 14),
                10
            )

            pygame.draw.polygon(
                screen,
                color,
                [
                    (hx + 4, hy + 18),
                    (hx + 25, hy + 42),
                    (hx + 46, hy + 18)
                ]
            )

            # shine
            pygame.draw.circle(
                screen,
                (255,170,170),
                (hx + 10, hy + 10),
                3
            )

        # HALF HEART
        elif remaining_hp >= 1:

            color = (220,40,40)

            # -----------------------------------------
            # LEFT RED CIRCLE
            # -----------------------------------------
            pygame.draw.circle(
                screen,
                color,
                (hx + 14, hy + 14),
                10
            )

            # -----------------------------------------
            # LEFT HALF BOTTOM
            # -----------------------------------------
            pygame.draw.polygon(
                screen,
                color,
                [
                    (hx + 4, hy + 18),
                    (hx + 25, hy + 42),
                    (hx + 25, hy + 18)
                ]
            )

            # -----------------------------------------
            # COVER RIGHT SIDE
            # makes the split cleaner
            # -----------------------------------------
            

            # -----------------------------------------
            # redraw right gray bump
            # -----------------------------------------
            

            # -----------------------------------------
            # shine
            # -----------------------------------------
            pygame.draw.circle(
                screen,
                (255,170,170),
                (hx + 10, hy + 10),
                3
            )


def boss_health(hp, max_hp):
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(WIDTH //2 - max_hp*4, 650, max_hp * 8, 50))
    pygame.draw.rect(screen, PURPLE, pygame.Rect(WIDTH //2 - hp*4, 650, hp * 8, 50))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(WIDTH //2 - max_hp*4, 650, max_hp * 8, 50),5)
# =========================================================
# BOSS
# =========================================================
class BlobBoss(Enemy):

    def __init__(self, x, y):

        super().__init__(x, y)

        self.rect = pygame.Rect(x, y, 120, 120)

        self.color = PURPLE
        self.max_hp = 40
        self.hp = 40

        self.jump_timer = 90

    def update(self, player, room):

        self.jump_timer -= 1

        if self.jump_timer <= 0:

            self.jump_timer = 90

            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            dist = math.hypot(dx, dy)

            if dist != 0:

                dx /= dist
                dy /= dist

            move_with_collision(
                self.rect,
                dx * 120,
                dy * 120,
                room.get_colliders()
            )

        if self.hp <= 0:
            self.dead = True
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        boss_health(self.hp, self.max_hp)
    

# =========================================================
# PLAYER
# =========================================================
class Player:

    def __init__(self):

        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 60)

        self.speed = 5
        self.maxhealth = 6
        self.hp = self.maxhealth
        
        self.tears = []

        self.fire_delay = 20
        self.fire_timer = 0

    def shoot(self, dx, dy):

        if self.fire_timer > 0:
            return

        self.fire_timer = self.fire_delay

        self.tears.append(
            Tear(
                self.rect.centerx,
                self.rect.centery - 20,
                dx,
                dy
            )
        )

    def update(self, room):

        keys = pygame.key.get_pressed()

        mx = 0
        my = 0

        if keys[pygame.K_a]:
            mx -= 1

        if keys[pygame.K_d]:
            mx += 1

        if keys[pygame.K_w]:
            my -= 1

        if keys[pygame.K_s]:
            my += 1

        move_with_collision(
            self.rect,
            mx * self.speed,
            my * self.speed,
            room.get_colliders()
        )

        if self.fire_timer > 0:
            self.fire_timer -= 1

        if keys[pygame.K_UP]:
            self.shoot(0, -1)

        if keys[pygame.K_DOWN]:
            self.shoot(0, 1)

        if keys[pygame.K_LEFT]:
            self.shoot(-1, 0)

        if keys[pygame.K_RIGHT]:
            self.shoot(1, 0)

        for tear in self.tears[:]:

            tear.update(room)

            if tear.dead:
                self.tears.remove(tear)

    def draw(self):

        keys = pygame.key.get_pressed()

        # =====================================================
        # MOVEMENT ANIMATION
        # =====================================================
        moving = (
            keys[pygame.K_w]
            or keys[pygame.K_a]
            or keys[pygame.K_s]
            or keys[pygame.K_d]
        )

        walk_bob = -30#math.sin(pygame.time.get_ticks() * 0.012) * 3 - 30

        # =====================================================
        # BODY POSITIONING
        # =====================================================
        head_x = self.rect.x + self.rect.w // 2
        head_y = self.rect.y + self.rect.h // 2 - 30

        # MUCH CLOSER BODY
        body_y = head_y + 42 + walk_bob

        left_leg_x = head_x - 10
        right_leg_x = head_x + 10

        leg_offset = -3

        if moving:
            leg_offset = math.sin(pygame.time.get_ticks() * 0.02) * 4

        # =====================================================
        # BODY
        # =====================================================

        pygame.draw.ellipse(
            screen,
            (0,0,0),
            pygame.Rect(
                head_x -20,
                body_y - 10,
                40,
                48
            ),
            
        )

        pygame.draw.circle(screen, BLACK,
                        (left_leg_x - 5, body_y+25), 11)
        pygame.draw.circle(screen, BLACK,
                        (left_leg_x +25, body_y+25), 11)

        
        pygame.draw.circle(screen, BLACK,
                        (left_leg_x - leg_offset, body_y + 35), 11)
        
        pygame.draw.circle(screen, BLACK,
                        (right_leg_x + leg_offset, body_y + 35), 11)
        
        pygame.draw.ellipse(
            screen,
            (239,193,193),
            pygame.Rect(
                head_x -15,
                body_y - 5,
                30,
                38
            )
        )



        # =====================================================
        # LEGS
        # =====================================================
        

        #pygame.draw.line(
         #   screen,
          #  (239,193,193),
           # (left_leg_x, body_y + 32),
            #(left_leg_x - leg_offset, body_y + 40),
            #10
        #)

        pygame.draw.circle(screen, (239,193,193),
                        (left_leg_x - leg_offset, body_y + 35), 6)
        pygame.draw.circle(screen, (239,193,193),
                        (left_leg_x - 5, body_y+25), 6)
        pygame.draw.circle(screen, (239,193,193),
                        (left_leg_x +25, body_y+25), 6)
        
        pygame.draw.circle(screen, (239,193,193),
                        (right_leg_x + leg_offset, body_y + 35), 6)
        #pygame.draw.line(
         #   screen,
          #  (239,193,193),
           # (right_leg_x, body_y + 32),
            #(right_leg_x + leg_offset, body_y + 40),
            #10
        #)

        # =====================================================
        # ARMS
        # =====================================================
        


        

        

        # =====================================================
        # HEAD
        # =====================================================
        pygame.draw.circle(
            screen,
            (239, 193, 193),
            (head_x, head_y),
            35
        )

        # =====================================================
        # TEAR STREAKS
        # =====================================================

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            pygame.draw.line(
                screen,
                (164, 226, 248),
                (self.rect.x+4, self.rect.y),
                (self.rect.x+4, self.rect.y+26),
                13
            )

        if not keys[pygame.K_LEFT] and not keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            pygame.draw.line(
                screen,
                (164, 226, 248),
                (self.rect.x + self.rect.w-5, self.rect.y),
                (self.rect.x + self.rect.w-5, self.rect.y+26),
                13
            )

        # =====================================================
        # EYES
        # =====================================================

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] or keys[pygame.K_DOWN]:

            pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x+4, self.rect.y),
                9
            )

            pygame.draw.circle(
                screen,
                (255,255,255),
                (self.rect.x+1, self.rect.y-3),
                4
            )

        if not keys[pygame.K_LEFT] and not keys[pygame.K_UP] or keys[pygame.K_DOWN]:

            pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x + self.rect.w-5, self.rect.y),
                9
            )

            pygame.draw.circle(
                screen,
                (255,255,255),
                (self.rect.x + self.rect.w-8, self.rect.y-3),
                4
            )

        # =====================================================
        # FRONT MOUTH
        # =====================================================

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] or keys[pygame.K_DOWN]:

            pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2-20),
                8
            )

            pygame.draw.line(
                screen,
                (239, 193, 193),
                (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2-17),
                (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2-7),
                18
            )

            pygame.draw.line(
                screen,
                (255,255,255),
                (self.rect.x + self.rect.w//2-1, self.rect.y + self.rect.h//2-22),
                (self.rect.x + self.rect.w//2-1, self.rect.y + self.rect.h//2-20),
                12
            )

        # =====================================================
        # LEFT MOUTH
        # =====================================================

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:

            pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x -7, self.rect.y + self.rect.h//2-18),
                7
            )

            pygame.draw.line(
                screen,
                (239, 193, 193),
                (self.rect.x -4, self.rect.y + self.rect.h//2-15),
                (self.rect.x -4, self.rect.y + self.rect.h//2-12),
                6
            )

        # =====================================================
        # RIGHT MOUTH
        # =====================================================

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:

            pygame.draw.circle(
                screen,
                (0,0,0),
                (self.rect.x + self.rect.w + 7, self.rect.y + self.rect.h//2 - 18),
                7
            )

            pygame.draw.line(
                screen,
                (239, 193, 193),
                (self.rect.x + self.rect.w + 4, self.rect.y + self.rect.h//2 - 15),
                (self.rect.x + self.rect.w + 4, self.rect.y + self.rect.h//2 - 12),
                6
            )

        # =====================================================
        # HEAD OUTLINE
        # =====================================================

        pygame.draw.circle(
            screen,
            (0,0,0),
            (head_x, head_y),
            35,
            5
        )

        # =====================================================
        # SIDE TEETH DRAWN LAST
        # =====================================================

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:

            pygame.draw.line(
                screen,
                (255,255,255),
                (self.rect.x -7, self.rect.y + self.rect.h//2-20),
                (self.rect.x -7, self.rect.y + self.rect.h//2-18),
                8
            )

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:

            pygame.draw.line(
                screen,
                (255,255,255),
                (self.rect.x + self.rect.w + 7, self.rect.y + self.rect.h//2 - 20),
                (self.rect.x + self.rect.w + 7, self.rect.y + self.rect.h//2 - 18),
                8
            )

        # =====================================================
        # TEARS
        # =====================================================

        for tear in self.tears:
            tear.draw()

# =========================================================
# GRID SETTINGS
# 50x50 ROCK GRID
# covers almost the entire room
# =========================================================
GRID_SIZE = 60

# room padding from walls
GRID_OFFSET_X = ROOM_X + 35
GRID_OFFSET_Y = ROOM_Y + 35

# how many cells fit in room
GRID_COLS = 17
GRID_ROWS = 9

# =========================================================
# ROOM TEMPLATE SYSTEM
#
# # = rock
# "" = empty
#
# each row = vertical
# each item = horizontal
# =========================================================
ROOM_TEMPLATES = [

    # =====================================================
    # SIMPLE CENTER ROCK
    # =====================================================
    {
        "enemies": [
            ("fly", 400, 300),
            ("fly", 700, 300),
            ("fly", 700, 300),
            ("fly", 700, 300),
            ("fly", 700, 300),
            ("wander", 400,400)
        ],

        "rocks": [

            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","#","","","","","","",""],
            ["","","","","","","","#","","","","","","",""],
            ["","","","","","","","#","#","#","#","#","","",""],
            ["","","","#","#","#","#","#","","","","","","",""],
            ["","","","","","","","#","","","","","","",""],
            ["","","","","","","","#","","","","","","",""],
            ["","","","","","","","","","","","","","",""],

        ]
    },

    # =====================================================
    # DOUBLE ROCK
    # =====================================================
    {
        "enemies": [
            ("charger", 600, 250),
            ("fly", 350, 400),
            ("fly", 350, 400),
            ("fly", 350, 400),
            
        ],

        "rocks": [

            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","#","#","","","","","","",""],
            ["","","","","","#","#","#","#","","","","","",""],
            ["","","","","","#","#","#","#","","","","","",""],
            ["","","","","","","#","#","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],

        ]
    },

    # =====================================================
    # HORIZONTAL WALL
    # =====================================================
    {
        "enemies": [
            ("wander", 500, 200),
            ("wander", 700, 450),
            ("fly", 350, 350),
            ("fly", 350, 400),
        ],

        "rocks": [

            ["","","","","","","","","","","","","","",""],
            ["","","","#","","","","","","","","#","","",""],
            ["","#","#","#","","","","","","","","#","#","#",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","#","#","#","","","","","","","","#","#","#",""],
            ["","","","#","","","","","","","","#","","",""],
            ["","","","","","","","","","","","","","",""],

        ]
    },

    # =====================================================
    # FOUR CORNERS
    # =====================================================
    {
        "enemies": [
            ("fly", 300, 200),
            ("fly", 800, 200),
            ("charger", 630, 340),
        ],

        "rocks": [

            ["#","","","","","","","","","","","","","",""],
            ["","","","#","#","#","#","#","#","#","","","","#",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","#","","","","#","#","#","#","#","#","#",""],
            ["","","","","","","","","","","","","","",""],

        ]
    },

    # =====================================================
    # VERTICAL LINE
    # =====================================================
    {
        "enemies": [
            ("wander", 350, 250),
            ("fly", 800, 400),
            ("horf", 550, 350),
            ("fly", 800, 200),
            ("chest", 600, 350)
            
        ],

        "rocks": [

            ["","","","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","","","",""],
            ["","","","","#","","#","#","#","","#","","","","","",""],
            ["","","","","#","","","","","","#","","","","","",""],
            ["","","","","#","","","","","","#","","","","","",""],
            ["","","","","#","","","","","","#","","","","","",""],
            ["","","","","#","","#","#","#","","#","","","","","",""],
            ["","","","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","","","",""],

        ]
    },

    {
        "enemies": [
            ("chest",620,340)
        ],

        "rocks": [

            ["","","","","","#","","","","#","","","","",""],
            ["#","#","#","#","#","","","","","","#","#","#","#","#"],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["","","","","","","","","","","","","","",""],
            ["#","#","#","#","#","","","","","","#","#","#","#","#"],
            ["","","","","","#","","","","#","","","","",""],

        ]
    },
]

# =========================================================
# COLLECTIBLE BASE
# now with velocity / burst physics
# =========================================================
class Collectible:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 34, 34)

        self.dead = False

        # burst velocity
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(10, 20)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.friction = 0.90

    def physics(self, room):

        self.vx *= 0.90
        self.vy *= 0.90

        # X movement
        self.rect.x += self.vx

        for collider in room.get_colliders():

            if self.rect.colliderect(collider):

                if self.vx > 0:
                    self.rect.right = collider.left

                elif self.vx < 0:
                    self.rect.left = collider.right

                self.vx = 0

        # Y movement
        self.rect.y += self.vy

        for collider in room.get_colliders():

            if self.rect.colliderect(collider):

                if self.vy > 0:
                    self.rect.bottom = collider.top

                elif self.vy < 0:
                    self.rect.top = collider.bottom

                self.vy = 0
    def update(self, player,room):
        self.player_push(player, room)
        self.physics(room)
        
    def player_push(self, player, room):

        if self.rect.colliderect(player.rect):

            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery

            dist = math.hypot(dx, dy)

            if dist == 0:
                dist = 1

            dx /= dist
            dy /= dist

            push_force = 1.2

            self.vx += dx * push_force
            self.vy += dy * push_force
    def draw(self):

        pygame.draw.rect(screen, WHITE, self.rect)


# =========================================================
# HEART PICKUP
# =========================================================
class HeartPickup(Collectible):

    def __init__(self, x, y):

        super().__init__(x, y)

    def update(self, player, room):

        super().update(player, room)

        if (
            self.rect.colliderect(player.rect)
            and player.hp < player.maxhealth
        ):

            player.hp += 2

            if player.hp > player.maxhealth:
                player.hp = player.maxhealth

            self.dead = True

    def draw(self):
        pygame.draw.polygon(
            screen,
            (0,0,0),
            [
                (self.rect.x - 3, self.rect.y + 16),
                (self.rect.x + 31, self.rect.y + 22),
                (self.rect.x + 17, self.rect.y + 38),
            ]
        )
        pygame.draw.circle(
            screen,
            (0,0,0),
            (self.rect.x + 10, self.rect.y + 12),
            14
        )

        pygame.draw.circle(
            screen,
            (0,0,0),
            (self.rect.x + 24, self.rect.y + 12),
            14
        )


        pygame.draw.circle(
            screen,
            (220,40,40),
            (self.rect.x + 10, self.rect.y + 12),
            10
        )

        pygame.draw.circle(
            screen,
            (220,40,40),
            (self.rect.x + 24, self.rect.y + 12),
            10
        )

        pygame.draw.polygon(
            screen,
            (220,40,40),
            [
                (self.rect.x + 3, self.rect.y + 16),
                (self.rect.x + 31, self.rect.y + 16),
                (self.rect.x + 17, self.rect.y + 32),
            ]
        )


# =========================================================
# COIN PICKUP
# =========================================================
class CoinPickup(Collectible):

    def __init__(self, x, y):

        super().__init__(x, y)

    def update(self, player, room):

        super().update(player, room)

        if self.rect.colliderect(player.rect):

            self.dead = True

    def draw(self):

        pygame.draw.circle(
            screen,
            (255, 210, 40),
            self.rect.center,
            12
        )

        pygame.draw.circle(
            screen,
            (255, 240, 120),
            self.rect.center,
            7
        )


# =========================================================
# CHEST
# =========================================================
class Chest:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 60, 45)

        self.opened = False

    def update(self, player, room):

        # open on contact
        
        self.player_collision(player, room)
        if (
            self.rect.colliderect(player.rect)
            and not self.opened
        ):

            self.opened = True

            # random pickups
            drop_count = random.randint(2, 6)

            for i in range(drop_count):

                choice = random.choice(["coin", "coin", "heart"])

                px = self.rect.centerx
                py = self.rect.centery

                if choice == "coin":

                    room.pickups.append(
                        CoinPickup(px, py)
                    )

                else:

                    room.pickups.append(
                        HeartPickup(px, py)
                    )

    def draw(self):

        # shadow
        pygame.draw.rect(
            screen,
            (0,0,0),
            pygame.Rect(
                self.rect.x - 4,
                self.rect.y - 4,
                self.rect.w + 8,
                self.rect.h + 8
            ),
            border_radius=6
        )

        if not self.opened:

            # closed chest
            pygame.draw.rect(
                screen,
                (120, 70, 20),
                self.rect,
                border_radius=6
            )

            pygame.draw.rect(
                screen,
                (180, 120, 40),
                pygame.Rect(
                    self.rect.x,
                    self.rect.y,
                    self.rect.w,
                    self.rect.h//2
                ),
                border_radius=6
            )

        else:

            # opened chest
            pygame.draw.rect(
                screen,
                (90, 50, 15),
                self.rect,
                border_radius=6
            )

            pygame.draw.rect(
                screen,
                (70, 40, 10),
                pygame.Rect(
                    self.rect.x,
                    self.rect.y,
                    self.rect.w,
                    self.rect.h//2
                ),
                border_radius=6
            )
    def player_collision(self, player,room):

        if self.rect.colliderect(player.rect):

            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery

            dist = math.hypot(dx, dy)

            if dist == 0:
                dist = 1

            dx /= dist
            dy /= dist

            push_speed = 4

            # attempt movement
            old_x = self.rect.x
            old_y = self.rect.y

            self.rect.x += dx * push_speed
            self.rect.y += dy * push_speed

            # stop chest from entering walls/rocks
            colliders = room.get_colliders()

            for collider in colliders:

                if self.rect.colliderect(collider):

                    self.rect.x = old_x
                    self.rect.y = old_y

                    break
# =========================================================
# ROOM
# =========================================================
class Room:

    def __init__(self, room_type="normal"):

        self.room_type = room_type

        self.cleared = False
        self.visited = False
        self.chests = []
        self.pickups = []
        self.enemies = []
        self.rocks = []

        self.generate()
        
    def generate(self):

        
        if self.room_type == "start":
            return

        if self.room_type == "boss":

            self.enemies.append(
                BlobBoss(WIDTH//2 - 60, HEIGHT//2 - 60)
            )

            

            return

        template = random.choice(ROOM_TEMPLATES)

        for enemy_data in template["enemies"]:

            etype, x, y = enemy_data

            if etype == "fly":
                self.enemies.append(fly(x, y))

            elif etype == "charger":
                self.enemies.append(ChargerEnemy(x, y))

            elif etype == "wander":
                self.enemies.append(WanderEnemy(x, y))
            elif etype == "chest":
                self.chests.append(Chest(x,y))
            elif etype == "horf":
                self.enemies.append(Horf(x, y))
        # =====================================================
        # GENERATE ROCKS FROM GRID
        # =====================================================
        rock_grid = template["rocks"]

        for row_index, row in enumerate(rock_grid):

            for col_index, cell in enumerate(row):

                if cell == "#":

                    rock_x = GRID_OFFSET_X + col_index * GRID_SIZE
                    rock_y = GRID_OFFSET_Y + row_index * GRID_SIZE

                    self.rocks.append(
                        Rock(
                            rock_x,
                            rock_y,
                            50,
                        )
                    )

    # =====================================================
    # COLLIDERS
    # =====================================================
    def get_colliders(self):

        colliders = BASE_WALLS[:]

        # fake walls for nonexistent doors
        if not dungeon.room_exists_up():
            colliders.append(
                pygame.Rect(WIDTH//2 - 50, ROOM_Y, 100, 20)
            )

        if not dungeon.room_exists_down():
            colliders.append(
                pygame.Rect(WIDTH//2 - 50, ROOM_Y + ROOM_H - 20, 100, 20)
            )

        if not dungeon.room_exists_left():
            colliders.append(
                pygame.Rect(ROOM_X, HEIGHT//2 - 50, 20, 100)
            )

        if not dungeon.room_exists_right():
            colliders.append(
                pygame.Rect(ROOM_X + ROOM_W - 20, HEIGHT//2 - 50, 20, 100)
            )

        # room uncleared
        if not self.cleared:

            colliders.append(
                pygame.Rect(WIDTH//2 - 50, ROOM_Y, 100, 20)
            )

            colliders.append(
                pygame.Rect(WIDTH//2 - 50, ROOM_Y + ROOM_H - 20, 100, 20)
            )

            colliders.append(
                pygame.Rect(ROOM_X, HEIGHT//2 - 50, 20, 100)
            )

            colliders.append(
                pygame.Rect(ROOM_X + ROOM_W - 20, HEIGHT//2 - 50, 20, 100)
            )

        for rock in self.rocks:
            colliders.append(rock.rect)

        return colliders

    def update(self, player):

        for enemy in self.enemies[:]:

            enemy.update(player, self)

            enemy_collision(enemy, self.enemies)

            for tear in player.tears[:]:

                if tear.rect.colliderect(enemy.rect):

                    enemy.hp -= tear.damage

                    tear.dead = True

            if enemy.rect.colliderect(player.rect):
                player.hp -= 0.02

            if enemy.dead:
                self.enemies.remove(enemy)

        if len(self.enemies) == 0:
            self.cleared = True
        for pickup in self.pickups[:]:

            pickup.update(player,self)

            if pickup.dead:
                self.pickups.remove(pickup)
        for chest in self.chests:
            chest.update(player, self)

    def draw(self):

        pygame.draw.rect(
            screen,
            (111, 69, 58),
            (ROOM_X, ROOM_Y, ROOM_W, ROOM_H)
        )

        for wall in BASE_WALLS:
            pygame.draw.rect(screen, (0,0,0),
                pygame.Rect(wall.x -5, wall.y - 5, wall.w + 10, wall.h + 10))

        for wall in BASE_WALLS:
            pygame.draw.rect(screen, (85, 51, 37), wall)

        # doors
        door_color = (61, 25, 17)
        
        if not dungeon.room_exists_up():
            recter = TOP_DOOR
            pygame.draw.rect(screen, (0,0,0),
                pygame.Rect(recter.x -5, recter.y - 5,
                            recter.w + 10, recter.h + 10))
            pygame.draw.rect(screen, (85, 51, 37),
                             pygame.Rect(recter.x - 20, recter.y, recter.w + 40, recter.h))
                
        if not dungeon.room_exists_down():
            recter = BOTTOM_DOOR
            pygame.draw.rect(screen, (0,0,0),
                pygame.Rect(recter.x -5, recter.y - 5,
                            recter.w + 10, recter.h + 10))
            pygame.draw.rect(screen, (85, 51, 37),
                             pygame.Rect(recter.x - 20, recter.y, recter.w + 40, recter.h))

        if not dungeon.room_exists_left():
            recter = LEFT_DOOR
            pygame.draw.rect(screen, (0,0,0),
                pygame.Rect(recter.x -5, recter.y - 5,
                            recter.w + 10, recter.h + 10))
            pygame.draw.rect(screen, (85, 51, 37),
                             pygame.Rect(recter.x, recter.y-20, recter.w, recter.h+40))

        if not dungeon.room_exists_right():
            recter = RIGHT_DOOR
            pygame.draw.rect(screen, (0,0,0),
                pygame.Rect(recter.x -5, recter.y - 5,
                            recter.w + 10, recter.h + 10))
            pygame.draw.rect(screen, (85, 51, 37),
                             pygame.Rect(recter.x, recter.y-20, recter.w, recter.h+40))
        if not self.cleared:
            if dungeon.room_exists_up():
                recter = TOP_DOOR
                pygame.draw.rect(screen, (0,0,0),
                    pygame.Rect(recter.x -5, recter.y - 5,
                                recter.w + 10, recter.h + 10))
                pygame.draw.rect(screen, door_color, TOP_DOOR)
                
            if dungeon.room_exists_down():
                recter = BOTTOM_DOOR
                pygame.draw.rect(screen, (0,0,0),
                    pygame.Rect(recter.x -5, recter.y - 5,
                                recter.w + 10, recter.h + 10))
                pygame.draw.rect(screen, door_color, BOTTOM_DOOR)

            if dungeon.room_exists_left():
                recter = LEFT_DOOR
                pygame.draw.rect(screen, (0,0,0),
                    pygame.Rect(recter.x -5, recter.y - 5,
                                recter.w + 10, recter.h + 10))
                pygame.draw.rect(screen, door_color, LEFT_DOOR)

            if dungeon.room_exists_right():
                recter = RIGHT_DOOR
                pygame.draw.rect(screen, (0,0,0),
                    pygame.Rect(recter.x -5, recter.y - 5,
                                recter.w + 10, recter.h + 10))
                pygame.draw.rect(screen, door_color, RIGHT_DOOR)

        # rocks
        for rock in self.rocks:
            rock.draw()

        # enemies
        for enemy in self.enemies:
            enemy.draw()
        # chests
        for chest in self.chests:
            chest.draw()
            
        #pickups
        for pickup in self.pickups:
            pickup.draw()
        

# =========================================================
# DUNGEON
# =========================================================
font_mini = pygame.font.SysFont("Segoe UI Emoji", 15)
class Dungeon:

    def __init__(self):

        self.rooms = {}

        self.current_pos = (0, 0)

        # =========================================
        # DUNGEON SIZE LIMITS
        # =========================================
        self.max_width = 4
        self.max_height = 3

        self.generate_floor()

    def generate_floor(self):

        self.rooms[(0, 0)] = Room("start")

        current = (0, 0)

        ROOM_COUNT = 15

        for i in range(ROOM_COUNT):

            direction = random.choice([
                (1,0),
                (-1,0),
                (0,1),
                (0,-1),
            ])

            new_room = (
                current[0] + direction[0],
                current[1] + direction[1]
            )

            # =====================================
            # STOP DUNGEON FROM GOING TOO FAR
            # =====================================
            if (
                abs(new_room[0]) > self.max_width or
                abs(new_room[1]) > self.max_height
            ):
                continue

            if new_room not in self.rooms:
                self.rooms[new_room] = Room()

            current = new_room

        # =========================================
        # CHOOSE FARTHEST ROOM AS BOSS
        # =========================================
        possible_rooms = [
            pos for pos in self.rooms.keys()
            if pos != (0, 0)
        ]

        farthest_room = max(
            possible_rooms,
            key=lambda pos: abs(pos[0]) + abs(pos[1])
        )

        self.rooms[farthest_room] = Room("boss")

    def current_room(self):

        return self.rooms[self.current_pos]

    def move(self, dx, dy):

        target = (
            self.current_pos[0] + dx,
            self.current_pos[1] + dy
        )

        if target in self.rooms:

            self.current_pos = target

            self.rooms[target].visited = True

            return True

        return False


    # =====================================================
    # ROOM CHECKS
    # =====================================================
    def room_exists_up(self):
        return (self.current_pos[0], self.current_pos[1]-1) in self.rooms

    def room_exists_down(self):
        return (self.current_pos[0], self.current_pos[1]+1) in self.rooms

    def room_exists_left(self):
        return (self.current_pos[0]-1, self.current_pos[1]) in self.rooms

    def room_exists_right(self):
        return (self.current_pos[0]+1, self.current_pos[1]) in self.rooms

    # =====================================================
    # MINIMAP
    # FULL ISAAC STYLE
    # =====================================================
    def draw_minimap(self):

        # ---------------------------------------------
        # SETTINGS
        # ---------------------------------------------
        tile_size = 30
        spacing = 0

        grid_size = 5

        map_width = grid_size * tile_size + (grid_size - 1) * spacing
        map_height = map_width

        map_x = WIDTH - map_width - 35
        map_y = 35

        # ---------------------------------------------
        # BACKGROUND PANEL
        # ---------------------------------------------
        bg_rect = pygame.Rect(
            map_x - 18,
            map_y - 18,
            map_width + 36,
            map_height + 36
        )

        pygame.draw.rect(screen, (25,25,25), bg_rect)
        pygame.draw.rect(screen, LIGHT, bg_rect, 3)

        # ---------------------------------------------
        # CURRENT ROOM
        # ---------------------------------------------
        current_x, current_y = self.current_pos

        # ---------------------------------------------
        # FIND ALL DISCOVERABLE ROOMS
        # these are rooms adjacent to visited rooms
        # ---------------------------------------------
        discoverable_rooms = set()

        directions = [
            (1,0),
            (-1,0),
            (0,1),
            (0,-1),
        ]

        for pos, room in self.rooms.items():

            if room.visited:

                for dx, dy in directions:

                    check_pos = (
                        pos[0] + dx,
                        pos[1] + dy
                    )

                    if check_pos in self.rooms:

                        check_room = self.rooms[check_pos]

                        if not check_room.visited:
                            discoverable_rooms.add(check_pos)

        # ---------------------------------------------
        # DRAW ROOMS
        # ---------------------------------------------
        for world_pos, room in self.rooms.items():

            # relative to current room
            rel_x = world_pos[0] - current_x
            rel_y = world_pos[1] - current_y

            # only draw within 5x5 area
            if abs(rel_x) > 2 or abs(rel_y) > 2:
                continue

            draw_x = map_x + (rel_x + 2) * (tile_size + spacing)
            draw_y = map_y + (rel_y + 2) * (tile_size + spacing)

            draw_room = False
            color = MAP_GRAY

            # -----------------------------------------
            # VISITED ROOMS
            # -----------------------------------------
            if room.visited:

                draw_room = True
                color = (180,180,180)

                # spawn

                # boss
                

            # -----------------------------------------
            # DISCOVERABLE ROOMS
            # -----------------------------------------
            elif world_pos in discoverable_rooms:

                draw_room = True
                color = (70,70,70)

                

            # -----------------------------------------
            # CURRENT ROOM
            # -----------------------------------------
            if world_pos == self.current_pos:

                draw_room = True
                color = WHITE

            # -----------------------------------------
            # DRAW TILE
            # -----------------------------------------
            if draw_room:

                pygame.draw.rect(
                    screen,
                    color,
                    (draw_x, draw_y, tile_size, tile_size)
                )

                pygame.draw.rect(
                    screen,
                    BLACK,
                    (draw_x, draw_y, tile_size, tile_size),
                    3
                )

                if world_pos in discoverable_rooms:

                    room = self.rooms[world_pos]

                if room.room_type == "boss" and not world_pos == self.current_pos:
                    text = font_mini.render(
                    "💀",
                    True,
                    WHITE
                    )
                    screen.blit(text, (draw_x + 5, draw_y +7))

# =========================================================
# FONTS
# =========================================================
font_big = pygame.font.SysFont("arial", 72)
font_small = pygame.font.SysFont("arial", 32)

# =========================================================
# GAME
# =========================================================
game_state = "menu"

player = Player()

dungeon = Dungeon()

dungeon.rooms[(0,0)].visited = True

# =========================================================
# MAIN LOOP
# =========================================================
running = True

while running:

    clock.tick(60)

    # =====================================================
    # EVENTS
    # =====================================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                game_state = "menu"
                
            if event.key == pygame.K_SPACE:
                if game_state != "game":
                    game_state = "game"
                elif game_state == "game":
                    game_state = "pause"
                
        
            

    screen.fill(BLACK)

    # =====================================================
    # MENU
    # =====================================================
    if game_state == "menu":

        title = font_big.render(
            "THE BINDING OF ISAAC",
            True,
            WHITE
        )

        prompt = font_small.render(
            "PRESS ANY KEY",
            True,
            LIGHT
        )

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 220)
        )

        screen.blit(
            prompt,
            (WIDTH//2 - prompt.get_width()//2, 360)
        )
        player = Player()
        player.hp = player.maxhealth
        dungeon = Dungeon()
        global_blood = []
        dungeon.rooms[(0,0)].visited = True
        pygame.display.flip()
        continue

    elif game_state == "pause":
        pause_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 100, 400, 200)
        room.draw()
        for blood in global_blood:
            blood.draw()
        player.draw()
        
        dungeon.draw_minimap()
        isaac_health(30, 30, player.hp, player.maxhealth)
        pygame.draw.rect(screen, (40,40,40), pause_rect)
        pygame.draw.rect(screen, BLACK, pause_rect, 5)

        text = font_small.render(
        "PAUSED",
        True,
        WHITE
        )
        screen.blit(text, (pause_rect.x + 30, pause_rect.y +30))
        pygame.display.flip()
        continue
    # =====================================================
    # GAME
    # =====================================================
    room = dungeon.current_room()

    player.update(room)

    room.update(player)

    if player.hp <= 1:
        game_state = "menu"

    # =====================================================
    # ROOM TRANSITIONS
    # =====================================================
    if room.cleared:

        if (
            dungeon.room_exists_up() and
            player.rect.colliderect(TOP_DOOR)
        ):

            if dungeon.move(0, -1):

                player.rect.center = (
                    WIDTH//2,
                    ROOM_Y + ROOM_H - 70
                )

        elif (
            dungeon.room_exists_down() and
            player.rect.colliderect(BOTTOM_DOOR)
        ):

            if dungeon.move(0, 1):

                player.rect.center = (
                    WIDTH//2,
                    ROOM_Y + 70
                )

        elif (
            dungeon.room_exists_left() and
            player.rect.colliderect(LEFT_DOOR)
        ):

            if dungeon.move(-1, 0):

                player.rect.center = (
                    ROOM_X + ROOM_W - 70,
                    HEIGHT//2
                )

        elif (
            dungeon.room_exists_right() and
            player.rect.colliderect(RIGHT_DOOR)
        ):

            if dungeon.move(1, 0):

                player.rect.center = (
                    ROOM_X + 70,
                    HEIGHT//2
                )

    # =====================================================
    # DRAW
    # =====================================================
    room.draw()
    
    for blood in global_blood[:]:

        blood.update(room,player)

        if blood.dead:
            global_blood.remove(blood)
            
    for blood in global_blood:
        blood.draw()
    player.draw()

    dungeon.draw_minimap()

    hp_text = font_small.render(
        f"HP: {int(player.hp)}",
        True,
        WHITE
    )
    isaac_health(30, 30, player.hp, player.maxhealth)
    

    pygame.display.flip()

pygame.quit()
