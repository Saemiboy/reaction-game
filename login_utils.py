import pygame

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Klicke in das Textfeld
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def update(self):
        # Dynamische Breite
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Login:
    def __init__(self, font):
        self.benutzername_input = InputBox(20, 20, 200, 30, font)
        self.passwort_input = InputBox(20, 60, 200, 30, font)
        self.isactive = True
        self.inputboxes = [self.benutzername_input, self.passwort_input]

    def draw(self, surface):
        surface.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.isactive = False
            for box in self.inputboxes:
                box.handle_event(event)

        for box in self.inputboxes:
            box.draw(surface)

    def update(self):
        for box in self.inputboxes:
            box.update()

        