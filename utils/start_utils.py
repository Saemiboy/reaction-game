import pygame

# --- Farben ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

class Home:
    def __init__(self, width, height, font, highscorelist, highscorelisttoday, username):
        self.width = width
        self.height = height
        self.font = font
        self.running = True
        self.username = username
        self.highscore = Tabelle(10, 180, highscorelist, self.font, ("Runden", "Zeit", "Benutzername", "Datum"), "Highscore")
        self.highscore_today = Tabelle(10, 180, highscorelisttoday, self.font, ("Runden", "Zeit", "Benutzername", "Datum"), "Todays Highscore")
        self.table_counter = 2

    def show(self, surface):
        surface.fill(WHITE)

        willkommen_text = self.font.render(f'Herzlich Willkommen {self.username}!', True, BLACK)
        optionen_text = self.font.render('Drücken sie Enter, um das Spiel zu starten.', True, BLACK)
        ziel_text = self.font.render('Die Spacebar drücken wenn rot innerhalb grün ist.', True, BLACK)
        pfeilbild = self.font.render('->', True, BLACK)

        surface.blit(willkommen_text, (10, 50))
        surface.blit(optionen_text, (10, 50 + ((optionen_text.get_height() + 10)*1)))
        surface.blit(ziel_text, (10, 50 + ((ziel_text.get_height() + 10)*2)))
        surface.blit(pfeilbild, (550, 550))

        if self.table_counter % 2 == 0:
            self.highscore.show(surface)
        else:
            self.highscore_today.show(surface)

    def input_handler(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.table_counter += 1



class Tabelle:
    """
    Folgende Veranschaulichung von einer Tabelle in pygame ist KI-generiert. Es wurde von ChatGPT gemacht.
    Prompt: "Ich möchte eine Highscoretabelle in pygame darstellen und habe folgende Daten zur verfügung:"
    """
    def __init__(self, x, y, highscorelist, font, header, titel):
        self.x = x
        self.y = y
        self.scorelist = highscorelist
        self.font = font
        self.textlist = []
        self.header = header
        self.titel = titel
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
        titeltext = self.font.render(self.titel, True, BLUE)
        surface.blit(titeltext, (self.x, self.y))
        self.zeichne_zeile(self.header, self.y+40, surface, farbe=RED)
        for i, zeile in enumerate(self.scorelist):
            self.zeichne_zeile(zeile, (self.y + 40) + (i+1) * 30, surface)
