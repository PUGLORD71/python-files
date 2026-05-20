# =========================================================
# ISAAC STYLE SPRITE EDITOR
# FULL REWRITE
# =========================================================
#
# FEATURES
# - circles
# - ellipses
# - rects
# - lines
# - ALL shapes relative to center point
# - selectable shapes
# - arrow key movement
# - zoom in/out
# - live color sliders
# - live preview before coloring
# - export code
# - no console needed
#
# CONTROLS
# =========================================================
#
# 1 = circle
# 2 = ellipse
# 3 = rect
# 4 = line
#
# LEFT CLICK = place shape
# RIGHT CLICK = select shape
#
# DELETE = delete selected
#
# ARROWS = move selected shape
#
# Q/E = zoom out/in
#
# TAB = cycle selected shape
#
# P = export code
#
# RGB sliders on right
#
# =========================================================

import pygame
import sys

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 1500
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isaac Sprite Editor")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

WHITE = (255,255,255)
BLACK = (0,0,0)

GRAY = (60,60,60)
LIGHT = (180,180,180)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# =========================================================
# CENTER
# =========================================================

CENTER_X = WIDTH // 2 - 150
CENTER_Y = HEIGHT // 2

# =========================================================
# FONT
# =========================================================

font = pygame.font.SysFont("arial", 22)

# =========================================================
# STATE
# =========================================================

shapes = []

selected_shape = -1

current_tool = "circle"

zoom = 1.0

placing = False
start_pos = (0,0)

current_color = [0,0,0]

export_mode = False
export_x_name = ""
export_y_name = ""

# =========================================================
# SLIDER
# =========================================================

class Slider:

    def __init__(self, x, y, color_index):

        self.rect = pygame.Rect(x, y, 220, 20)

        self.value = 0

        self.color_index = color_index

        self.dragging = False

    def update(self):

        mouse = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:

            if self.rect.collidepoint(mouse):
                self.dragging = True

        else:
            self.dragging = False

        if self.dragging:

            rel = mouse[0] - self.rect.x

            rel = max(0, min(rel, self.rect.w))

            self.value = int((rel / self.rect.w) * 255)

    def draw(self):

        pygame.draw.rect(screen, LIGHT, self.rect)

        knob_x = self.rect.x + (self.value / 255) * self.rect.w

        pygame.draw.circle(
            screen,
            WHITE,
            (int(knob_x), self.rect.centery),
            12
        )

# =========================================================
# SLIDERS
# =========================================================

r_slider = Slider(1200, 120, 0)
g_slider = Slider(1200, 180, 1)
b_slider = Slider(1200, 240, 2)

# =========================================================
# HELPERS
# =========================================================

def world_to_screen(x, y):

    return (
        CENTER_X + x * zoom,
        CENTER_Y + y * zoom
    )

# =========================================================
# EXPORT
# =========================================================

def export_code():

    global export_x_name
    global export_y_name

    code = []

    code.append(f"# GENERATED SPRITE")
    code.append(f"head_x = {export_x_name}")
    code.append(f"head_y = {export_y_name}")
    code.append("")

    for shape in shapes:

        if shape["type"] == "circle":

            code.append(
f'''pygame.draw.circle(screen, {shape["color"]},
    (head_x + {shape["x"]}, head_y + {shape["y"]}),
    {shape["radius"]})'''
            )

        elif shape["type"] == "ellipse":

            code.append(
f'''pygame.draw.ellipse(screen, {shape["color"]},
    pygame.Rect(
        head_x + {shape["x"]},
        head_y + {shape["y"]},
        {shape["w"]},
        {shape["h"]}
    ))'''
            )

        elif shape["type"] == "rect":

            code.append(
f'''pygame.draw.rect(screen, {shape["color"]},
    pygame.Rect(
        head_x + {shape["x"]},
        head_y + {shape["y"]},
        {shape["w"]},
        {shape["h"]}
    ))'''
            )

        elif shape["type"] == "line":

            code.append(
f'''pygame.draw.line(screen, {shape["color"]},
    (head_x + {shape["x1"]}, head_y + {shape["y1"]}),
    (head_x + {shape["x2"]}, head_y + {shape["y2"]}),
    {shape["thickness"]})'''
            )

    return "\n\n".join(code)

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

        # =================================================
        # KEYS
        # =================================================

        if event.type == pygame.KEYDOWN:

            # tools
            if event.key == pygame.K_1:
                current_tool = "circle"

            if event.key == pygame.K_2:
                current_tool = "ellipse"

            if event.key == pygame.K_3:
                current_tool = "rect"

            if event.key == pygame.K_4:
                current_tool = "line"

            # zoom
            if event.key == pygame.K_q:
                zoom -= 0.1

            if event.key == pygame.K_e:
                zoom += 0.1

            zoom = max(0.2, min(zoom, 5))

            # cycle selection
            if event.key == pygame.K_TAB:

                if len(shapes) > 0:

                    selected_shape += 1

                    if selected_shape >= len(shapes):
                        selected_shape = 0

            # delete
            if event.key == pygame.K_DELETE:

                if selected_shape != -1:

                    shapes.pop(selected_shape)

                    selected_shape = -1

            # movement
            if selected_shape != -1:

                shape = shapes[selected_shape]

                move_speed = 2

                if event.key == pygame.K_LEFT:

                    if "x" in shape:
                        shape["x"] -= move_speed

                    if "x1" in shape:
                        shape["x1"] -= move_speed
                        shape["x2"] -= move_speed

                if event.key == pygame.K_RIGHT:

                    if "x" in shape:
                        shape["x"] += move_speed

                    if "x1" in shape:
                        shape["x1"] += move_speed
                        shape["x2"] += move_speed

                if event.key == pygame.K_UP:

                    if "y" in shape:
                        shape["y"] -= move_speed

                    if "y1" in shape:
                        shape["y1"] -= move_speed
                        shape["y2"] -= move_speed

                if event.key == pygame.K_DOWN:

                    if "y" in shape:
                        shape["y"] += move_speed

                    if "y1" in shape:
                        shape["y1"] += move_speed
                        shape["y2"] += move_speed

            # export
            if event.key == pygame.K_p:

                export_mode = True
                export_x_name = "head_x"
                export_y_name = "head_y"

                print(export_code())

        # =================================================
        # MOUSE
        # =================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            rel_x = int((mx - CENTER_X) / zoom)
            rel_y = int((my - CENTER_Y) / zoom)

            # left click place
            if event.button == 1:

                color = (
                    r_slider.value,
                    g_slider.value,
                    b_slider.value
                )

                # circle
                if current_tool == "circle":

                    shapes.append({
                        "type":"circle",
                        "x":rel_x,
                        "y":rel_y,
                        "radius":30,
                        "color":color
                    })

                # ellipse
                elif current_tool == "ellipse":

                    shapes.append({
                        "type":"ellipse",
                        "x":rel_x,
                        "y":rel_y,
                        "w":80,
                        "h":50,
                        "color":color
                    })

                # rect
                elif current_tool == "rect":

                    shapes.append({
                        "type":"rect",
                        "x":rel_x,
                        "y":rel_y,
                        "w":80,
                        "h":50,
                        "color":color
                    })

                # line
                elif current_tool == "line":

                    shapes.append({
                        "type":"line",
                        "x1":rel_x,
                        "y1":rel_y,
                        "x2":rel_x + 50,
                        "y2":rel_y,
                        "thickness":6,
                        "color":color
                    })

            # right click select
            if event.button == 3:

                if len(shapes) > 0:

                    selected_shape += 1

                    if selected_shape >= len(shapes):
                        selected_shape = 0

    # =====================================================
    # UPDATE
    # =====================================================

    r_slider.update()
    g_slider.update()
    b_slider.update()

    # =====================================================
    # DRAW
    # =====================================================

    screen.fill((30,30,30))

    # center lines
    pygame.draw.line(
        screen,
        (70,70,70),
        (CENTER_X, 0),
        (CENTER_X, HEIGHT),
        2
    )

    pygame.draw.line(
        screen,
        (70,70,70),
        (0, CENTER_Y),
        (WIDTH, CENTER_Y),
        2
    )
    

    # =====================================================
    # DRAW SHAPES
    # =====================================================

    for i, shape in enumerate(shapes):

        selected = i == selected_shape

        outline = WHITE if selected else None

        if shape["type"] == "circle":

            x, y = world_to_screen(shape["x"], shape["y"])

            pygame.draw.circle(
                screen,
                shape["color"],
                (int(x), int(y)),
                int(shape["radius"] * zoom)
            )

            if selected:

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (int(x), int(y)),
                    int(shape["radius"] * zoom),
                    3
                )

        elif shape["type"] == "ellipse":

            x, y = world_to_screen(shape["x"], shape["y"])

            rect = pygame.Rect(
                x,
                y,
                shape["w"] * zoom,
                shape["h"] * zoom
            )

            pygame.draw.ellipse(
                screen,
                shape["color"],
                rect
            )

            if selected:
                pygame.draw.ellipse(
                    screen,
                    WHITE,
                    rect,
                    3
                )

        elif shape["type"] == "rect":

            x, y = world_to_screen(shape["x"], shape["y"])

            rect = pygame.Rect(
                x,
                y,
                shape["w"] * zoom,
                shape["h"] * zoom
            )

            pygame.draw.rect(
                screen,
                shape["color"],
                rect
            )

            if selected:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    rect,
                    3
                )

        elif shape["type"] == "line":

            x1, y1 = world_to_screen(shape["x1"], shape["y1"])
            x2, y2 = world_to_screen(shape["x2"], shape["y2"])

            pygame.draw.line(
                screen,
                shape["color"],
                (x1,y1),
                (x2,y2),
                int(shape["thickness"] * zoom)
            )

    # =====================================================
    # UI
    # =====================================================

    pygame.draw.rect(
        screen,
        (45,45,45),
        pygame.Rect(1120, 0, 380, HEIGHT)
    )

    tool_text = font.render(
        f"TOOL: {current_tool}",
        True,
        WHITE
    )

    screen.blit(tool_text, (1150, 40))

    zoom_text = font.render(
        f"ZOOM: {round(zoom,2)}",
        True,
        WHITE
    )

    screen.blit(zoom_text, (1150, 70))

    # sliders
    r_slider.draw()
    g_slider.draw()
    b_slider.draw()

    # labels
    screen.blit(font.render("R", True, RED), (1160, 115))
    screen.blit(font.render("G", True, GREEN), (1160, 175))
    screen.blit(font.render("B", True, BLUE), (1160, 235))

    # preview color
    pygame.draw.rect(
        screen,
        (
            r_slider.value,
            g_slider.value,
            b_slider.value
        ),
        pygame.Rect(1180, 320, 120, 120)
    )

    pygame.display.flip()

pygame.quit()
sys.exit()
