import random
import sys
import pygame
from constants import *  
from AirHockey import Stick, Puck, AirHockey, Score, Timer
from load_image import load_image
from load_sound import load_sound

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_icon(load_image(ICON_IMAGE))
clock = pygame.time.Clock()

AH_stick1 = Stick(AH_STICK1_COLOR, AH_STICK1X, AH_STICK1Y)
AH_stick2 = Stick(AH_STICK2_COLOR, AH_STICK2X, AH_STICK2Y)
AH_puck = Puck(AH_PUCK_COLOR, WIDTH // 2, HEIGHT // 2)
AH_score = Score()
AH_timer = Timer()
AH = AirHockey(screen, AH_FIELD_COLOR, AH_stick1, AH_stick2, AH_puck, AH_score, AH_timer)



is_pause = False
is_gameover = False
game_mode = ""

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global game_mode
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (WIDTH, HEIGHT))
    pygame.display.set_caption('Air Hockey')
    
    
    def draw_button(text,button_y,mousepos):
        global game_mode
        button_width, button_height = 300,100
        button_x = (WIDTH-button_width)//2
        
        if 0<mousepos[0]-button_x<button_width and 0<mousepos[1]-button_y<button_height:
            game_mode=text[0]
            button_col,buttontext_col=COLORS['dark green'],COLORS['yellow']
        else:
            button_col,buttontext_col=COLORS['black'],COLORS['white']

        pygame.draw.rect(screen,button_col,pygame.Rect(button_x,button_y,button_width,button_height))
        buttonFont = pygame.font.SysFont("CopperPlate Gothic",50 , bold=True)
        buttonText = buttonFont.render(text, True,buttontext_col)
        buttonTextSize = buttonFont.size(text)
        buttontext_x = (WIDTH-buttonTextSize[0])//2
        screen.blit(
            buttonText,
            (
                buttontext_x,
                button_y+15
            ),
        )

    if START_MUSIC:
        pygame.mixer.Sound.play(load_sound('start.mp3'))
    screen.blit(fon, (0, 0))
    mousepos = pygame.mouse.get_pos()
    game_mode=""
    draw_button('1 Player',500,mousepos)
    draw_button('2 Player',650,mousepos)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode!="":
                    pygame.mixer.stop()
                    return
            elif event.type == pygame.MOUSEMOTION:
                screen.blit(fon, (0, 0))
                mousepos = event.pos
                game_mode=""
                draw_button('1 Player',500,mousepos)
                draw_button('2 Player',650,mousepos)
        pygame.display.flip()
        clock.tick(FPS)

def paused():
    global is_pause
    # sound.stop("music")
    pausedFont = pygame.font.SysFont("CopperPlate Gothic", 150, bold=True)
    pausedText = pausedFont.render("PAUSED", True, "PURPLE")
    pausedTextSize = pausedFont.size("PAUSED")
    screen.blit(
        pausedText,
        (
            int(WIDTH / 2 - pausedTextSize[0] / 2),
            int(HEIGHT / 2 - pausedTextSize[1] / 2),
        ),
    )

    while is_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_pause = False
                # sound.play("music")
        # gameDisplay.fill(white)
        clock.tick(FPS)
        pygame.display.update()

def game_over(game):
    global is_gameover

    winner = AH_score.get_result()
    player1Text = ""
    player2Text = ""
    if winner == 0:
        player1Text = "YOU DRAW!!!"
        player2Text = "YOU DRAW!!!"
    elif winner == 1:
        player1Text = "YOU WIN!!!"
        player2Text = "YOU LOSE!!!"
    elif winner == 2:
        player1Text = "YOU LOSE!!!"
        player2Text = "YOU WIN!!!"

    resultFont = pygame.font.SysFont("CopperPlate Gothic", 75, bold=True)
    
    player1Result = resultFont.render(player1Text, True, "RED")
    player2Result = resultFont.render(player2Text, True, "BLUE")
    
    player1Size = resultFont.size(player1Text)
    player2Size = resultFont.size(player2Text)

    player1ResultPos = (WIDTH//4-player1Size[0]//2, HEIGHT//2-player1Size[1]//2)
    player2ResultPos = (WIDTH*3//4-player2Size[0]//2, HEIGHT//2-player2Size[1]//2)

    
    screen.blit(player1Result, player1ResultPos)
    screen.blit(player2Result, player2ResultPos)
    
    while is_gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # reset game
                is_gameover = False
        clock.tick(FPS)
        pygame.display.update()



def start_game():
    global is_pause, is_gameover
    game = AH
    game.reset()
    while True:
        time_delta = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                #     game.restart()
                if event.key == pygame.K_ESCAPE:
                    #TODO
                    is_pause = not is_pause
        
        

        if game == AH:
            if is_pause:
                paused()
            
            if AH_timer.ping():
                is_gameover = True
            if is_gameover:
                game_over(game)
                return
            keys = pygame.key.get_pressed()
            # Player 1 input
            w = keys[pygame.K_w]
            s = keys[pygame.K_s]
            d = keys[pygame.K_d]
            a = keys[pygame.K_a]
            # Player 2 input
            if game_mode=='2':
                up = keys[pygame.K_UP]
                down = keys[pygame.K_DOWN]
                right = keys[pygame.K_RIGHT]
                left = keys[pygame.K_LEFT]
            else:
                right = AH_stick2.x < AH_puck.x+60
                left = not right
                down = AH_stick2.y < AH_puck.y
                up = not down
                if right or abs(AH_stick2.y-AH_puck.y)<30: down=up=False
                if  abs(AH_stick2.x-AH_puck.x)<10: right=left=False
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

            goal_result = game.goal()
            if goal_result > 0:  # if the boal hit goal => restart game
                if goal_result == 1:
                    AH_score.add(1,2) # Player 2 scores
                elif goal_result == 2:
                    AH_score.add(1,1) # Player 1 scores
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
        # clock.tick(FPS)
        deltaTime = clock.tick(FPS) / 1000.0
        AH_timer.count_down(deltaTime)
        pygame.display.flip()


if __name__ == '__main__':
    while True:
        start_screen()
        start_game()