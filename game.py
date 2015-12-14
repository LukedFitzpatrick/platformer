from logging import *
from graphicsHandler import *
from keybindings import *
from menu import *
from gameObject import *
from levels import *
import sys


def updateCamera(tracking, level, cameraX, cameraY):
   
   newcameraX = tracking.x - int(constant("SCREEN_WIDTH")/2)
   newcameraY = tracking.y - int(constant("SCREEN_HEIGHT")/2)

   
   newcameraX = max(newcameraX, 0)
   newcameraX = min(newcameraX, level.width-constant("SCREEN_WIDTH"))

   newcameraY = max(newcameraY, 0)
   newcameraY = min(newcameraY, level.height-constant("SCREEN_HEIGHT"))     
   
   return (newcameraX, newcameraY)



def playLevel(level, screen, FPS=60):
   keysdown = []
   mainloop = True
   clock = pygame.time.Clock()
   
   cameraX = 0
   cameraY = 0
   
   gH = GraphicsHandler()

   controlsOn = True
   while mainloop:
      player = level.findObjectByName("Player")

      milliseconds = clock.tick(FPS)
      if clock.get_fps() < 20:
         print "FPS DROP: " + str(clock.get_fps())
         pass

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            mainloop = False
            sys.exit(1)
         elif event.type == pygame.KEYDOWN:
            if controlsOn:
               keysdown.append(event.key)
         elif event.type == pygame.KEYUP:
            if event.key in keysdown:
               keysdown.remove(event.key)
         elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            level.dealWithClick(pos, cameraX, cameraY)


      # do stuff with keysdown here
      if keyBinding("PAUSE") in keysdown:
         keysdown.remove(keyBinding("PAUSE"))
         pauseMenu(screen)
         keysdown = []
      if keyBinding("NEXT_LEVEL") in keysdown:
         keysdown.remove(keyBinding("NEXT_LEVEL"))
         dprint("Next level!")
         return 1

      if keyBinding("PREVIOUS_LEVEL") in keysdown:
         keysdown.remove(keyBinding("PREVIOUS_LEVEL"))
         dprint("Previous level!")
         return -1


      if keyBinding("RELOAD_LEVEL") in keysdown:
         keysdown.remove(keyBinding("RELOAD_LEVEL"))
         level.restartLevel()
         player = level.findObjectByName("Player")
         dprint("Restarted level!")

      if keyBinding("WRITE_LEVEL") in keysdown:
         keysdown.remove(keyBinding("WRITE_LEVEL"))
         level.writeLevelToFile()
         dprint("Wrote level!")
      
      if keyBinding("EDIT_DELETE") in keysdown:
         keysdown.remove(keyBinding("EDIT_DELETE"))
         level.setEditMode(constant("EDIT_DELETE"))
         dprint("Click to delete!")

      if keyBinding("EDIT_ADD") in keysdown:
         keysdown.remove(keyBinding("EDIT_ADD"))
         level.setEditMode(constant("EDIT_ADD"))
         dprint("Click to add!")
         
      if keyBinding("EDIT_CANCEL") in keysdown:
         keysdown.remove(keyBinding("EDIT_CANCEL"))
         level.setEditMode(constant("EDIT_NONE"))
         dprint("Edit cancelled!")

      if keyBinding("EDIT_UNDO") in keysdown:
         keysdown.remove(keyBinding("EDIT_UNDO"))
         level.undoDeleteLevelLine()
         dprint("Edit undone!")
     
     
      (cameraX, cameraY) = updateCamera(player, level, cameraX, cameraY)


      count = 0
      for o in level.gameObjects:
         (level, keysDown) = o.update(level, keysdown, gH)           
          

      if player.x >= level.width:
         return 1

      if player.player.isDead():
          level.restartLevel(keepPosition=False)

      level.displayCollisionMap(gH)
      
      gH.displayAll(screen, cameraX, cameraY)
