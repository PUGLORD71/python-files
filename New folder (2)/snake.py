import pygame
import random

# ------------------ SETUP ------------------
pygame.init()
WIDTH, HEIGHT = 500, 500
CELL = 50
ROWS = WIDTH // CELL
COLS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
speed = 5

# Colors
BG = (20, 20, 20)
SNAKE_COLOR = (0, 220, 220)
FOOD_COLOR = (220, 50, 50)
TEXT = (240, 240, 240)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

state = MENU

MAX_LENGTH = ROWS * COLS

# ------------------ HELPERS ------------------
def get_free_cells(snake, apples):
    free = []
    for x in range(0, WIDTH, CELL):
        for y in range(0, HEIGHT, CELL):
            pos = (x, y)
            if pos not in snake and pos not in apples:
                free.append(pos)
    return free


def spawn_food(snake, apples):
    free = get_free_cells(snake, apples)
    if not free:
        return None
    return random.choice(free)


APPLE_COUNT = 20
def reset_game():
    snake = [(CELL * 3, 0), (0, CELL * 2), (0, CELL)]
    direction = (CELL, 0)
    food = []
    while len(food) < APPLE_COUNT:
        pos = spawn_food(snake,food)
        if pos not in food:
            food.append(pos)
    return snake, direction, food

snake, direction, food = reset_game()

# ------------------ GAME LOOP ------------------
running = True
while running:
    clock.tick(speed)
    screen.fill(BG)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == MENU and event.key == pygame.K_SPACE:
                snake, direction, food = reset_game()
                state = PLAYING

            elif state in (GAME_OVER, WIN) and event.key == pygame.K_SPACE:
                snake, direction, food = reset_game()
                state = PLAYING

            elif state == PLAYING:
                if event.key == pygame.K_w and direction != (0, CELL):
                    direction = (0, -CELL)
                elif event.key == pygame.K_s and direction != (0, -CELL):
                    direction = (0, CELL)
                elif event.key == pygame.K_a and direction != (CELL, 0):
                    direction = (-CELL, 0)
                elif event.key == pygame.K_d and direction != (-CELL, 0):
                    direction = (CELL, 0)

    # -------- STATES --------
    if state == MENU:
        title = font.render("SNAKE", True, TEXT)
        start = small_font.render("Press SPACE to Start", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 220))
        screen.blit(start, (WIDTH//2 - start.get_width()//2, 280))

    elif state == PLAYING:
        # Move snake
        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)

        # Wall / self collision
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake
        ):
            state = GAME_OVER
        else:
            snake.insert(0, new_head)

            # Food collision
            ate_food = False

            for i, f in enumerate(food):
                if new_head == f:
                    ate_food = True
                    food.pop(i)

                    # Respawn apple ONLY if space exists
                    new_food = spawn_food(snake, food)
                    if new_food is not None:
                        food.append(new_food)

                    break

            if not ate_food:
                snake.pop()
            if len(snake) == MAX_LENGTH:
                pygame.time.wait(1000)
                state = WIN




            

        # Draw food
        for f in food:
            pygame.draw.rect(screen, FOOD_COLOR, (*f, CELL, CELL))

        # Draw snake
        for i, segment in enumerate(snake):
            shade = max(60, 255 - i * int(CELL / 25))
            pygame.draw.rect(
                screen,
                (0, shade, 200),
                (*segment, CELL, CELL)
            )

        # Progress text
        progress = small_font.render(
            f"{len(snake)}/{MAX_LENGTH}", True, TEXT
        )
        screen.blit(progress, (10, 10))

    elif state == GAME_OVER:
        over = font.render("GAME OVER", True, TEXT)
        retry = small_font.render("Press SPACE to Retry", True, TEXT)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, 220))
        screen.blit(retry, (WIDTH//2 - retry.get_width()//2, 280))

    elif state == WIN:
        win = font.render("YOU WIN!", True, TEXT)
        retry = small_font.render("Press SPACE to Play Again", True, TEXT)
        screen.blit(win, (WIDTH//2 - win.get_width()//2, 220))
        screen.blit(retry, (WIDTH//2 - retry.get_width()//2, 280))

    pygame.display.flip()

pygame.quit()
