import pygame
import random
import sys

pygame.init()

# --- CONSTANTS ---
WIDTH, HEIGHT = 800, 600
LANES = [200, 400, 600]
PLAYER_Y = 450
GRAVITY = 0.8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers Lite")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# --- PLAYER ---
class Player:
    def __init__(self):
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = PLAYER_Y
        self.vel_y = 0
        self.jumping = False
        self.rolling = False
        self.on_train = False
        self.rect = pygame.Rect(self.x - 25, self.y - 50, 50, 50)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 2:
            self.lane += 1

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

    def roll(self):
        self.rolling = True

    def update(self):
        self.x = LANES[self.lane]

        # Gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Ground / Train height
        ground = PLAYER_Y - (100 if self.on_train else 0)

        if self.y >= ground:
            self.y = ground
            self.vel_y = 0
            self.jumping = False

        self.rect.topleft = (self.x - 25, self.y - 50)

    def draw(self, screen):
        color = (0, 200, 255) if not self.rolling else (255, 200, 0)
        pygame.draw.rect(screen, color, self.rect)


# --- OBJECTS ---
class Obstacle:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -50
        self.type = random.choice(["hurdle", "train", "ramp"])
        self.rect = pygame.Rect(self.x - 30, self.y, 60, 60)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x - 30, self.y)

    def draw(self, screen):
        if self.type == "hurdle":
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        elif self.type == "train":
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 40, self.y, 80, 120))
        elif self.type == "ramp":
            pygame.draw.polygon(screen, (0, 255, 0),
                                [(self.x - 30, self.y + 60),
                                 (self.x + 30, self.y + 60),
                                 (self.x, self.y)])


class Coin:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -50
        self.rect = pygame.Rect(self.x - 10, self.y, 20, 20)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x - 10, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 215, 0), self.rect.center, 10)


# --- MENU ---
def main_menu():
    while True:
        screen.fill((30, 30, 30))
        title = font.render("Subway Surfers Lite", True, (255, 255, 255))
        start = font.render("Press SPACE to Start", True, (200, 200, 200))

        screen.blit(title, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(start, (WIDTH//2 - 170, HEIGHT//2 + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


# --- GAME LOOP ---
def game():
    player = Player()
    obstacles = []
    coins = []
    speed = 8
    score = 0

    spawn_timer = 0

    while True:
        screen.fill((50, 50, 70))

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_DOWN:
                    player.roll()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.rolling = False

        # --- SPAWN ---
        spawn_timer += 1
        if spawn_timer > 10:
            obstacles.append(Obstacle())
            if random.random() < 0.7:
                coins.append(Coin())
            spawn_timer = 0

        # --- UPDATE ---
        player.on_train = False

        for obs in obstacles[:]:
            obs.update(speed)

            # Train top logic
            if obs.type == "train":
                train_rect = pygame.Rect(obs.x - 40, obs.y, 80, 120)
                if player.rect.colliderect(train_rect):
                    player.on_train = True

            # Ramp jump boost
            if obs.type == "ramp" and player.rect.colliderect(obs.rect):
                player.vel_y = -20

            # Collision
            if obs.type == "hurdle" and player.rect.colliderect(obs.rect):
                if not player.jumping and not player.rolling:
                    return  # game over

            if obs.y > HEIGHT:
                obstacles.remove(obs)

        for coin in coins[:]:
            coin.update(speed)
            if player.rect.colliderect(coin.rect):
                score += 1
                coins.remove(coin)

            elif coin.y > HEIGHT:
                coins.remove(coin)

        player.update()

        # --- DRAW ---
        for lane in LANES:
            pygame.draw.line(screen, (100, 100, 100), (lane, 0), (lane, HEIGHT), 2)

        for obs in obstacles:
            obs.draw(screen)

        for coin in coins:
            coin.draw(screen)

        player.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


# --- RUN ---
while True:
    main_menu()
    game()


