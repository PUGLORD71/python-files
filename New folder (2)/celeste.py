"""""""""""""""""""""""
|__                   | 
|  \       /\_    _C\ |
|__/      / | \_ C___J|
|     _  /|   | \     |
|    /_\/| | | | \    |
|___/|||||||||||||\___|
|_--_--CELESTE--_--_--|
|_____________________|
|/\/\/\/\/\/\/\/\/\/\/|
|_-_-_-_-_-_-_-_-_-_-_|
"""""""""""""""""""""""
import pygame

#import tsapp as tsk
import random
import pygame.freetype
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 500
window = pygame.Surface((WIDTH, HEIGHT))
ext_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

def scale_surface(surface, window):
    win_w, win_h = window.get_size()
    scale = min(win_w / WIDTH, win_h / HEIGHT)

    scaled_w = int(WIDTH * scale)
    scaled_h = int(HEIGHT * scale)

    scaled_surface = pygame.transform.scale(surface, (scaled_w, scaled_h))

    x_offset = (win_w - scaled_w) // 2
    y_offset = (win_h - scaled_h) // 2

    #window.fill((0, 0, 0))  # letterbox
    window.blit(scaled_surface, (x_offset, y_offset))


BLACK = (255, 0, 0)

# Player settings
player_width = 64
player_height = 72
player_x = 100
player_y = 800
player_velocity = 19
dash_velocity = 17
dashing = False
gravity = 0.5
jump_power = 12
dash_duration = 10  # Dash duration in frames
is_dashing = False
one_time = True
dash_timer = 0
jumping = True
supers = False
# Player mr,g,bes
x_velocity = 0
y_velocity = 0
ex_velocity = 0.5



respawn = [(50, 800),(1500,200), (1300, 800), (100,100), (25, 800), (50, 850)]
hairx = 0
hairy = 0
hairx1 = 0
hairy1 = 0
hairx2 = 0
hairy2 = 0
lock1 = True
lock3 = True
lock2 = True
bounce_time = 0
on_ground = False
lock = False
moving = False
_3d = 25
# Create player rect
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
once = True
# Set up clock for frame rate
clock = pygame.time.Clock()
running = True
directiony = 0
directionx = 0
climb = False
lock3 = True
lock4 = True
levellock = True
badd = []
#frames
COLOR = (255,0,0)
level = 1

menu = True

bgx = 0

COLOR2 = (125, 0,0)
x = 700
y = 450



offsetx = 19
offsety = 19
facing = "right"
def madeline1():
    pygame.draw.line(window, (COLOR), (x+60,y+25), (x+70,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+35), (x+40,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+45), (x+50,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+25), (x+50,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+60,y+45), (x+70,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+35), (x+30,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+45), (x+40,y+45), 10)
    pygame.draw.line(window, (COLOR2), (x+50,y+55), (x+60,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+35), (x+60,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+45), (x+60,y+45), 10)
    pygame.draw.line(window, (COLOR2), (x+20,y+55), (x+30,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+65), (x+30,y+65), 10)
    pygame.draw.line(window, (COLOR2), (x+30,y+55), (x+40,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+55), (x+50,y+55), 10)
    pygame.draw.line(window, (COLOR2), (x+60,y+35), (x+70,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+25), (x+60,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+45), (x+30,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+65), (x+60,y+65), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+25), (x+40,y+25), 10)
    pygame.draw.line(window, (COLOR2), (x+40,y+35), (x+50,y+35), 10)

def madelineleft():
    pygame.draw.line(window, ((COLOR)), (x+40,y+45), (x+50,y+45), 10)
    pygame.draw.line(window, ((COLOR)), (x+50,y+65), (x+60,y+65), 10)
    pygame.draw.line(window, ((COLOR2)), (x+50,y+55), (x+60,y+55), 10)
    pygame.draw.line(window, ((COLOR2)), (x+10,y+35), (x+20,y+35), 10)
    pygame.draw.line(window, ((COLOR2)), (x+40,y+55), (x+50,y+55), 10)
    pygame.draw.line(window, ((COLOR)), (x+20,y+65), (x+30,y+65), 10)
    pygame.draw.line(window, ((COLOR)), (x+10,y+25), (x+20,y+25), 10)
    pygame.draw.line(window, ((COLOR)), (x+40,y+25), (x+50,y+25), 10)
    pygame.draw.line(window, ((COLOR)), (x+10,y+45), (x+20,y+45), 10)
    pygame.draw.line(window, ((COLOR)), (x+30,y+45), (x+40,y+45), 10)
    pygame.draw.line(window, ((COLOR)), (x+30,y+25), (x+40,y+25), 10)
    pygame.draw.line(window, ((COLOR)), (x+40,y+35), (x+50,y+35), 10)
    pygame.draw.line(window, ((COLOR2)), (x+30,y+35), (x+40,y+35), 10)
    pygame.draw.line(window, ((COLOR)), (x+20,y+35), (x+30,y+35), 10)
    pygame.draw.line(window, ((COLOR2)), (x+20,y+55), (x+30,y+55), 10)
    pygame.draw.line(window, ((COLOR)), (x+50,y+35), (x+60,y+35), 10)
    pygame.draw.line(window, ((COLOR)), (x+50,y+45), (x+60,y+45), 10)
    pygame.draw.line(window, ((COLOR)), (x+30,y+55), (x+40,y+55), 10)
    pygame.draw.line(window, ((COLOR)), (x+20,y+25), (x+30,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+45), (x+30,y+45), 10)
    
def rightwalk():
    pygame.draw.line(window, (COLOR), (x+60,y+25), (x+70,y+25), 10)
    pygame.draw.line(window, (COLOR2), (x+50,y+55), (x+60,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+45), (x+50,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+55), (x+50,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+60,y+45), (x+70,y+45), 10)
    pygame.draw.line(window, (COLOR2), (x+60,y+35), (x+70,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+35), (x+60,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+25), (x+50,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+45), (x+40,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+25), (x+40,y+25), 10)
    pygame.draw.line(window, (COLOR2), (x+40,y+35), (x+50,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+35), (x+40,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+35), (x+30,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+25), (x+60,y+25), 10)
    pygame.draw.line(window, (COLOR2), (x+20,y+55), (x+30,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+60,y+65), (x+70,y+65), 10)
    pygame.draw.line(window, (COLOR), (x+10,y+65), (x+20,y+65), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+45), (x+60,y+45), 10)
    pygame.draw.line(window, (COLOR2), (x+30,y+55), (x+40,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+45), (x+30,y+45), 10)
def leftwalk():
    pygame.draw.line(window, (COLOR), (x+40,y+25), (x+50,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+55), (x+40,y+55), 10)
    pygame.draw.line(window, (COLOR2), (x+30,y+35), (x+40,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+25), (x+30,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+10,y+25), (x+20,y+25), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+35), (x+30,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+45), (x+40,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+60,y+65), (x+70,y+65), 10)
    pygame.draw.line(window, (COLOR2), (x+50,y+55), (x+60,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+45), (x+50,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+45), (x+60,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+20,y+45), (x+30,y+45), 10)
    pygame.draw.line(window, (COLOR2), (x+20,y+55), (x+30,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+10,y+45), (x+20,y+45), 10)
    pygame.draw.line(window, (COLOR), (x+10,y+65), (x+20,y+65), 10)
    pygame.draw.line(window, (COLOR2), (x+10,y+35), (x+20,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+50,y+35), (x+60,y+35), 10)
    pygame.draw.line(window, (COLOR2), (x+40,y+55), (x+50,y+55), 10)
    pygame.draw.line(window, (COLOR), (x+40,y+35), (x+50,y+35), 10)
    pygame.draw.line(window, (COLOR), (x+30,y+25), (x+40,y+25), 10)
bx = 620
by = 100

def berry():
    pass

    
bad = pygame.Rect(100,100,100,100)
    
    
wall_bounce = True
cycleleft = False
cycleright = False
cycle = 0
tim = 100
if level == 1:
    blocks = [pygame.Rect(200, 800, 900, 200), pygame.Rect(0, 900, 900, 100), pygame.Rect(1500, 300, 100, 500), pygame.Rect(0, 300, 100, 700), pygame.Rect(600, 300, 300, 100)]
def _3d_():
    pygame.draw.line(window, (255,255,255), (block.x, block.y), (block.x - _3d, block.y- _3d), 5)
    pygame.draw.line(window, (255,255,255), (block.x, block.y+block.h), (block.x - _3d, block.y- _3d+block.h), 5)
    pygame.draw.line(window, (255,255,255), (block.x+block.w, block.y), (block.x+block.w - _3d, block.y- _3d), 5)
    pygame.draw.line(window, (255,255,255), (block.x+block.w - _3d, block.y - _3d), (block.x - _3d, block.y- _3d), 5)
    pygame.draw.line(window, (255,255,255), (block.x - _3d, block.y - _3d+block.h), (block.x - _3d, block.y- _3d), 5)
    
    pygame.draw.line(window, (255,0,0), (bad.x, bad.y), (bad.x - _3d, bad.y- _3d), 5)
    pygame.draw.line(window, (255,0,0), (bad.x, bad.y+bad.h), (bad.x - _3d, bad.y- _3d+bad.h), 5)
    pygame.draw.line(window, (255,0,0), (bad.x+bad.w, bad.y), (bad.x+bad.w - _3d, bad.y- _3d), 5)
    pygame.draw.line(window, (255,0,0), (bad.x+bad.w - _3d, bad.y - _3d), (bad.x - _3d, bad.y- _3d), 5)
    pygame.draw.line(window, (255,0,0), (bad.x - _3d, bad.y - _3d+bad.h), (bad.x - _3d, bad.y- _3d), 5)
r = 255
g =255
b =255
font = pygame.freetype.Font(None)
font.size = 130
font.fgcolor = (100,100,100)
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            menu = False
        elif event.type == pygame.KEYDOWN:
            menu = False
            running = True
    window.fill((0,0,0))
                            
                                 
    pygame.draw.line(window, (r,g,b), (x+90,y+175), (x+100,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+80,y+35), (x+90,y+35), 10)
    pygame.draw.line(window, (r,g,b), (x+40,y+165), (x+50,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+150,y+85), (x+160,y+85), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+55), (x+80,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+165), (x+110,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+110,y+65), (x+120,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+190,y+175), (x+200,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+0,y+155), (x+10,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+50,y+125), (x+60,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+50,y+55), (x+60,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+165), (x+40,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+125), (x+80,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+0,y+125), (x+10,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+155), (x+100,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+175), (x+170,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+125), (x+190,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+150,y+125), (x+160,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+170,y+125), (x+180,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+150,y+155), (x+160,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+80,y+55), (x+90,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+40,y+75), (x+50,y+75), 10)
    pygame.draw.line(window, (r,g,b), (x+20,y+105), (x+30,y+105), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+65), (x+100,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+165), (x+140,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+15), (x+80,y+15), 10)
    pygame.draw.line(window, (r,g,b), (x+50,y+65), (x+60,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+125), (x+70,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+35), (x+70,y+35), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+165), (x+70,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+175), (x+190,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+145), (x+110,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+125), (x+100,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+145), (x+70,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+40,y+145), (x+50,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+110,y+55), (x+120,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+0,y+145), (x+10,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+190,y+125), (x+200,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+50,y+45), (x+60,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+40,y+125), (x+50,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+85), (x+40,y+85), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+55), (x+140,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+25), (x+80,y+25), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+175), (x+40,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+165), (x+190,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+110,y+125), (x+120,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+125), (x+110,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+80,y+125), (x+90,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+45), (x+140,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+45), (x+70,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+190,y+165), (x+200,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+145), (x+100,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+145), (x+190,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+170,y+115), (x+180,y+115), 10)
    pygame.draw.line(window, (r,g,b), (x+0,y+175), (x+10,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+20,y+125), (x+30,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+155), (x+170,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+65), (x+140,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+35), (x+80,y+35), 10)
    pygame.draw.line(window, (r,g,b), (x+40,y+175), (x+50,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+10,y+175), (x+20,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+175), (x+70,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+80,y+45), (x+90,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+175), (x+110,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+65), (x+110,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+60,y+155), (x+70,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+145), (x+40,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+65), (x+190,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+10,y+65), (x+20,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+175), (x+140,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+165), (x+100,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+20,y+115), (x+30,y+115), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+125), (x+130,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+10,y+15), (x+20,y+15), 10)
    pygame.draw.line(window, (r,g,b), (x+170,y+105), (x+180,y+105), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+95), (x+40,y+95), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+55), (x+130,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+170,y+15), (x+180,y+15), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+165), (x+170,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+175), (x+130,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+145), (x+170,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+175), (x+80,y+175), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+125), (x+40,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+155), (x+130,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+125), (x+140,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+30,y+155), (x+40,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+190,y+145), (x+200,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+125), (x+170,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+35), (x+130,y+35), 10)
    pygame.draw.line(window, (r,g,b), (x+130,y+145), (x+140,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+160,y+95), (x+170,y+95), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+145), (x+130,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+10,y+125), (x+20,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+45), (x+130,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+180,y+155), (x+190,y+155), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+45), (x+100,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+120,y+65), (x+130,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+0,y+165), (x+10,y+165), 10)
    pygame.draw.line(window, (r,g,b), (x+70,y+45), (x+80,y+45), 10)
    pygame.draw.line(window, (r,g,b), (x+150,y+75), (x+160,y+75), 10)
    pygame.draw.line(window, (r,g,b), (x+140,y+125), (x+150,y+125), 10)
    pygame.draw.line(window, (r,g,b), (x+140,y+65), (x+150,y+65), 10)
    pygame.draw.line(window, (r,g,b), (x+10,y+145), (x+20,y+145), 10)
    pygame.draw.line(window, (r,g,b), (x+90,y+55), (x+100,y+55), 10)
    pygame.draw.line(window, (r,g,b), (x+100,y+15), (x+110,y+15), 10)
    font.render_to(window, (200,300), "PRESS A KEY TO BEGIN")


    x += offsetx
    y += offsety
    if x <0:
        offsetx *= -1
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)   
    if y <0:
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)   
        offsety *= -1
    if x +200>WIDTH:
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)   
        offsetx *= -1
    if y + 200 > HEIGHT:
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)   
        offsety *= -1



    pygame.display.flip()


# Game loop
while running:
    
    if level == 4:
        if WIDTH != 3200 or HEIGHT != 2000:
            WIDTH += 200
            if WIDTH >= 3200:
                WIDTH = 3200
           
            HEIGHT += 200
            if HEIGHT >= 2000:
                HEIGHT = 2000
            window = pygame.display.set_mode([WIDTH, HEIGHT])
            window.fill((0,0,0))
    if level == 5:
        if WIDTH != 1600 or HEIGHT != 1000:
            WIDTH -= 200
            if WIDTH <= 1600:
                WIDTH = 1600
           
            HEIGHT -= 200
            if HEIGHT <= 1000:
                HEIGHT = 1000
            window = pygame.display.set_mode([WIDTH, HEIGHT])
            window.fill((0,0,0))
    
    
    
    window.fill((0,0,0))
    
    #bg.draw()
    on_ground = False
    # Key states
    keys = pygame.key.get_pressed()
    for block in blocks:
        
        #pygame.draw.rect(window, (255,255,255), block, 5)
        
        if block.h == 100 and block.w == 100:
            bad = pygame.Rect(block.x, block.y - 50, block.w, 50)
            
        elif level == 2:
            bad = pygame.Rect(1250, 300, 50, 500)
        if level == 3:
            bad = pygame.Rect(0, 900, 1100, 100)
        if level == 3 and block.x == 0:
            bad = pygame.Rect(0, 800, 500, 100)
        if level == 3 and block.x == 100:
            bad = pygame.Rect(200, 300, 1000, 400)
        if level == 3 and block.x == 1400:
            bad = pygame.Rect(1200, 300, 400, 300)
        
        if level == 1:
            bad = pygame.Rect(100, 300, 300,200)
        
        
        
        if level >= 4:
            for bads in badd:
                
                if player_rect.x + int(player_rect.w/2) >= bads.x and player_rect.x+int(player_rect.w/2) <= bads.x + bads.w and player_rect.bottom-10 >= bads.y and player_rect.bottom-10 <= bads.y + bads.h or player_rect.top >= bads.y and player_rect.top <= bads.y + bads.h and player_rect.x + int(player_rect.w/2) >= bads.x and player_rect.x+int(player_rect.w/2) <= bads.x + bads.w:
                    respawnx, respawny = respawn[level -1]
                    player_rect.x = respawnx
                    player_rect.y = respawny
                    pygame.time.wait(tim)
                    x_velocity = 0
                    y_velocity = 0
                    is_dashing = False
                pygame.draw.rect(window, (COLOR), bads)
                pygame.draw.rect(window, (COLOR2), bads,10)
        
        pygame.draw.rect(window, (COLOR), bad)
        pygame.draw.rect(window, (COLOR2), bad,10)
        
        if player_rect.x + int(player_rect.w/2) >= bad.x and player_rect.x+int(player_rect.w/2) <= bad.x + bad.w and player_rect.bottom-10 >= bad.y and player_rect.bottom-10 <= bad.y + bad.h or player_rect.top >= bad.y and player_rect.top <= bad.y + bad.h and player_rect.x + int(player_rect.w/2) >= bad.x and player_rect.x+int(player_rect.w/2) <= bad.x + bad.w:
            respawnx, respawny = respawn[level -1]
            player_rect.x = respawnx
            player_rect.y = respawny
            pygame.time.wait(tim)
            x_velocity = 0
            y_velocity = 0
            is_dashing = False
        
       
        if level == 3:
            bad = pygame.Rect(1500, 600, 100, 300)
            pygame.draw.rect(window, (COLOR), bad)
            pygame.draw.rect(window, (COLOR2), bad,10)
        if player_rect.x + int(player_rect.w/2) >= bad.x and player_rect.x+int(player_rect.w/2) <= bad.x + bad.w and player_rect.bottom-10 >= bad.y and player_rect.bottom-10 <= bad.y + bad.h or player_rect.top >= bad.y and player_rect.top <= bad.y + bad.h and player_rect.x + int(player_rect.w/2) >= bad.x and player_rect.x+int(player_rect.w/2) <= bad.x + bad.w:
            respawnx, respawny = respawn[level -1]
            player_rect.x = respawnx
            player_rect.y = respawny
            pygame.time.wait(tim)
            x_velocity = 0
            y_velocity = 0
            is_dashing = False
        
        
        
        
        
        #_3d_()
        if player_rect.bottom >= block.y+10 and player_rect.right <= block.x+50 and player_rect.top <= block.bottom-10 and player_rect.right >= block.x - 10:
            x_velocity = 0
            player_rect.right = block.x - 10
            if keys[pygame.K_z]:
                climb = True
            else:
                if directionx == 1:
                
                    directionx = 0
                if directionx == -1 :
                    player_rect.x -= 10
                if is_dashing:
                    if keys[pygame.K_c] and keys[pygame.K_UP]:
                        if wall_bounce:
                            wall_bounce = False
                            y_velocity -=jump_power
                    else:
                        if x_velocity >= 10:
                            x_velocity = 9
                        if lock2:
                            y_velocity = -10
                            lock2 = False
                            x_velocity = -10
                            player_rect.x -= 10
                        wall_bounce = True
                        lock2 = False
                    
                
                else:
                    lock2 = True
                climb = False
                if keys[pygame.K_c]:
                    
                    if lock3:
                        if y_velocity < -9: 
                            y_velocity -= 10
                        else:
                            y_velocity = -10
                        lock2 = False
                        x_velocity = -10
                        player_rect.x -= 10
                    lock3 = False
                else:
                    lock3 = True
                climb = False

                
            if climb and keys[pygame.K_z]:
                
                if keys[pygame.K_UP]:
                    player_rect.y -= 7
                elif keys[pygame.K_DOWN]:
                    player_rect.y += 7
                
                    
                if keys[pygame.K_c]:
                    if lock1:
                        lock1 = False
                        y_velocity -= jump_power
            
                else:
                    lock1 = True
                    y_velocity = 0
            else:
                climb = False
            
        if player_rect.bottom >= block.y +10 and player_rect.left >= block.x + block.w -50 and player_rect.top <= block.bottom-10 and player_rect.left <= block.x + block.w+ 10:
            x_velocity = 0
            player_rect.left = block.x + block.w + 10
            if keys[pygame.K_z]:
                climb = True
            else:
                if directionx == -1:
                
                    directionx = 0
                if directionx ==1:
                    player_rect.x += 10
                if is_dashing:
                    if keys[pygame.K_c] and keys[pygame.K_UP]:
                        if wall_bounce:
                            wall_bounce = False
                            y_velocity -=jump_power
                    else:
                        if x_velocity >= 10:
                            x_velocity = 9
                        if lock2:
                            y_velocity = -10
                            lock2 = False
                            x_velocity = -10
                            player_rect.x -= 10
                        wall_bounce = True
                        lock2 = False
                    
                else:
                    lock2 = True
                climb = False

                
                
                
                
                
                
                
                
                if keys[pygame.K_c]:
                    
                    if lock3:
                        if y_velocity < -9: 
                            y_velocity -= 10
                        else:
                            y_velocity = -10
                        lock2 = False
                        x_velocity = 10
                        player_rect.x += 10
                    lock3 = False
                else:
                    lock3 = True
                climb = False
                
            if climb and keys[pygame.K_z]:
                
                if keys[pygame.K_UP]:
                    player_rect.y -= 7
                elif keys[pygame.K_DOWN]:
                    player_rect.y += 7
                
                    
                if keys[pygame.K_c]:
                    if lock4:
                        lock4 = False
                        y_velocity -= jump_power
            
                else:
                    lock4 = True
                    y_velocity = 0
            else:
                climb = False
                
                
                
        if player_rect.top >= block.y + block.h - 10 and player_rect.top <= block.y + block.h and player_rect.left <= block.x + block.w -10 and player_rect.right >= block.x+10:
            player_rect.top = block.y + block.h + 10
            y_velocity = 0
            
        
        
        
        # Simple ground collision 
        if player_rect.bottom >= block.y and player_rect.left <= block.x + block.w-10 and player_rect.right >= block.x+10 and player_rect.top <= block.top - 10:
            COLOR = (255,0,0)
            COLOR2 = (155,0,0)
            player_rect.bottom = block.y
            y_velocity = 0
            on_ground = True
        if is_dashing:
            if player_rect.bottom >= block.y:
                
                if not supers:
                    if on_ground and keys[pygame.K_c] and jumping == False:
                        x_velocity = directionx * dash_velocity * 5
                        y_velocity = -int(jump_power /2)
                        jumping = True
                        
                    
                elif supers:
                    if on_ground and keys[pygame.K_c] and jumping == False:
                        x_velocity = directionx * dash_velocity * 4
                        y_velocity = -jump_power + int(jump_power*0.25)
                        jumping = True
                if once:
                    COLOR = (255,0,0)
                    COLOR2 = (155,0,0)   
                
            dash_timer -= 1
            if dash_timer <= 0:
                is_dashing = False
                  # Stop the dash movement
                
            
            
        
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
                
    
        
    
    
    
    
    
    if not once:
        COLOR = (0,200,255)
        COLOR2 = (0,100,155)
    # Movement
    if not is_dashing:
        moving = False
        if not is_dashing:
            if keys[pygame.K_LEFT]:
                
                if not on_ground and x_velocity < -player_velocity:
                    x_velocity += ex_velocity
                    bounce_time = 0
                elif x_velocity != 10:
                    x_velocity = -player_velocity
                    bounce_time = 0
                elif bounce_time >= 15:
                    x_velocity = -9
                elif bounce_time <=15:    
                    bounce_time+=1
                
                directionx = -1   
                moving = True
                last_key = -1
                facing = "left"
                
            
            if keys[pygame.K_RIGHT] :
                
                    
                if not on_ground and x_velocity > player_velocity:
                    x_velocity -= ex_velocity
                    bounce_time = 0
                elif x_velocity != -10:
                    x_velocity = player_velocity
                    bounce_time = 0
                elif bounce_time >= 15:
                    x_velocity = 9
                elif bounce_time <=15:    
                    bounce_time+=1
                directionx = 1
                moving = True
                last_key = 1
                facing = "right"
            if keys[pygame.K_DOWN]:
                directiony = 1
                moving = True
                last_key = 0
            if keys[pygame.K_UP]:
                directiony = -1
                moving = True
                last_key = 0
        if not moving:
            
            x_velocity = 0
            directiony = 0
             
            if x_velocity <= 0:
                x_velocity = 0
            
        if on_ground and keys[pygame.K_c] and jumping == False:
            
            jumping = True
            y_velocity = -jump_power
            on_ground = False
             
    # Dash logic
    
    
    if not keys[pygame.K_x]:
        lock = False
    if on_ground:
        once = True
    if keys[pygame.K_x] and not is_dashing and once and not lock:
        
        lock = True
        if on_ground:
            supers = True
            
        is_dashing = True
        dash_timer = dash_duration
        once = False
        if directionx != 0:
            dash_duration =17
            dash_velocity = 12
            
        else:
            dash_duration = 12
            dash_velocity = 17
            
            
            
    
        
        if last_key != 0:
            x_velocity = dash_velocity * directionx + (directionx*17)
        
        
        y_velocity = dash_velocity * directiony
    
    
    # Dash timer
    
    # Apply gravity
    if on_ground:
        jumping = False
    if not on_ground and not is_dashing:
        if on_ground and keys[pygame.K_c] and jumping == False:
            pass
        else:
            y_velocity += gravity 
    
    
    
    hair2x = hairx1 - directionx * 6
    hair2y = hairy1 + 10
    pygame.draw.circle(window, COLOR, (hair2x,hair2y), 18)
    
    
    
    hairx1 = hairx - directionx * 10
    hairy1 = hairy + 5
    pygame.draw.circle(window, COLOR, (hairx1,hairy1), 22)
    
    
    
    
    
    # Update player position
    hairx = player_rect.x + 30
    hairy = player_rect.y + 30     
    
    pygame.draw.circle(window, COLOR, (hairx,hairy), 25)
    
    
    player_rect.x = int(player_rect.x + x_velocity)
    player_rect.y = int(player_rect.y + y_velocity)
    x = player_rect.x - 10
    y = player_rect.y
    
    pygame.draw.circle(window, COLOR, (player_rect.x + 29,player_rect.y + 30), 25)
    pygame.draw.line(window, COLOR, (hairx, hairy), (hair2x, hair2y), 34)
    
    # Drawing the player
    #pygame.draw.rect(window, (100,100,100), player_rect)
    
    if on_ground:
        if facing == "right":
            if on_ground and moving:
                if cycle % 4 == 0:
                    cycleright = not cycleright
                    
                if cycleright:
                    madeline1()
                    
                if not cycleright:
                    rightwalk()
                    
    
            else:
                madeline1()
        elif facing == "left":
            
            if on_ground and moving:
                if cycle % 4 == 0:
                    cycleleft = not cycleleft
                    
                if cycleleft:
                    madelineleft()
                    
                if not cycleleft:
                    leftwalk()
                    
    
            else:
                madelineleft()
    elif not on_ground:
        if facing == "right":
            rightwalk()
        else:
            leftwalk()
        
    
    if player_rect.y >= HEIGHT:
        respawnx, respawny = respawn[level -1]
        player_rect.x = respawnx
        player_rect.y = respawny
        pygame.time.wait(tim)
        x_velocity = 0
        y_velocity = 0
        is_dashing = False
    
    #if player_rect.y <= 0 and one_time:
     #   music.play()
      #  one_time = False
    
    #if on_ground:
     #   one_time = True
      #  music.stop()
    
    
    
    #def TOP():
    #    if player_rect.y <= 0:
    #        level += 1
    #        player_rect.y = 850
    #def RIGHT():
    #    if player_rect.x >= WIDTH:
    #        level += 1
    #        player_rect.x = 0
   
        
    for block in blocks:
        pygame.draw.rect(window, (COLOR2), block)#105, 237, 255
        pygame.draw.rect(window, (255,255,255), block, 5)
        pygame.draw.line(window, (255,255,255), (block.x, block.y+10), (block.right, block.y + 10), 20)
        pygame.draw.line(window, (255,255,255), (block.x, block.bottom-10), (block.right, block.bottom - 10), 20)
        pygame.draw.line(window, (255,255,255), (block.x+10, block.top), (block.x + 10, block.bottom), 20)
        pygame.draw.line(window, (255,255,255), (block.right-10, block.top), (block.right - 10, block.bottom), 20)
    
    
    
    
    if level == 1:
        if player_rect.x <= 0:
            level += 1
            player_rect.x = WIDTH
            player_rect.y -= 50
            once = True
            
    if level == 2:
        
        if levellock:
            levellock = False
            blocks = [pygame.Rect(1500, 300, 100, 700), pygame.Rect(1300, 0, 100, 800), pygame.Rect(1000, 300,100,100), pygame.Rect(600,200,100,100), pygame.Rect(400,300,100,100), pygame.Rect(200,500,100,100), pygame.Rect(600,600,100,100), pygame.Rect(1400, 0, 200, 100)]
        if player_rect.y <= 0:
            level += 1
            player_rect.y = 850
            once = True
            levellock = True
    if level == 3:
        
        if levellock:
            levellock = False
        
            blocks = [pygame.Rect(1100,900, 500, 100), pygame.Rect(0, 500, 100, 100), pygame.Rect(100, 200, 200, 100), pygame.Rect(1400, 200, 200, 100)]
        if player_rect.right >= WIDTH:
            level += 1
            levellock = True
            once = True
            player_rect.x = 0
    
    if level == 4:
        if levellock:
            levellock = False
            blocks = [pygame.Rect(0,200,200, 100), pygame.Rect(1600,500,300,200),pygame.Rect(1400, 600, 100, 600),pygame.Rect(600, 100, 100, 100), pygame.Rect(300, 1300, 100, 100), pygame.Rect(600, 1100, 100, 100), pygame.Rect( 900, 1700, 100,100), pygame.Rect(1200, 1900, 500, 100), pygame.Rect(3000, 200, 100,100)]
            badd = [pygame.Rect(0, 400, 1200, 300), pygame.Rect(3100, 100, 100, 1800), pygame.Rect(1200, 1200, 1900, 500), pygame.Rect(200, 1700, 500, 200)]
        if player_rect.right >= WIDTH:
            level += 1
            player_rect.x = 0
            player_rect.y = 800
            levellock = True
        #pygame.draw.polygon(window,(0,255,0), [(500,800), (525, 775), (550,800), (525, 825)])
        #if player_rect.top - player_rect.h/2 >775 and player_rect.top - player_rect.h/2 <825:
         #   COLOR = (255,0,0)
          #  COLOR2 = (155,0,0)
           # once = True
    if level == 5:  
        if levellock:
            levellock = False
            blocks = [pygame.Rect(0, 900, 200, 100), pygame.Rect(1400, 800, 100,100), pygame.Rect(1200, 200, 100,100), pygame.Rect(300, 200,100,100)]
            badd = [pygame.Rect(0, 400, 1200, 300), pygame.Rect(1500, 800, 50,100), pygame.Rect(1300, 200, 50,100), pygame.Rect(400, 200,50,100), pygame.Rect(100, 0, 1500, 50)]
        if player_rect.y <= 0:
            level += 1
            player_rect.x = 0
            player_rect.y = 850
            levellock = True
    if level == 6:
        if levellock:
            levellock = False
            blocks = [pygame.Rect(0,900,200,100), pygame.Rect(600, 800, 100,100), pygame.Rect(400,400,100,100), pygame.Rect(1200, 300, 100,100), pygame.Rect(1500, 0, 100, 700,), pygame.Rect(1500, 900, 100, 100)]
            badd = [pygame.Rect(700, 800, 50,100), pygame.Rect(350,400,50,100), pygame.Rect(1150, 300, 50,100),pygame.Rect(1300, 300, 50,100), pygame.Rect(1200, 400, 100,50), pygame.Rect(1500, 700, 100, 50,)]
    
    
    
    
    
    
    
    
    
    if player_rect.right >= WIDTH:
        player_rect.right = WIDTH
    if player_rect.top <= 0:
        player_rect.top = 0
    if player_rect.left <= 0:
        player_rect.left = 0
    
    
    
    
    
    
    
    
    
    
    
    # Refresh the screen
    scale_surface(window, ext_surf)
    pygame.display.flip()
    cycle += 1
    # Frame rate
    clock.tick(60)
