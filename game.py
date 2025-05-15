import pygame
from game_utils import Game, Gameover
from start_utils import Home
from db_utils import DBClient

# --- Initialisierung Muss alles auf None setzen damit alles im gleichen Thread abläuft da mit tkinter und pygame zusammen läuft---
FONT = None
WIDTH, HEIGHT = 700, 600
screen = None
clock = None
FONT = None
FPS = 60
mainswitch = True
client = None


def spiel(userid, spieler):
    global mainswitch
    if not mainswitch:
        return
    game = Game(WIDTH, HEIGHT, FONT)
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
    game_over = Gameover(game.vergangeneZeit, game.rounds, FONT)
    game_over.show(screen)
    client.insert_game((userid, game.rounds, game.vergangeneZeit), spieler=spieler)


def start(username):
    global mainswitch
    highscore = client.fetch_highscore()

    start = Home(WIDTH, HEIGHT, FONT, highscore, username)
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

def main_game(userid, username, spieler):
    global mainswitch, FONT, screen, clock, client
    
    # Initialisierung in der Funktion damit dies nicht früher schon geschieht
    # Pygame soll nicht gleichzeitig wie tkinter laufen
    # wenn ein import gemacht wird würde alles oben schon ausgeführt werden.
    pygame.init()
    FONT = pygame.font.SysFont(None, 36)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stop the Light")
    clock = pygame.time.Clock()
    client = DBClient()

    while mainswitch:
        start(username)
        spiel(userid, spieler)
    client.close()

# Testklausel
if __name__ == '__main__':
    main_game(2, 'Sanguel', True)
