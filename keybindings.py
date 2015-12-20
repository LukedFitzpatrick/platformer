import pygame

def keyBinding(keyid):
   if keyid == "MENU_DOWN":
      return pygame.K_s
   elif keyid == "MENU_UP":
      return pygame.K_w
   elif keyid == "MENU_ACCEPT":
      return pygame.K_RETURN
   elif keyid == "PAUSE":
      return pygame.K_p
   elif keyid == "NEXT_LEVEL":
      return pygame.K_n
   elif keyid == "PREVIOUS_LEVEL":
      return pygame.K_b
   elif keyid == "RELOAD_LEVEL":
      return pygame.K_r
   elif keyid == "WRITE_LEVEL":
      return pygame.K_f
   elif keyid == "EDIT_DELETE":
      return pygame.K_q
   elif keyid == "EDIT_CANCEL":
      return pygame.K_ESCAPE
   elif keyid == "EDIT_ADD":
      return pygame.K_e
   elif keyid == "EDIT_UNDO":
      return pygame.K_z
   elif keyid == "CHANGE_ADD_TILE":
      return pygame.K_c
   elif keyid == "RIGHT":
      return pygame.K_d
   elif keyid == "LEFT":
      return pygame.K_a
   elif keyid == "JUMP":
      return pygame.K_w
   elif keyid == "NEXT_TWEAK":
      return pygame.K_RIGHT
   elif keyid == "PREV_TWEAK":
      return pygame.K_LEFT
   elif keyid == "TWEAK_UP":
      return pygame.K_UP
   elif keyid == "TWEAK_DOWN":
      return pygame.K_DOWN
   
