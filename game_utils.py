import pygame
import random

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


class GameZone:
    def __init__(self, width):
        self.x = 0
        self.width = width
        self.height = 20
        self.y = 90

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height))


class LightBar:
    def __init__(self, width):
        self.x = 0
        self.y = 90
        self.radius = 5
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
        pygame.draw.rect(surface, RED, (self.x, self.y, self.radius, 20))


class Game:
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.light = LightBar(self.width)
        self.gameZone = GameZone(self.width)
        self.score = 0
        self.rounds = 0
        self.max_rounds = 5
        self.running = True
        self.startzeit = pygame.time.get_ticks()
        self.vergangeneZeit = 0
        self.reset_target()

    def reset_target(self):
        target_x = random.randint(100, self.width - 150)
        target_width = random.randint(40, 100)
        self.target = TargetZone(target_x, target_width)
        self.light.x = 0 if self.rounds % 2 == 1 else self.gameZone.width

    def check_hit(self):
        light_pos = self.light.x
        in_zone = self.target.x <= light_pos <= (self.target.x + self.target.width)
        return in_zone

    def update(self, dt):
        self.light.update(dt)
        self.vergangeneZeit = (pygame.time.get_ticks() - self.startzeit) / 1000

    def draw(self, surface):
        surface.fill(WHITE)
        self.gameZone.draw(surface)
        self.target.draw(surface)
        self.light.draw(surface)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (10, 10))

        zeit_text = self.font.render(f'Vergangene Zeit: {self.vergangeneZeit}', True, BLACK)
        surface.blit(zeit_text, (100, 10))

        round_text = self.font.render(f"Round: {self.rounds}/{self.max_rounds}", True, BLACK)
        surface.blit(round_text, (10, 50))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.rounds += 1
            if self.check_hit():
                self.score += 1
            if self.score < self.max_rounds:
                self.reset_target()
                self.light.speed = (2.5*(self.score**2) + 250) # Kurve damit der Ball schneller wird
            else:
                self.running = False

class Gameover:
    def __init__(self, endzeit, rounds, font):
        self.endzeit = endzeit
        self.rounds = rounds
        self.font = font

    def show(self, screen):
        screen.fill(WHITE)
        end_text = self.font.render(f"Game Over!", True, BLUE)
        zeit_text = self.font.render(f'Benötigte Zeit: {self.endzeit}S', True, BLUE)
        runden_text = self.font.render(f'Anzahl benötigter Runden: {self.rounds} Runden', True, BLUE)
        screen.blit(end_text, (0, screen.get_height() // 2 - end_text.get_height() - 10))
        screen.blit(zeit_text, (0, screen.get_height() // 2 - (zeit_text.get_height() // 2)))
        screen.blit(runden_text, (0, screen.get_height() // 2 + 10))
        pygame.display.flip()
        pygame.time.wait(3000)




