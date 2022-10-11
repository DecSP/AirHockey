import os
import sys
import pygame
from constants import SOUND_DIR

pygame.init()


def load_sound(name):
    fullname = os.path.join(SOUND_DIR, name)
    if not os.path.isfile(fullname):
        print(f'File is not exist')
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound
