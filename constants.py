constants = {"SCREEN_WIDTH": 640, 
             "SCREEN_HEIGHT": 480, 
             "MENU_BACKGROUND_COLOUR":(100, 100, 100),
             "MENU_TITLE_COLOUR":(200, 200, 200),
             "MENU_INACTIVE_COLOUR":(150, 150, 150),
             "MENU_ACTIVE_COLOUR":(200, 200, 200),
             "TILE_SIZE":16,
             "PLAYER_ACCELERATION": 0.4,
             "PLAYER_MAX_SPEED": 6,
             "GRAVITY": 1.14,
             "FRICTION": 0.2,
             "JUMP_ACCELERATION": 17,
             "SPIKE_EPSILON":  25,
             "SPIKE_SPEED": 20,
             "EDIT_DELETE": 0,
             "EDIT_ADD": 1,
             "EDIT_NONE": 2,
             "EDIT_ON": True,
             "BOUNDING_BOXES": False,
             "LEVEL_BACKGROUND_COLOUR": (25,71,157),
             "JUMP_ROTATION_MODIFIER": 3,
             "JUMP_SPEEDUP_MODIFIER": 1.6
             }

def updateConstant(id, newValue):
   global constants
   constants[id] = newValue

def constant(id):
   global constants
   return constants[id]
