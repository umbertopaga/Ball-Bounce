import pygame
import sys
import math
import random
from pygame.locals import *

# Impostazioni iniziali
pygame.init()

# Definizione colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# Colori per le palle
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

# Dimensioni schermo e cerchio
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Palla nel Cerchio')
clock = pygame.time.Clock()

# Dimensioni cerchio e palla
CIRCLE_RADIUS = 200
BALL_RADIUS = 10

# Area del cerchio
circle_area = math.pi * (CIRCLE_RADIUS ** 2)

# Impostazioni cerchio e apertura
circle_center = (WIDTH // 2, HEIGHT // 2)
angle_opening = math.pi / 6  # Apertura di 30 gradi
opening_speed = 0.02  # Velocità di rotazione dell'apertura
current_angle = 0  # Angolo attuale dell'apertura

# Timer
start_time = pygame.time.get_ticks()

# Lista palle
balls = [{'pos': circle_center, 'vel': [random.uniform(-3, 3), random.uniform(-3, 3)], 'color': random.choice(COLORS)}]

def draw_circle_with_opening():
    global current_angle
    current_angle += opening_speed  # Ruota l'apertura
    start_angle = current_angle
    end_angle = current_angle + angle_opening

    # Disegna il cerchio e l'apertura
    pygame.draw.circle(screen, WHITE, circle_center, CIRCLE_RADIUS, 5)
    pygame.draw.arc(screen, BLACK, (circle_center[0] - CIRCLE_RADIUS, circle_center[1] - CIRCLE_RADIUS, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), start_angle, end_angle, CIRCLE_RADIUS)

def move_balls():
    global balls
    for ball in balls:
        ball['pos'] = (ball['pos'][0] + ball['vel'][0], ball['pos'][1] + ball['vel'][1])

        # Controllo rimbalzo contro i bordi del cerchio
        dx = ball['pos'][0] - circle_center[0]
        dy = ball['pos'][1] - circle_center[1]
        distance = math.hypot(dx, dy)

        if distance + BALL_RADIUS >= CIRCLE_RADIUS:
            normal = (dx / distance, dy / distance)
            vel_normal = ball['vel'][0] * normal[0] + ball['vel'][1] * normal[1]
            ball['vel'] = [
                ball['vel'][0] - 2 * vel_normal * normal[0],
                ball['vel'][1] - 2 * vel_normal * normal[1]
            ]

            # Aggiunta di caos: leggera variazione casuale alla velocità dopo il rimbalzo
            ball['vel'][0] += random.uniform(-0.5, 0.5)
            ball['vel'][1] += random.uniform(-0.5, 0.5)

            # Controllo se la palla è nell'apertura
            ball_angle = math.atan2(-dy, dx) % (2 * math.pi)
            start_angle = current_angle % (2 * math.pi)
            end_angle = (current_angle + angle_opening) % (2 * math.pi)

            if start_angle <= ball_angle <= end_angle or start_angle <= ball_angle + 2 * math.pi <= end_angle:
                ball['pos'] = circle_center
                ball['vel'] = [random.uniform(-3, 3), random.uniform(-3, 3)]
                balls.append({'pos': circle_center, 'vel': [random.uniform(-3, 3), random.uniform(-3, 3)], 'color': random.choice(COLORS)})

def check_game_over():
    total_balls_area = len(balls) * (math.pi * BALL_RADIUS ** 2)
    return total_balls_area >= circle_area

def show_game_over_screen(elapsed_time):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    font = pygame.font.SysFont(None, 48)
    time_text = font.render(f"Time: {elapsed_time:.2f} s", True, WHITE)
    screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

    pygame.display.flip()

    # Aspetta che l'utente chiuda il gioco
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

# Ciclo principale del gioco
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Disegna il cerchio con l'apertura
    draw_circle_with_opening()

    # Muovi e disegna le palle
    move_balls()
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['pos'][0]), int(ball['pos'][1])), BALL_RADIUS)

    # Calcola e mostra il tempo trascorso
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Controllo fine del gioco
    if check_game_over():
        show_game_over_screen(elapsed_time)
        break

    pygame.display.flip()
    clock.tick(60)
