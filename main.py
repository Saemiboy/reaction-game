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

def spiel():
    game = game_utils.Game(WIDTH, HEIGHT, FONT)
    while game.running:
        dt = clock.tick(FPS) / 1000  # Sekunden seit letztem Frame

        for event in pygame.event.get():
            game.handle_input(event)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    # Spielende
    game_over = game_utils.Gameover(game.vergangeneZeit, game.rounds, FONT)
    game_over.show(screen)

def main():
    spiel()
    pygame.quit()

if __name__ == "__main__":
    main()