import pygame
import game_utils
import start_utils

# --- Initialisierung ---
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stop the Light")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
FPS = 60
mainswitch = True

testliste = [
    (2312, "asdfas", '24-01-01'),
    (2312, "sdff", '24-01-01'),
    (2312, "dd", '24-01-01'),
    (2312, "gadsghwwe", '24-01-01'),
    (2312, "asdcasdfghasd", '24-01-01'),
]

def spiel():
    global mainswitch
    if not mainswitch:
        return
    game = game_utils.Game(WIDTH, HEIGHT, FONT)
    while game.running:
        dt = clock.tick(FPS) / 1000  # Sekunden seit letztem Frame

        for event in pygame.event.get():
            game.handle_input(event)
            if event.type == pygame.QUIT:
                game.running = False
                mainswitch = False
                pygame.quit()
                return

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    # Spielende
    game_over = game_utils.Gameover(game.vergangeneZeit, game.rounds, FONT)
    game_over.show(screen)

def start():
    global mainswitch

    start = start_utils.Home(WIDTH, HEIGHT, FONT, testliste)
    while start.running:
        for event in pygame.event.get():
            start.input_handler(event)
            if event.type == pygame.QUIT:
                start.running = False
                mainswitch = False
                pygame.quit()
                return

        start.update()
        start.show(screen)
        pygame.display.flip()



def main():
    global mainswitch
    while mainswitch:
        start()
        spiel()

    
if __name__ == "__main__":
    main()