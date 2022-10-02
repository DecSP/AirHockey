import sys
import pygame
from constants import *  
from AirHockey import Stick, Puck, AirHockey
from load_image import load_image
from load_sound import load_sound

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_icon(load_image(ICON_IMAGE))
clock = pygame.time.Clock()

AH_stick1 = Stick(AH_STICK1_COLOR, AH_STICK1X, AH_STICK1Y)
AH_stick2 = Stick(AH_STICK2_COLOR, AH_STICK2X, AH_STICK2Y)
AH_puck = Puck(AH_PUCK_COLOR, WIDTH // 2, HEIGHT // 2)
AH = AirHockey(screen, AH_FIELD_COLOR, AH_stick1, AH_stick2, AH_puck)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.png'), (WIDTH, HEIGHT))
    pygame.display.set_caption('Pygame Mini Games')
    screen.blit(fon, (0, 0))
    if START_MUSIC:
        pygame.mixer.Sound.play(load_sound('start.mp3'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.stop()
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    game = AH
    while True:
        time_delta = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
        if game == AH:
            keys = pygame.key.get_pressed()
            # Player 1 input
            w = keys[pygame.K_w]
            s = keys[pygame.K_s]
            d = keys[pygame.K_d]
            a = keys[pygame.K_a]
            # Player 2 input
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            right = keys[pygame.K_RIGHT]
            left = keys[pygame.K_LEFT]
            # update player move 1
            AH_stick1.move(w, s, a, d, time_delta)
            AH_stick1.check_vertical()
            AH_stick1.check_left()
            # update player move 2
            AH_stick2.move(up, down, left, right, time_delta)
            AH_stick2.check_vertical()
            AH_stick2.check_right()
            # move puck
            AH_puck.move(time_delta)
            if game.goal():  # if the boal hit goal => restart game
                pygame.mixer.Sound.play(AirHockey.goal_sound)
                game.restart()
            AH_puck.check()
            if AH_puck.check_collision(AH_stick1):  
                pygame.mixer.Sound.play(AirHockey.hit_sound)
            if AH_puck.check_collision(AH_stick2):  
                pygame.mixer.Sound.play(AirHockey.hit_sound)
        pygame.display.set_caption(game.caption)
        screen.fill((0, 0, 0))
        game.render()
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    start_game()
