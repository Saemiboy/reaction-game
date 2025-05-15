import pygame

# --- Farben ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

class Home:
    def __init__(self, width, height, font, highscorelist, username):
        self.width = width
        self.height = height
        self.font = font
        self.running = True
        self.username = username
        self.highscore = Tabelle(10, 150, highscorelist, self.font, ("Score", "Zeit", "Name", "Datum"))

    def show(self, surface):
        surface.fill(WHITE)

        willkommen_text = self.font.render(f'Herzlich Willkommen! {self.username}', True, BLACK)
        optionen_text = self.font.render('Drücken sie Enter, um das Spiel zu starten.', True, BLACK)

        surface.blit(willkommen_text, (10, 50))
        surface.blit(optionen_text, (10, 50 + ((optionen_text.get_height() + 10)*1)))

        self.highscore.show(surface)

    def input_handler(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.running = False



class Tabelle:
    """
    Folgende Veranschaulichung von einer Tabelle in pygame ist KI-generiert. Es wurde von ChatGPT gemacht.
    Prompt: "Ich möchte eine Highscoretabelle in pygame darstellen und habe folgende Daten zur verfügung:"
    """
    def __init__(self, x, y, highscorelist, font, header):
        self.x = x
        self.y = y
        self.scorelist = highscorelist
        self.font = font
        self.textlist = []
        self.header = header
        # Spaltenbreiten berechnen
        spalten = list(zip(*([self.header] + self.scorelist)))
        self.breiten = [max(self.font.size(str(e))[0] for e in spalte) + 20 for spalte in spalten]

    def zeichne_zeile(self, zeile, start_y, screen, farbe=BLACK):
        start_x = self.x
        for i, eintrag in enumerate(zeile):
            text = self.font.render(str(eintrag), True, farbe)
            screen.blit(text, (start_x, start_y))
            start_x += self.breiten[i]

    def show(self, surface):
        self.zeichne_zeile(self.header, self.y, surface, farbe=RED)
        for i, zeile in enumerate(self.scorelist):
            self.zeichne_zeile(zeile, (self.y + 40) + i * 30, surface)
