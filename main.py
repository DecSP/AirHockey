import random
import sys
import pygame
from constants import *  
from AirHockey import Stick, Puck, AirHockey, Score, Timer
from load_image import load_image
from load_sound import load_sound
# from spell import *

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
game = AH

spell1 = 0
spell2 = 0
cooldown_spell1 = 0
cooldown_spell2 = 0
duration_spell1 = 0
duration_spell2 = 0

is_pause = False
is_gameover = False

def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (WIDTH, HEIGHT))
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
    global is_gameover, duration_spell1, duration_spell2, cooldown_spell1, cooldown_spell2

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
                game.reset()
                duration_spell1 = 0
                duration_spell2 = 0
                cooldown_spell1 = 0
                cooldown_spell2 = 0
                shuffle_spell(1)
                shuffle_spell(2)
        clock.tick(FPS)
        pygame.display.update()

def draw_process_bar():
    if spell1 > 0:
        pygame.draw.line(screen, "RED", (15, HEIGHT-20),
                         (15 + (WIDTH/2-3-15)*duration_spell1/SPELL_DURATION, HEIGHT-20), 10)
    elif spell1 == 0:
        pygame.draw.line(screen, "RED", (15, HEIGHT-20),
                         (15 + (WIDTH/2-3-15)*cooldown_spell1/SPELL_COOLDOWN, HEIGHT-20), 10)
    else:
        pygame.draw.line(screen, "RED", (15, HEIGHT-20),
                         (WIDTH/2-3, HEIGHT-20), 10)
    
    if spell2 > 0:
        pygame.draw.line(screen, "BLUE", (WIDTH-15, HEIGHT-20),
                         (WIDTH-15 - (WIDTH-15 - WIDTH/2-3)*duration_spell2/SPELL_DURATION, HEIGHT-20), 10)
    elif spell2 == 0:
        pygame.draw.line(screen, "BLUE", (WIDTH-15, HEIGHT-20),
                         (WIDTH-15 - (WIDTH-15 - WIDTH/2-3)*cooldown_spell2/SPELL_COOLDOWN, HEIGHT-20), 10)
    else:
        pygame.draw.line(screen, "BLUE", (WIDTH-15, HEIGHT-20),
                         (WIDTH/2+3, HEIGHT-20), 10)
    

def draw_spell():
    spellFont = pygame.font.SysFont("CopperPlate Gothic", 40, bold=True)
    next_spell1 = spellFont.render(SPELL_LIST[abs(spell1)-1].upper(), True, "RED")
    next_spell2 = spellFont.render(SPELL_LIST[abs(spell2)-1].upper(), True, "BLUE")
    cooldown_spell1 = spellFont.render("--COOLDOWN--", True, "RED")
    cooldown_spell2 = spellFont.render("--COOLDOWN--", True, "BLUE")
    active_spell1 = spellFont.render("--ACTIVE--", True, "RED")
    active_spell2 = spellFont.render("--ACTIVE--", True, "BLUE")
    
    if spell1 > 0:
        screen.blit(active_spell1, (20, HEIGHT-60))
    elif spell1 == 0:
        screen.blit(cooldown_spell1, (20, HEIGHT-60))
    else:
        screen.blit(next_spell1, (20, HEIGHT-60))
    
    if spell2 > 0:
        screen.blit(active_spell2, (WIDTH-active_spell2.get_width()-20, HEIGHT-60))
    elif spell2 == 0:
        screen.blit(cooldown_spell2, (WIDTH-cooldown_spell2.get_width()-20, HEIGHT-60))
    else:
        screen.blit(next_spell2, (WIDTH-next_spell2.get_width()-20, HEIGHT-60))

    draw_process_bar()

    

## Spell
def call_fire_ball():
    global game
    game.puck.speed = game.puck.speed * 1.85

def call_freeze_ball(player=1): #
    global game, duration_spell1, duration_spell2
    game.puck.speed = 0
    if player == 1:
        duration_spell1 = 0
    elif player == 2:
        duration_spell2 = 0


def call_small_goal(player=1):
    global game
    x = 120
    if player == 1: # opponen: Right
        game.ah_goal_y1_left = HEIGHT // 2 - x // 2
        game.ah_goal_y2_left = HEIGHT // 2 + x // 2
        game.ah_goal_width_left = x
    elif player == 2:
        game.ah_goal_y1_right = HEIGHT // 2 - x // 2
        game.ah_goal_y2_right = HEIGHT // 2 + x // 2
        game.ah_goal_width_right = x

def call_big_goal(player=1):
    global game
    x = 500
    if player == 1: # opponen: Right
        game.ah_goal_y1_right = HEIGHT // 2 - x // 2
        game.ah_goal_y2_right = HEIGHT // 2 + x // 2
        game.ah_goal_width_right = x
    elif player == 2:
        game.ah_goal_y1_left = HEIGHT // 2 - x // 2
        game.ah_goal_y2_left = HEIGHT // 2 + x // 2
        game.ah_goal_width_left = x

def call_small_char(player=1):
    global game
    if player == 1:
        game.s1.radius = game.s1.radius /2
        game.s1.mass = game.s1.mass /2
    elif player == 2:
        game.s2.radius = game.s1.radius /2
        game.s2.mass = game.s1.mass /2
    

def call_big_char(player=1):
    global game
    if player==1:
        game.s1.radius = game.s1.radius * 2
        game.s1.mass = game.s1.mass * 2
    elif player == 2:
        game.s2.radius = game.s2.radius * 2
        game.s2.mass = game.s2.mass * 2

def call_big_ball():
    global game
    game.puck.radius = game.puck.radius * 2

def call_small_ball():
    global game
    game.puck.radius = game.puck.radius / 2

def call_add_time(player=1): #
    global game, duration_spell1, duration_spell2
    game.timer.time = game.timer.time + 4
    if player == 1:
        duration_spell1 = 0
    elif player == 2:
        duration_spell2 = 0

def call_fast_char():
    global game
    game.s1.speed = game.s1.speed * 1.8

def call_slow_char():
    global game
    game.s2.speed = game.s2.speed * 1.8

# def disorient(): pass
# def no_spell(): pass

def shuffle_spell(player = 1):
    global spell1, spell2
    if player == 1:
        spell1 = -random.randint(1, SPELL_NUMS)
        print("[Spell 1] Next spell is", SPELL_LIST[abs(spell1)-1])
    else:
        spell2 = -random.randint(1, SPELL_NUMS)
        print("[Spell 2] Next spell is", SPELL_LIST[abs(spell2)-1])

SPELL_LIST = ["Fire Ball", "Freeze Ball", "Small Goal", "Big Goal", "Small Character", "Big Character", "Big Ball", "Small Ball", "Add time", "Fast Character", "Slow Character", "Cool down"]

# 1 - N (Using | Duration countdown)
# 0 (CoolDown for next spell)
# -1 -> -N (Pending | Next use)
def call_spell(player=1):
    global game, spell1, spell2, cooldown_spell1, cooldown_spell2, duration_spell1, duration_spell2
    if player == 1:
        spell1 = -spell1
        spell_idx = spell1
        cooldown_spell1 = SPELL_COOLDOWN
        duration_spell1 = SPELL_DURATION
    elif player == 2:
        spell2 = -spell2
        spell_idx = spell2
        cooldown_spell2 = SPELL_COOLDOWN
        duration_spell2 = SPELL_DURATION

    if spell_idx == 1:
        call_fire_ball()
    elif spell_idx == 2:
        call_freeze_ball(player)
    elif spell_idx == 3:
        call_small_goal()
    elif spell_idx == 4:
        call_big_goal()
    elif spell_idx == 5:
        call_small_char(3-player)
    elif spell_idx == 6:
        call_big_char(player)
    elif spell_idx == 7:
        call_big_ball()
    elif spell_idx == 8:
        call_small_ball()
    elif spell_idx == 9:
        call_add_time(player)
    elif spell_idx == 10:
        call_fast_char()
    elif spell_idx == 11:
        call_slow_char()

def delete_spell(player = 1):
    global game, spell1, spell2
    if player == 1:
       spell_idx = spell1
       spell1 = 0 
    elif player == 2:
        spell_idx = spell2
        spell2 = 0

    if spell_idx == 1:
        delete_fire_ball()
    elif spell_idx == 2:
        delete_freeze_ball()
    elif spell_idx == 3:
        delete_small_goal()
    elif spell_idx == 4:
        delete_big_goal()
    elif spell_idx == 5:
        delete_small_char(3-player)
    elif spell_idx == 6:
        delete_big_char(player)
    elif spell_idx == 7:
        delete_big_ball()
    elif spell_idx == 8:
        delete_small_ball()
    elif spell_idx == 9:
        delete_add_time()
    elif spell_idx == 10:
        delete_fast_char()
    elif spell_idx == 11:
        delete_slow_char()


def delete_fire_ball():
    global game
    game.puck.speed = game.puck.speed // 1.85

def delete_freeze_ball(): pass

def delete_small_goal():
    global game
    game.ah_goal_y1_left = AH_GOAL_Y1
    game.ah_goal_y2_left = AH_GOAL_Y2
    game.ah_goal_y1_right = AH_GOAL_Y1
    game.ah_goal_y2_right = AH_GOAL_Y2
    game.ah_goal_width_left = AH_GOAL_WIDTH
    game.ah_goal_width_right = AH_GOAL_WIDTH

def delete_big_goal():
    global game
    game.ah_goal_y1_left = AH_GOAL_Y1
    game.ah_goal_y2_left = AH_GOAL_Y2
    game.ah_goal_y1_right = AH_GOAL_Y1
    game.ah_goal_y2_right = AH_GOAL_Y2
    game.ah_goal_width_left = AH_GOAL_WIDTH
    game.ah_goal_width_right = AH_GOAL_WIDTH

def delete_small_char(player=1):
    global game
    if player == 1:
        game.s1.radius = AH_STICK_RADIUS
        game.s1.mass = AH_STICK_MASS
    elif player == 2:
        game.s2.radius = AH_STICK_RADIUS
        game.s2.mass = AH_STICK_MASS
    

def delete_big_char(player=1):
    global game
    if player==1:
        game.s1.radius = AH_STICK_RADIUS
        game.s1.mass = AH_STICK_MASS
    elif player == 2:
        game.s2.radius = AH_STICK_RADIUS
        game.s2.mass = AH_STICK_MASS

def delete_big_ball():
    global game
    game.puck.radius = game.puck.radius / 2

def delete_small_ball():
    global game
    game.puck.radius = game.puck.radius * 2

def delete_add_time(): pass

def delete_fast_char():
    game.s1.speed = AH_STICK_SPEED

def delete_slow_char(): 
    game.s2.speed = AH_STICK_SPEED


def start_game():
    global is_pause, is_gameover, game, cooldown_spell1, cooldown_spell2, spell1, spell2, duration_spell1, duration_spell2
    game = AH
    shuffle_spell(1)
    shuffle_spell(2)
    while True:
        time_delta = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # [Spell 1]
                    if duration_spell1 <= 0 and cooldown_spell1 <= 0:
                        print("[Spell 1]", SPELL_LIST[abs(spell1)-1])
                        call_spell(1)
                    elif duration_spell1 > 0:
                        print("[Spell 1] Active")
                    elif cooldown_spell1 > 0:
                        print("[Spell 1] Cooldown")
                if event.key == pygame.K_l:
                    # [Spell 2]
                    if duration_spell2 <= 0 and cooldown_spell2 <= 0:
                        print("[Spell 2]", SPELL_LIST[abs(spell2)-1])
                        call_spell(2)
                    elif duration_spell2 > 0:
                        print("[Spell 2] Active")
                    elif cooldown_spell2 > 0:
                        print("[Spell 2] Cooldown")
                if event.key == pygame.K_ESCAPE:
                    is_pause = not is_pause
        
        # print(spell1)

        if game == AH:
            if is_pause:
                paused()
            
            if AH_timer.ping():
                is_gameover = True
            if is_gameover:
                game_over(game)

            if spell1 == 0:
                cooldown_spell1 -= time_delta
                if cooldown_spell1 <= 0:
                    print("[Spell 1] Ready")
                    shuffle_spell(1)

            if spell2 == 0:
                cooldown_spell2 -= time_delta
                if cooldown_spell2 <= 0:
                    print("[Spell 2] Ready")
                    shuffle_spell(2)

            if spell1 > 0: # Cooldown
                duration_spell1 -= time_delta
                if duration_spell1 <= 0:
                    print("[Spell 1] Ended")
                    delete_spell(1)
                    spell1 = 0

            if spell2 > 0: # Cooldown
                duration_spell2 -= time_delta
                if duration_spell2 <= 0:
                    print("[Spell 2] Ended")
                    delete_spell(2)
                    spell2 = 0

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

            goal_result = game.goal()
            if goal_result > 0:  # if the boal hit goal => restart game
                if goal_result == 1:
                    AH_score.add(1,2) # Player 2 scores
                elif goal_result == 2:
                    AH_score.add(1,1) # Player 1 scores
                pygame.mixer.Sound.play(AirHockey.goal_sound)
                game.restart()
                # duration_spell1 = 0
                # duration_spell2 = 0
                # cooldown_spell1 = 0
                # cooldown_spell2 = 0
                # shuffle_spell(1)
                # shuffle_spell(2)
            AH_puck.check()
            if AH_puck.check_collision(AH_stick1):  
                pygame.mixer.Sound.play(AirHockey.hit_sound)
            if AH_puck.check_collision(AH_stick2):  
                pygame.mixer.Sound.play(AirHockey.hit_sound)
        
        
        

        pygame.display.set_caption(game.caption)
        screen.fill((0, 0, 0))
        game.render()
        draw_spell()
        clock.tick(FPS)
        AH_timer.count_down(time_delta)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    start_game()