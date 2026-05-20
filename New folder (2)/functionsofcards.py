import pygame
import math
pygame.init()

running = True
screen = pygame.display.set_mode([1280, 720])
def button(x, y, w, h, text):

    but = pygame.Rect(x, y, w, h)

    # ===== Shadow =====
    pygame.draw.rect(screen, (20, 20, 20),
                     (x + 5, y + 5, w, h),
                     border_radius=10)

    # ===== Outer Border =====
    pygame.draw.rect(screen, (210, 180, 60),
                     but,
                     border_radius=10)

    # ===== Main Button =====
    inner = pygame.Rect(x + 3, y + 3, w - 6, h - 6)

    pygame.draw.rect(screen, (30, 120, 60),
                     inner,
                     border_radius=8)

    # ===== Top Highlight =====
    pygame.draw.rect(screen, (60, 180, 100),
                     (x + 6, y + 6, w - 12, h // 3),
                     border_radius=6)

    # ===== Inner Outline =====
    pygame.draw.rect(screen, (10, 70, 35),
                     inner,
                     width=2,
                     border_radius=8)

    # ===== Text =====
    font = pygame.font.SysFont("arial", 28, bold=True)

    txt = font.render(text, True, (255, 255, 255))
    txt_rect = txt.get_rect(center=but.center)

    screen.blit(txt, txt_rect)
    ex, ey = pygame.mouse.get_pos()
    if but.collidepoint(ex,ey):
        
        return True
    return False
    
def draw_card(x, y, suit, chara):
    card_rect = pygame.Rect(x, y, 50, 80)
    suit_color = (255,0,0)
    if suit == "S" or suit == "C":
        suit_color = (0,0,0)
    pygame.draw.rect(screen, (255,255,255), card_rect)
    pygame.draw.rect(screen, suit_color, card_rect,5)
    pygame.draw.rect(screen, (255,255,255), card_rect,1)
    font = pygame.freetype.SysFont("arial", 38)
    font.render_to(
    screen,              # surface to draw on
    (x+15, y+10),          # position
    chara,       # text
    (suit_color)      # color
    )

    fonter = pygame.freetype.SysFont("Segoe UI Emoji", 38)
    if suit == "C":
        char = "♣"
    if suit == "S":
        char = "♠"
    if suit == "H":
        char = "♥"
    if suit == "D":
        char = "♦"
    font.render_to(
    screen,              # surface to draw on
    (x+15, y+40),          # position
    char,       # text
    (suit_color)      # color
    )
    
        
while running:
    draw_card(300,300,"D", "7")
    if button(400,400,400,100, "hi"):
        print("hover")
    pygame.display.flip()

pygame.quit()
