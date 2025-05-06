import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Spielvariablen
directions = ['up', 'down', 'left', 'right']
current_direction = random.choice(directions)
arrow_shown_time = 0
reaction_time = 0
waiting_for_input = False
score = 0

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

running = True
while running:
    screen.fill(WHITE)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and waiting_for_input:
            # Reaktion registrieren
            key_pressed = event.key
            correct = (
                (current_direction == 'up' and key_pressed == pygame.K_UP) or
                (current_direction == 'down' and key_pressed == pygame.K_DOWN) or
                (current_direction == 'left' and key_pressed == pygame.K_LEFT) or
                (current_direction == 'right' and key_pressed == pygame.K_RIGHT)
            )
            if correct:
                reaction_time = now - arrow_shown_time  # in Millisekunden
                # Beispiel: Score = 1000 - Reaktionszeit (min 0)
                score = max(0, 1000 - reaction_time)
                waiting_for_input = False

    # Neues Zeichen anzeigen
    if not waiting_for_input:
        current_direction = random.choice(directions)
        arrow_shown_time = pygame.time.get_ticks()
        waiting_for_input = True

    # Pfeil anzeigen (nur textlich hier)
    text = font.render(current_direction.upper(), True, BLACK)
    screen.blit(text, (150, 180))

    # Score anzeigen
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
