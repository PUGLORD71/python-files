import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My First Pygame Window")

window = pygame.display.set_mode((600, 400))
pygame.display.set_caption("My First Pygame Window")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

