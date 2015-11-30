import pygame
from graphicsHandler import *
from menu import *
from game import *
from constants import *
from levels import *

pygame.init()



def playGame(screen):
   level = 1
   while(level<2):
      level += playLevel(generateLevel(level), screen)
      

screen = pygame.display.set_mode((constant("SCREEN_WIDTH"), 
                                  constant("SCREEN_HEIGHT")))


while True:
   result = mainMenu(screen)
   if result == 0: playGame(screen)
   elif result == 1: settingsMenu(screen)
   elif result == 2: sys.exit(1)

