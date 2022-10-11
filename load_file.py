import os
import sys
import pygame
from constants import LOAD_DIR, SOUND_DIR

pygame.init()

def filename(name):
    # Find out where we are, or in the case of an exe
    if hasattr(sys, "frozen"):
        basedir = sys.prefix
    else:
        basedir = sys.path[0]

    filename = os.path.join(basedir, name)

    if not os.access(filename, os.F_OK | os.R_OK):
        print("Could not find file '%s'." % filename)
        raise SystemExit

    return filename

def load_image(name, colorkey=None):
    fullname = os.path.join(filename(LOAD_DIR), name)
    if not os.path.isfile(fullname):
        print(f"Image is not exist")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_sound(name):
    fullname = os.path.join(filename(SOUND_DIR), name)
    if not os.path.isfile(fullname):
        print(f'File is not exist')
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound
