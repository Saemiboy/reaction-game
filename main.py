import pygame
import game_utils

# --- Initialisierung ---
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stop the Light")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
FPS = 60

# --- Farben ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

def spiel():
    game = game_utils.Game(WIDTH, HEIGHT, FONT)
    while game.running:
        dt = clock.tick(FPS) / 1000  # Sekunden seit letztem Frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            game.handle_input(event)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    # Spielende
    screen.fill(WHITE)
    end_text = FONT.render(f"Game Over!", True, BLUE)
    zeit_text = FONT.render(f'Benötigte Zeit: {game.vergangeneZeit}S', True, BLUE)
    runden_text = FONT.render(f'Anzahl benötigter Runden: {game.rounds} Runden', True, BLUE)
    screen.blit(end_text, (0, HEIGHT // 2 - end_text.get_height() - 10))
    screen.blit(zeit_text, (0, HEIGHT // 2 - (zeit_text.get_height() // 2)))
    screen.blit(runden_text, (0, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    spiel()
    pygame.quit()

if __name__ == "__main__":
    main()