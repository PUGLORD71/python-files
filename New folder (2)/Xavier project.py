import pygame
import math

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Physics Sandbox")
clock = pygame.time.Clock()

# =========================
# CONSTANTS
# =========================
GRAVITY = 0.6
FRICTION = 0.995

GRAB_MODE = 0
RACKET_MODE = 1
LINE_MODE = 2
BALL_MODE = 3
DELETE_MODE = 4
RECT_MODE = 5

# =========================
# CAMERA
# =========================
camera_offset = pygame.Vector2(0, 0)
zoom = 1.0

panning = False
pan_start_mouse = pygame.Vector2()
pan_start_offset = pygame.Vector2()

# =========================
# HELPERS
# =========================
def world_to_screen(pos):
    return (pos - camera_offset) * zoom

def screen_to_world(pos):
    return pygame.Vector2(pos) / zoom + camera_offset

def distance_to_line(point, start, end):

    line = end - start
    length = line.length()

    if length == 0:
        return 999999

    direction = line.normalize()

    proj = max(0, min(length, (point - start).dot(direction)))
    closest = start + direction * proj

    return point.distance_to(closest)

# =========================
# BALL
# =========================
class Ball:

    def __init__(self, x, y, ra=40):

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2()

        self.radius = ra

        self.held = False
        self.prev_mouse = pygame.Vector2()

    def update(self):

        if not self.held:

            self.vel.y += GRAVITY

            self.pos += self.vel

            self.vel *= FRICTION

            bottom_world_y = camera_offset.y + (HEIGHT / zoom)

            # FLOOR
            if self.pos.y + self.radius > bottom_world_y:

                self.pos.y = bottom_world_y - self.radius

                self.vel.y *= -0.7

            # WALLS
            if self.pos.x < -3000:

                self.pos.x = -3000 + self.radius
                self.vel.x *= -0.8

            if self.pos.x > 3000:

                self.pos.x = 3000 - self.radius
                self.vel.x *= -0.8

    def draw(self):

        draw_pos = world_to_screen(self.pos)

        pygame.draw.circle(
            screen,
            (80, 200, 255),
            draw_pos,
            int(self.radius * zoom)
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            draw_pos,
            int(self.radius * zoom),
            max(1, int(2 * zoom))
        )

        if self.held:

            pygame.draw.circle(
                screen,
                (255, 120, 120),
                draw_pos,
                int(self.radius * zoom),
                4
            )

    def grab(self, mouse_world):

        self.held = True
        self.prev_mouse = mouse_world

    def drag(self, mouse_world):

        self.vel = mouse_world - self.prev_mouse

        self.pos = mouse_world

        self.prev_mouse = mouse_world

    def release(self, mouse_world):

        self.held = False
        self.vel = (mouse_world - self.prev_mouse) * 0.6

# =========================
# LINE
# =========================
class Line:

    def __init__(self, start, end):

        self.start = pygame.Vector2(start)
        self.end = pygame.Vector2(end)

    def draw(self):

        pygame.draw.line(
            screen,
            (255, 255, 255),
            world_to_screen(self.start),
            world_to_screen(self.end),
            max(2, int(4 * zoom))
        )

# =========================
# RECTANGLE
# =========================
class PhysicsRect:

    def __init__(self, x, y, w, h):

        self.pos = pygame.Vector2(x, y)
        self.size = pygame.Vector2(w, h)

        self.vel = pygame.Vector2()

        self.held = False
        self.prev_mouse = pygame.Vector2()

    @property
    def rect(self):

        return pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.size.x,
            self.size.y
        )

    def update(self):

        if not self.held:

            self.vel.y += GRAVITY

            self.pos += self.vel

            self.vel *= FRICTION

            bottom_world_y = camera_offset.y + (HEIGHT / zoom)

            # FLOOR
            if self.pos.y + self.size.y > bottom_world_y:

                self.pos.y = bottom_world_y - self.size.y

                self.vel.y *= -0.5

            # WALLS
            if self.pos.x < -3000:

                self.pos.x = -3000
                self.vel.x *= -0.5

            if self.pos.x + self.size.x > 3000:

                self.pos.x = 3000 - self.size.x
                self.vel.x *= -0.5

    def draw(self):

        draw_rect = pygame.Rect(
            (self.pos.x - camera_offset.x) * zoom,
            (self.pos.y - camera_offset.y) * zoom,
            self.size.x * zoom,
            self.size.y * zoom
        )

        pygame.draw.rect(
            screen,
            (255, 180, 80),
            draw_rect
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            draw_rect,
            max(1, int(2 * zoom))
        )

        if self.held:

            pygame.draw.rect(
                screen,
                (255, 120, 120),
                draw_rect,
                4
            )

    def grab(self, mouse_world):

        self.held = True
        self.prev_mouse = mouse_world

    def drag(self, mouse_world):

        self.vel = mouse_world - self.prev_mouse

        self.pos += self.vel

        self.prev_mouse = mouse_world

    def release(self, mouse_world):

        self.held = False
        self.vel = (mouse_world - self.prev_mouse) * 0.6

# =========================
# COLLISIONS
# =========================
def resolve_ball_collision(a, b):

    delta = b.pos - a.pos
    dist = delta.length()

    min_dist = a.radius + b.radius

    if dist == 0 or dist >= min_dist:
        return

    overlap = min_dist - dist

    normal = delta.normalize()

    a.pos -= normal * (overlap / 2)
    b.pos += normal * (overlap / 2)

    rel_vel = b.vel - a.vel

    vel_along_normal = rel_vel.dot(normal)

    if vel_along_normal > 0:
        return

    impulse = vel_along_normal

    a.vel += normal * impulse
    b.vel -= normal * impulse

def resolve_rect_rect_collision(a, b):

    if not a.rect.colliderect(b.rect):
        return

    overlap_left = a.rect.right - b.rect.left
    overlap_right = b.rect.right - a.rect.left
    overlap_top = a.rect.bottom - b.rect.top
    overlap_bottom = b.rect.bottom - a.rect.top

    min_overlap = min(
        overlap_left,
        overlap_right,
        overlap_top,
        overlap_bottom
    )

    if min_overlap == overlap_left:

        a.pos.x -= overlap_left / 2
        b.pos.x += overlap_left / 2

        temp = a.vel.x
        a.vel.x = b.vel.x * 0.7
        b.vel.x = temp * 0.7

    elif min_overlap == overlap_right:

        a.pos.x += overlap_right / 2
        b.pos.x -= overlap_right / 2

        temp = a.vel.x
        a.vel.x = b.vel.x * 0.7
        b.vel.x = temp * 0.7

    elif min_overlap == overlap_top:

        a.pos.y -= overlap_top / 2
        b.pos.y += overlap_top / 2

        temp = a.vel.y
        a.vel.y = b.vel.y * 0.7
        b.vel.y = temp * 0.7

    elif min_overlap == overlap_bottom:

        a.pos.y += overlap_bottom / 2
        b.pos.y -= overlap_bottom / 2

        temp = a.vel.y
        a.vel.y = b.vel.y * 0.7
        b.vel.y = temp * 0.7

def resolve_racket_collision(ball, racket_rect, mouse_vel):

    closest_x = max(racket_rect.left, min(ball.pos.x, racket_rect.right))
    closest_y = max(racket_rect.top, min(ball.pos.y, racket_rect.bottom))

    closest = pygame.Vector2(closest_x, closest_y)

    delta = ball.pos - closest

    dist = delta.length()

    if dist == 0 or dist >= ball.radius:
        return

    normal = delta.normalize()

    penetration = ball.radius - dist

    ball.pos += normal * penetration

    vel_along_normal = ball.vel.dot(normal)

    if vel_along_normal < 0:

        ball.vel -= normal * (1.8 * vel_along_normal)

    ball.vel += mouse_vel * 0.45

def resolve_racket_rect_collision(rect_obj, racket_rect, mouse_vel):

    if rect_obj.rect.colliderect(racket_rect):

        center = pygame.Vector2(
            rect_obj.pos.x + rect_obj.size.x / 2,
            rect_obj.pos.y + rect_obj.size.y / 2
        )

        racket_center = pygame.Vector2(
            racket_rect.centerx,
            racket_rect.centery
        )

        delta = center - racket_center

        if delta.length() == 0:
            delta = pygame.Vector2(1, 0)

        normal = delta.normalize()

        rect_obj.vel += normal * 6
        rect_obj.vel += mouse_vel * 0.45

def collide_ball_with_line(ball, line):

    line_vec = line.end - line.start

    line_len = line_vec.length()

    if line_len == 0:
        return

    line_dir = line_vec.normalize()

    to_ball = ball.pos - line.start

    proj = max(0, min(line_len, to_ball.dot(line_dir)))

    closest = line.start + line_dir * proj

    delta = ball.pos - closest

    dist = delta.length()

    if dist < ball.radius and dist != 0:

        normal = delta.normalize()

        overlap = ball.radius - dist

        ball.pos += normal * overlap

        vel_dot = ball.vel.dot(normal)

        if vel_dot < 0:

            ball.vel -= 1.8 * vel_dot * normal

def collide_rect_with_line(rect_obj, line):

    line_vec = line.end - line.start

    line_len = line_vec.length()

    if line_len == 0:
        return

    line_dir = line_vec.normalize()

    rect_points = [

        pygame.Vector2(rect_obj.pos.x, rect_obj.pos.y),

        pygame.Vector2(
            rect_obj.pos.x + rect_obj.size.x,
            rect_obj.pos.y
        ),

        pygame.Vector2(
            rect_obj.pos.x,
            rect_obj.pos.y + rect_obj.size.y
        ),

        pygame.Vector2(
            rect_obj.pos.x + rect_obj.size.x,
            rect_obj.pos.y + rect_obj.size.y
        ),

        pygame.Vector2(
            rect_obj.pos.x + rect_obj.size.x / 2,
            rect_obj.pos.y + rect_obj.size.y / 2
        )
    ]

    for point in rect_points:

        to_point = point - line.start

        proj = max(
            0,
            min(line_len, to_point.dot(line_dir))
        )

        closest = line.start + line_dir * proj

        delta = point - closest

        dist = delta.length()

        COLLISION_THICKNESS = 18

        if dist < COLLISION_THICKNESS and dist != 0:

            normal = delta.normalize()

            push = COLLISION_THICKNESS - dist

            rect_obj.pos += normal * push

            vel_dot = rect_obj.vel.dot(normal)

            if vel_dot < 0:

                rect_obj.vel -= 1.9 * vel_dot * normal

                tangent = pygame.Vector2(
                    -normal.y,
                    normal.x
                )

                tangent_speed = rect_obj.vel.dot(tangent)

                rect_obj.vel -= tangent * tangent_speed * 0.04

def collide_ball_with_rect(ball, rect_obj):

    rect = rect_obj.rect

    closest_x = max(rect.left, min(ball.pos.x, rect.right))
    closest_y = max(rect.top, min(ball.pos.y, rect.bottom))

    closest = pygame.Vector2(closest_x, closest_y)

    delta = ball.pos - closest

    dist = delta.length()

    if dist == 0 or dist >= ball.radius:
        return

    normal = delta.normalize()

    overlap = ball.radius - dist

    ball.pos += normal * overlap

    vel_dot = ball.vel.dot(normal)

    if vel_dot < 0:

        ball.vel -= 1.8 * vel_dot * normal

        rect_obj.vel += normal * -vel_dot * 0.2

# =========================
# SETUP
# =========================
balls = [Ball(200 + i * 70, 200) for i in range(5)]

lines = []

rectangles = []

held_ball = None
held_rect = None

mode = GRAB_MODE

racket_size = pygame.Vector2(120, 120)

prev_mouse_world = pygame.Vector2()

line_start = None
rect_start = None

ball_size = 40

font = pygame.font.SysFont(None, 28)

# =========================
# LOOP
# =========================
running = True

while running:

    clock.tick(60)

    screen.fill((20, 20, 30))

    mouse_screen = pygame.Vector2(pygame.mouse.get_pos())

    mouse_world = screen_to_world(mouse_screen)

    mouse_vel = mouse_world - prev_mouse_world

    prev_mouse_world = mouse_world.copy()

    keys = pygame.key.get_pressed()

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ZOOM
        if event.type == pygame.MOUSEWHEEL:

            old_mouse_world = screen_to_world(mouse_screen)

            if keys[pygame.K_LSHIFT]:

                ball_size += event.y * 3
                ball_size = max(5, min(200, ball_size))

            else:

                zoom += event.y * 0.1
                zoom = max(0.2, min(3.0, zoom))

                new_mouse_world = screen_to_world(mouse_screen)

                camera_offset += old_mouse_world - new_mouse_world

        # MODE SWITCH
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                mode = GRAB_MODE

            if event.key == pygame.K_2:
                mode = RACKET_MODE

            if event.key == pygame.K_3:
                mode = LINE_MODE

            if event.key == pygame.K_4:
                mode = BALL_MODE

            if event.key == pygame.K_5:
                mode = DELETE_MODE

            if event.key == pygame.K_6:
                mode = RECT_MODE
            if event.key == pygame.K_r:
                lines = []
                rectangles = []
                balls = []

        # PAN
        if keys[pygame.K_p]:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                panning = True

                pan_start_mouse = pygame.Vector2(pygame.mouse.get_pos())

                pan_start_offset = camera_offset.copy()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                panning = False

        # GRAB MODE
        if mode == GRAB_MODE and not panning:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                held_rect = None
                held_ball = None

                for rect in reversed(rectangles):

                    if rect.rect.collidepoint(mouse_world):

                        held_rect = rect
                        rect.grab(mouse_world)
                        break

                if held_rect is None:

                    for ball in reversed(balls):

                        if ball.pos.distance_to(mouse_world) <= ball.radius + 60:

                            held_ball = ball
                            ball.grab(mouse_world)
                            break

            if event.type == pygame.MOUSEBUTTONUP:

                if held_ball:

                    held_ball.release(mouse_world)
                    held_ball = None

                if held_rect:

                    held_rect.release(mouse_world)
                    held_rect = None

        # LINE MODE
        if mode == LINE_MODE and not panning:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if line_start is None:

                    line_start = mouse_world.copy()

                else:

                    lines.append(Line(line_start, mouse_world))
                    line_start = None

        # BALL MODE
        if mode == BALL_MODE and not panning:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                balls.append(
                    Ball(mouse_world.x, mouse_world.y, ball_size)
                )

        # RECT MODE
        if mode == RECT_MODE and not panning:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                rect_start = mouse_world.copy()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                if rect_start is not None:

                    width = mouse_world.x - rect_start.x
                    height = mouse_world.y - rect_start.y

                    x = rect_start.x
                    y = rect_start.y

                    if width < 0:
                        x += width
                        width *= -1

                    if height < 0:
                        y += height
                        height *= -1

                    if width > 10 and height > 10:

                        rectangles.append(
                            PhysicsRect(x, y, width, height)
                        )

                    rect_start = None

        # DELETE MODE
        if mode == DELETE_MODE and not panning:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                for ball in reversed(balls):

                    if ball.pos.distance_to(mouse_world) <= ball.radius:

                        balls.remove(ball)
                        break

                for line in reversed(lines):

                    if distance_to_line(
                        mouse_world,
                        line.start,
                        line.end
                    ) < 10 / zoom:

                        lines.remove(line)
                        break

                for rect in reversed(rectangles):

                    if rect.rect.collidepoint(mouse_world):

                        rectangles.remove(rect)
                        break

    # CAMERA PAN
    if panning:

        mouse_now = pygame.Vector2(pygame.mouse.get_pos())

        delta = (mouse_now - pan_start_mouse) / zoom

        camera_offset = pan_start_offset - delta

    # DRAG
    if mode == GRAB_MODE:

        if held_ball:
            held_ball.drag(mouse_world)

        if held_rect:
            held_rect.drag(mouse_world)

    # RACKET
    racket_rect = pygame.Rect(
        mouse_world.x - racket_size.x // 2,
        mouse_world.y - racket_size.y // 2,
        racket_size.x,
        racket_size.y
    )

    if mode == RACKET_MODE:

        for ball in balls:
            resolve_racket_collision(ball, racket_rect, mouse_vel)

        for rect in rectangles:
            resolve_racket_rect_collision(
                rect,
                racket_rect,
                mouse_vel
            )

    # UPDATE
    for ball in balls:
        ball.update()

    for rect in rectangles:
        rect.update()

    # BALL-BALL
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            resolve_ball_collision(balls[i], balls[j])

    # RECT-RECT
    for i in range(len(rectangles)):
        for j in range(i + 1, len(rectangles)):
            resolve_rect_rect_collision(
                rectangles[i],
                rectangles[j]
            )

    # LINE COLLISIONS
    for line in lines:

        for ball in balls:
            collide_ball_with_line(ball, line)

        for rect in rectangles:
            collide_rect_with_line(rect, line)

    # BALL-RECT
    for rect in rectangles:

        for ball in balls:
            collide_ball_with_rect(ball, rect)

    # DRAW LINES
    for line in lines:
        line.draw()

    # PREVIEW LINE
    if line_start is not None:

        pygame.draw.line(
            screen,
            (100, 255, 100),
            world_to_screen(line_start),
            mouse_screen,
            3
        )

    # DRAW RECTS
    for rect in rectangles:
        rect.draw()

    # RECT PREVIEW
    if mode == RECT_MODE and rect_start is not None:

        preview_rect = pygame.Rect(
            world_to_screen(rect_start).x,
            world_to_screen(rect_start).y,
            mouse_screen.x - world_to_screen(rect_start).x,
            mouse_screen.y - world_to_screen(rect_start).y
        )

        pygame.draw.rect(
            screen,
            (100, 255, 100),
            preview_rect,
            2
        )

    # DRAW BALLS
    for ball in balls:
        ball.draw()

    # DRAW RACKET
    if mode == RACKET_MODE:

        draw_rect = pygame.Rect(
            (racket_rect.x - camera_offset.x) * zoom,
            (racket_rect.y - camera_offset.y) * zoom,
            racket_rect.width * zoom,
            racket_rect.height * zoom
        )

        pygame.draw.rect(
            screen,
            (255, 120, 120),
            draw_rect,
            border_radius=8
        )

    # BALL PREVIEW
    if mode == BALL_MODE:

        pygame.draw.circle(
            screen,
            (100, 255, 100),
            mouse_screen,
            int(ball_size * zoom),
            2
        )

    # UI
    mode_names = {
        GRAB_MODE: "GRAB",
        RACKET_MODE: "RACKET",
        LINE_MODE: "LINE",
        BALL_MODE: "BALL CREATE",
        DELETE_MODE: "DELETE",
        RECT_MODE: "RECT CREATE"
    }

    ui = [
        f"MODE: {mode_names[mode]}",
        "1 = Grab",
        "2 = Racket",
        "3 = Line",
        "4 = Create Ball",
        "5 = Delete",
        "6 = Create Rectangles",
        "SHIFT + Mouse Wheel = Change Ball Size",
        "Mouse Wheel = Zoom",
        "Hold P + Drag = Pan",
        f"Ball Size: {ball_size}"
    ]

    y = 10

    for text in ui:

        img = font.render(text, True, (230, 230, 230))

        screen.blit(img, (10, y))

        y += 28

    pygame.display.flip()

pygame.quit()
