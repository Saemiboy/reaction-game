import pygame
import game_utils
import start_utils
from db_utils import DBClient
from login_utils import TkinterLogin

# --- Initialisierung ---
pygame.init()
FONT = pygame.font.SysFont(None, 36)
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stop the Light")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
FPS = 60
mainswitch = True
client = DBClient()
userid = None
spieler = None


def spiel():
    global mainswitch, spieler, userid
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
    client.insert_game((userid, game.rounds, game.vergangeneZeit), spieler=spieler)


def start():
    global mainswitch
    highscore = client.fetch_highscore()

    start = start_utils.Home(WIDTH, HEIGHT, FONT, highscore)
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

def login():
    global userid, spieler
    newlogin = TkinterLogin()
    answer = newlogin.show()

    if answer[0] == 'Guest':
        client.get_GaesteID(answer[2])
        spieler = False
    else:
        client.get_SpielerID(answer[2])
        spieler = True




def main_game():
    global mainswitch
    login()

    while mainswitch:
        start()
        spiel()
    client.close()

if __name__ == "__main__":
    main_game()