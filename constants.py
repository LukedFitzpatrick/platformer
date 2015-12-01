
def constant(id):
   if id == "SCREEN_WIDTH":
      return 640
   elif id == "SCREEN_HEIGHT":
      return 480
   elif id == "MENU_BACKGROUND_COLOUR":
      return (100, 100, 100)
   elif id == "MENU_TITLE_COLOUR":
      return (200,200,200)
   elif id == "MENU_INACTIVE_COLOUR":
      return (150, 150, 150)
   elif id == "MENU_ACTIVE_COLOUR":
      return (255, 255, 255)
   elif id == "TILE_SIZE":
      return 16
   elif id == "PLAYER_ACCELERATION":
      return 0.5
   elif id == "PLAYER_MAX_SPEED":
      return 4
   elif id == "GRAVITY":
      return 0.5
   elif id == "FRICTION":
      return 0.3
   elif id == "JUMP_ACCELERATION":
      return 10
   elif id == "SPIKE_EPSILON":
      return 100
