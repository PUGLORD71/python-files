import pygame
import math

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
FOV = 400
FOCAL_LENGTH = 2.75   # <-- CHANGE THIS to scale the scene
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------------- 3D GENERATORS ----------------
def low_poly_sphere(segments=8, rings=6):
    pts, edges = [], []
    for i in range(rings + 1):
        lat = math.pi * i / rings
        for j in range(segments):
            lon = 2 * math.pi * j / segments
            pts.append([
                math.sin(lat) * math.cos(lon),
                math.cos(lat),
                math.sin(lat) * math.sin(lon)
            ])

    def idx(r, s): return r * segments + s
    for r in range(rings):
        for s in range(segments):
            edges += [(idx(r,s), idx(r,(s+1)%segments)),
                      (idx(r,s), idx(r+1,s))]
    return pts, edges

def low_poly_cylinder(segments=10):
    pts, edges = [], []
    for y in (-1,1):
        for i in range(segments):
            a = 2 * math.pi * i / segments
            pts.append([math.cos(a), y, math.sin(a)])
    for i in range(segments):
        edges += [
            (i,(i+1)%segments),
            (i+segments,(i+1)%segments+segments),
            (i,i+segments)
        ]
    return pts, edges

# ---------------- 4D OBJECTS ----------------
def tesseract():
    pts, edges = [], []
    for x in (-1,1):
        for y in (-1,1):
            for z in (-1,1):
                for w in (-1,1):
                    pts.append([x,y,z,w])
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            if sum(pts[i][k] != pts[j][k] for k in range(4)) == 1:
                edges.append((i,j))
    return pts, edges

def pentachoron():
    pts = [
        [1,1,1,-1],[1,-1,-1,-1],
        [-1,1,-1,-1],[-1,-1,1,-1],
        [0,0,0,2]
    ]
    edges = [(i,j) for i in range(5) for j in range(i+1,5)]
    return pts, edges

def cell16():
    pts = [
        [1,0,0,0],[-1,0,0,0],
        [0,1,0,0],[0,-1,0,0],
        [0,0,1,0],[0,0,-1,0],
        [0,0,0,1],[0,0,0,-1]
    ]
    edges = [(i,j) for i in range(8) for j in range(i+1,8)
             if sum(abs(pts[i][k]-pts[j][k]) for k in range(4)) == 2]
    return pts, edges

# ---------------- OBJECT LIST ----------------
sphere_pts, sphere_edges = low_poly_sphere()
cyl_pts, cyl_edges = low_poly_cylinder()

OBJECTS = [
    ("cube",
     [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
      [-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],
     [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
      (0,4),(1,5),(2,6),(3,7)], 3),

    ("pyramid",
     [[0,1,0],[-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1]],
     [(0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4),(4,1)], 3),

    ("tetrahedron",
     [[1,1,1],[-1,-1,1],[-1,1,-1],[1,-1,-1]],
     [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)], 3),

    ("octahedron",
     [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],
     [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),
      (2,4),(2,5),(3,4),(3,5)], 3),

    ("prism",
     [[-1,-1,-1],[1,-1,-1],[0,1,-1],[-1,-1,1],[1,-1,1],[0,1,1]],
     [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)], 3),

    ("cylinder", cyl_pts, cyl_edges, 3),
    ("sphere", sphere_pts, sphere_edges, 3),
    ("tesseract", *tesseract(), 4),
    ("pentachoron", *pentachoron(), 4),
    ("16-cell", *cell16(), 4)
]

# ---------------- ROTATION ----------------
def rot2(a,b,t):
    c,s = math.cos(t), math.sin(t)
    return a*c - b*s, a*s + b*c

def rotate_3d(p, ax, ay, az):
    x,y,z = p
    y,z = rot2(y,z,ax)
    x,z = rot2(x,z,ay)
    x,y = rot2(x,y,az)
    return [x,y,z]

def rotate_4d(p, ax, ay, az, aw):
    x,y,z,w = p
    x,w = rot2(x,w,aw)
    y,z = rot2(y,z,ax)
    x,z = rot2(x,z,ay)
    x,y = rot2(x,y,az)
    return [x,y,z,w]

# ---------------- PROJECTION ----------------
def project_4d_to_3d(p):
    x,y,z,w = p
    w += FOCAL_LENGTH
    f = 1 / w
    return [x*f, y*f, z*f]

def project_3d_to_2d(p):
    x,y,z = p
    z += FOCAL_LENGTH
    f = FOV / z
    return int(x*f + CENTER[0]), int(-y*f + CENTER[1])

# ---------------- MAIN ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D / 4D Wireframe Viewer (Focal Length)")
clock = pygame.time.Clock()

ax=ay=az=aw=0
current = 0
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if pygame.K_0 <= e.key <= pygame.K_9:
                idx = e.key - pygame.K_1
                if idx < len(OBJECTS):
                    current = idx
            if e.key == pygame.K_r:
                ax=ay=az=aw=0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: ax += 0.02
    if keys[pygame.K_s]: ax -= 0.02
    if keys[pygame.K_d]: ay += 0.02
    if keys[pygame.K_a]: ay -= 0.02
    if keys[pygame.K_q]: az += 0.02
    if keys[pygame.K_e]: az -= 0.02
    if keys[pygame.K_z]: aw += 0.02
    if keys[pygame.K_x]: aw -= 0.02

    name, pts, edges, dim = OBJECTS[current]
    proj = []

    for p in pts:
        if dim == 4:
            r4 = rotate_4d(p,ax,ay,az,aw)
            r3 = project_4d_to_3d(r4)
        else:
            r3 = rotate_3d(p,ax,ay,az)
        proj.append(project_3d_to_2d(r3))

    for a,b in edges:
        pygame.draw.line(screen, WHITE, proj[a], proj[b], 2)

    pygame.display.flip()

pygame.quit()
