# ===== Binary Adder =====
import pygame

Bits = 6
OutBits = Bits + 1

bitlista = [0]*Bits
bitlistb = [0]*Bits
output = [0]*OutBits

WIDTH = 150
HEIGHT = OutBits * 50

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Binary Adder")
clock = pygame.time.Clock()

running = True

def xor(a, b):
    return (a and not b) or (b and not a)

while running:
    clock.tick(60)
    window.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:

            # Toggle A bits
            for i in range(Bits):
                rect = pygame.Rect(50, (Bits-1-i)*50+50, 50, 50)
                if rect.collidepoint(mx,my):
                    bitlista[i] ^= 1

            # Toggle B bits
            for i in range(Bits):
                rect = pygame.Rect(100, (Bits-1-i)*50+50, 50, 50)
                if rect.collidepoint(mx,my):
                    bitlistb[i] ^= 1

    # ---------- ADDER LOGIC ----------
    carry = 0
    for i in range(Bits):
        a = bitlista[i]
        b = bitlistb[i]

        output[i] = xor(xor(a,b), carry)
        carry = (a and b) or (carry and xor(a,b))

    output[Bits] = carry   # extra MSB carry

    # ---------- DRAW A ----------
    for i in range(Bits):
        rect = pygame.Rect(50, (Bits-1-i)*50+50, 50, 50)
        pygame.draw.rect(window, (255,255,255) if bitlista[i] else (0,0,0), rect)
        pygame.draw.rect(window, (255,255,255), rect, 2)

    # ---------- DRAW B ----------
    for i in range(Bits):
        rect = pygame.Rect(100, (Bits-1-i)*50+50, 50, 50)
        pygame.draw.rect(window, (255,255,255) if bitlistb[i] else (0,0,0), rect)
        pygame.draw.rect(window, (255,255,255), rect, 2)

    # ---------- DRAW OUTPUT ----------
    for i in range(OutBits):
        rect = pygame.Rect(0, (OutBits-1-i)*50, 50, 50)
        pygame.draw.rect(window, (255,255,255) if output[i] else (0,0,0), rect)
        pygame.draw.rect(window, (255,255,255), rect, 2)

    pygame.display.flip()

pygame.quit()
