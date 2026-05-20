"""
PYXELART

-Original Code by Sawyer
-Simplified by ChatGPT
-Refined and Polished by Dante



-SETUP-
Go into project and scroll all the way down. 
Then select 'Add Font'. Click the first font 'Acme Regular'.
Next hit Add at the bottom right area of the window.

Now you should be good to go!



-Controls and Explanation-
are you needing some art?
can't import assets?
try Pyxelart! a new and innovative way
to create your own sprites! click with the mouse
to create and remove pixels as needed.
press space to change between drawing and color choosing!
this is a beta so let us now if you have any problems!

When you're done close the window for a copy-pasteable code!
and the math is all relative to a single point (0,0) AKA the top left corner)
so YOU only have to move the x and y variables! how cool is that?


-Terms of Agreement-
(failure to comply to these terms will end up with Dante and Sawyer angry at you)
PLEASE do not steal and pass this code off as yours. Sawyer worked very hard to get this to work.
if you use this tool please give us credit at the end of your code/game.)

"""
import random

import pygame
#import tsapp as tsk
pygame.init()

# Window setup
window_size = 400
window = pygame.display.set_mode([window_size, window_size])


window.fill((255, 255, 255))

# Grid settings
lines = int(window_size / 25)  # Number of grid lines
square_size = int(window_size / lines) # Size of squares
collums = [0]

# Generate grid positions
line_spacing = window_size // lines
for i in range(1, lines + 1):
    collums.append(i * line_spacing)

# Color settings
colors = [(0,0,0)]
current_color_index = 0  # Tracks which color is active
current_color = 0
color_change = False #Color changing mode

#Variables
r = 0
g = 0
b = 0

r1 = False
b1 = False
g1 = False

time = 0

font = pygame.freetype.Font(None, window_size / 16)
font.fgcolor = (255,255,255)

precision = False

# Store active squares
squares = {}

# Draw grid function
def draw_grid():
    window.fill((255,255,255))  
    for pos in collums:
        pygame.draw.line(window, (0, 0, 0), (pos, 0), (pos, window_size), 2)
        pygame.draw.line(window, (0, 0, 0), (0, pos), (window_size, pos), 2)

# Draw initial grid
draw_grid()
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change color mode on when 'Space' is pressed (only affects new squares)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_color = (r,g,b)
                color_change = not color_change
                current_color_index = (current_color_index + 1) % len(colors)
                colors.append(current_color)
                
                    
        
        if color_change == False:        
            
            
            # Handle mouse click to toggle squares 
            # plus offset for more accurate mouse placing.
            x, y = pygame.mouse.get_pos() 
            #x = x - 50
            #y = y - 50
            
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_color = (r,g,b)
    
                # Find closest grid position
                x1 = min(collums, key=lambda val: abs(val - x))
                y1 = min(collums, key=lambda val: abs(val - y))
                                                     
                # Toggle square on/off
                if (x1, y1) in squares:
                    del squares[(x1, y1)]  # Remove square
                else:
                    squares[(x1, y1)] = current_color  # Assign the current color
    
                # Redraw everything
                draw_grid()
                for (sx, sy), color in squares.items():
                    my_rect = pygame.Rect(sx, sy, square_size - 1, square_size - 1)
                    pygame.draw.rect(window, color, (my_rect))
            #pygame.draw.circle(window, (100,100,100), (x,y), 15)
            pygame.display.flip()
    
    if color_change:  # change color on
        window.fill((0,0,0))
        pygame.draw.line(window, (r,g,b), (0, int(window_size /2)), (window_size, int(window_size /2)), int(window_size / 2))
        keys = pygame.key.get_pressed()
        # allows you to press coordinating- 
        #keys to change the color to you choosing
        
        if not precision: 
             
                
                
            if keys[pygame.K_b]:
                b1 = True
                r1 = False
                g1 = False
                
            
            if keys[pygame.K_UP]:
                if b1:
                    b +=1
            if keys[pygame.K_DOWN]:
                if b1:
                    b -= 1
            if b >= 255:
                if b1:
                    b = 255
            if b <= 0:
                if b1:
                    b = 0
                    
                    
            if keys[pygame.K_r]:
                r1 = True
                g1=False
                b1 = False
            
            if r1:
                if keys[pygame.K_UP]:
                    r +=1
                if keys[pygame.K_DOWN]:
                    r -= 1
                if r >= 255:
                    r = 255
                if r <= 0:
                    r = 0
                
            if keys[pygame.K_g]:
                g1 =True
                b1 = False
                r1 = False
            
            if g1:
                if keys[pygame.K_UP]:
                    g +=1
                    
                if keys[pygame.K_DOWN]:
                    g -= 1
                if g >= 255:
                    g = 255
                if g <= 0:
                    g = 0
        if precision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if keys[pygame.K_b]:
                    b1 = True
                    r1 = False
                    g1 = False
                    
                
                if keys[pygame.K_UP]:
                    if b1:
                        b +=1
                if keys[pygame.K_DOWN]:
                    if b1:
                        b -= 1
                if b >= 255:
                    if b1:
                        b = 255
                if b <= 0:
                    if b1:
                        b = 0
                        
                        
                if keys[pygame.K_r]:
                    r1 = True
                    g1=False
                    b1 = False
                
                if r1:
                    if keys[pygame.K_UP]:
                        r +=1
                    if keys[pygame.K_DOWN]:
                        r -= 1
                    if r >= 255:
                        r = 255
                    if r <= 0:
                        r = 0
                    
                if keys[pygame.K_g]:
                    g1 =True
                    b1 = False
                    r1 = False
                
                if g1:
                    if keys[pygame.K_UP]:
                        g +=1
                        
                    if keys[pygame.K_DOWN]:
                        g -= 1
                    if g >= 255:
                        g = 255
                    if g <= 0:
                        g = 0
                    
        if keys[pygame.K_p]:
            precision = True
        else:
            precision = False
        font.render_to(window, (0,0), "RED: " + str(r) + "|  GREEN: " + str(g) + "|  BLUE: " + str(b))
        font.render_to(window, (0,window_size - font.size), "hold 'P' for precision mode")
        pygame.display.flip()


output = []
for coords, color in squares.items():
    
    x,y = coords
    x1 = str(int(int(x + square_size)/10))
    if x != 0:
        x = str(int(x/10))
    else:
        x = str(x)
    
    y = str(int(int(y + int(square_size/2))/10))
    
    
    color = str(color) #                       + color +        +x  +         +y +         +x  +         +y +
    output.append("pygame.draw.line(window, ("+color +" ), (x+" + x + ",y+" + y+"), (x+" + x1 + ",y+" + y+"), "+str(int(square_size/10))+")")
print("\n".join(output))


