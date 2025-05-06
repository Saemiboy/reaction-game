import pygame
import random


class Maingame:
    WIDTH, HEIGHT = 500, 500
    FPS = 60
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        # Pygame Praeambel
        pygame.init()
        self.mainscreen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.running = True

        # Spielvariabeln
        self.directions = ['up', 'down', 'left', 'right']
        self.choice = random.choice(self.directions)
        self.key_type = None
        self.arrow_starttime = 0
        self.reactiontime = 0
        self.score = 0
        self.waitingInput = True
        self.correct = (
            (self.choice == 'up' and self.key_type == pygame.K_UP) or
            (self.choice == 'down' and self.key_type == pygame.K_DOWN) or
            (self.choice == 'left' and self.key_type == pygame.K_LEFT) or
            (self.choice == 'right' and self.key_type == pygame.K_RIGHT)
        )

    def main(self):
        while self.running:
            self.mainscreen.fill(self.WHITE)
            zeit_aktuell = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and self.waitingInput:
                    self.key_type = event.key

                    if self.correct:
                        self.reactiontime = zeit_aktuell - self.arrow_starttime
                        self.score = max(0, 1000-self.reactiontime)
                        print(self.score)
                        self.waitingInput = False

            # Pfeil anzeigen (nur textlich hier)
            text = self.font.render(self.choice.upper(), True, self.BLACK)
            self.mainscreen.blit(text, (150, 180))

            # Score anzeigen
            score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
            self.mainscreen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

                    

game = Maingame()
game.main()
