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

    def main(self):
        while self.running:
            self.mainscreen.fill(self.WHITE)
            zeit_aktuell = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and self.waitingInput:
                    if self.check_correct(event.key):
                        self.reactiontime = zeit_aktuell - self.arrow_starttime
                        self.score = max(0, 1000-self.reactiontime)
                        print(self.score, 'asdfasdf')
                        self.waitingInput = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.waitingInput:
                        self.new_direction()
                

            # Pfeil anzeigen (nur textlich hier)
            text = self.font.render(self.choice.upper(), True, self.BLACK)
            self.mainscreen.blit(text, (250, 250))

            # Score anzeigen
            score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
            self.mainscreen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)

    def new_direction(self):
        self.choice = random.choice(self.directions)
        self.arrow_starttime = pygame.time.get_ticks()
        self.waitingInput = True

    def check_correct(self, key):
        if (
            (self.choice == 'up' and key == pygame.K_UP) or
            (self.choice == 'down' and key == pygame.K_DOWN) or
            (self.choice == 'left' and key == pygame.K_LEFT) or
            (self.choice == 'right' and key == pygame.K_RIGHT)
        ): 
            return True
        else:
            return False


                    

game = Maingame()
game.main()
