import pygame

# --- Farben ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

testliste = [
    (2312, "asdfas", '24-01-01'),
    (2312, "sdff", '24-01-01'),
    (2312, "dd", '24-01-01'),
    (2312, "gadsghwwe", '24-01-01'),
    (2312, "asdcasdfghasd", '24-01-01'),
]

class Home:
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.running = True

    def show(self, surface):
        surface.fill(WHITE)

        willkommen_text = self.font.render('Herzlich Willkommen!', True, BLACK)
        optionen_text = self.font.render('Drücken sie Enter, um das Spiel zu starten.', True, BLACK)

        surface.blit(willkommen_text, (10, 50))
        surface.blit(optionen_text, (10, 50 + ((optionen_text.get_height() + 10)*1)))

    def input_handler(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.running = False


    def update(self):
        pass


class Highscore:
    def __init__(self, x, y, highscorelist, font):
        self.x = x
        self.y = y
        self.scorelist = highscorelist
        self.font = font
        self.textlist = []
    
    def show(self):
        for eintrag in self.scorelist:
            tablerow = self.font.render(f'')
    
