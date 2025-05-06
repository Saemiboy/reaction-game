import pygame
import random

# --- Initialisierung ---
pygame.init()
WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stop the Light")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)

# --- Farben ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

# --- Klassen ---

class TargetZone:
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y = 90
        self.height = 20

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))


class LightBar:
    def __init__(self, width):
        self.x = 0
        self.y = 90
        self.radius = 10
        self.speed = 250  # Pixel pro Sekunde
        self.direction = 1  # 1 = rechts, -1 = links
        self.width = width

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        if self.x <= 0:
            self.x = 0
            self.direction *= -1
        elif self.x >= self.width:
            self.x = self.width
            self.direction *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), self.y + 10), self.radius)


class Game:
    def __init__(self):
        self.light = LightBar(WIDTH)
        self.reset_target()
        self.score = 0
        self.rounds = 0
        self.max_rounds = 10
        self.running = True

    def reset_target(self):
        target_x = random.randint(100, WIDTH - 150)
        target_width = random.randint(40, 100)
        self.target = TargetZone(target_x, target_width)

    def check_hit(self):
        light_pos = self.light.x
        in_zone = self.target.x <= light_pos <= (self.target.x + self.target.width)
        return in_zone

    def update(self, dt):
        self.light.update(dt)

    def draw(self, surface):
        surface.fill(WHITE)
        self.target.draw(surface)
        self.light.draw(surface)

        score_text = FONT.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (10, 10))

        round_text = FONT.render(f"Round: {self.rounds}/{self.max_rounds}", True, BLACK)
        surface.blit(round_text, (10, 50))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.rounds += 1
            if self.check_hit():
                self.score += 1
            if self.rounds < self.max_rounds:
                self.reset_target()
            else:
                self.running = False


# --- Hauptspielschleife ---

def main():
    game = Game()
    while game.running:
        dt = clock.tick(60) / 1000  # Sekunden seit letztem Frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            game.handle_input(event)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    # Spielende
    screen.fill(WHITE)
    end_text = FONT.render(f"Game Over! Final Score: {game.score}", True, BLUE)
    screen.blit(end_text, (WIDTH // 2 - 160, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
