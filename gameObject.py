from graphicsHandler import *
from keybindings import *
from constants import *
import random
import math

class GameObject:
   def __init__(self, debugName, x, y,solid=False, graphic=None, text=None, 
                player=None, hazard=None):     
      self.solid = solid
      self.debugName = debugName
      self.x = x
      self.y = y
      self.levelLineIndex = -1

      # make sure if you add anything here to fix the buggy
      # copier in objectGenerator.py

      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self
      else:
         self.graphic = None
      if(player):
         self.player = player
         self.player.parent = self
      else:
         self.player = None
      if(text):
         self.text = text
         self.text.parent = self
      else:
         self.text = None
      if(hazard):
         self.hazard = hazard
         self.hazard.parent = self
      else:
         self.hazard = None
         

   def isSolid(self):
      return self.solid

   def update(self, level, keys, gH):

      if(self.graphic):
         self.graphic.update(gH)
      if(self.player):
         self.player.update(keys, level)
      if(self.text):
         self.text.update()
      if(self.hazard):
         self.hazard.update(level)
      
      return (level, keys)


   def setLevelLineIndex(self, index):
      self.levelLineIndex = index

   def getLevelLineIndex(self):
      return self.levelLineIndex

   def setCoordinates(self, x, y):
      self.x = x
      self.y = y

   def getCoordinates(self):
      return (self.x, self.y)

   def getRect(self, cameraX=0, cameraY=0):
      r = pygame.Rect(self.x-cameraX, self.y-cameraY, 
                      self.graphic.width, self.graphic.height)
      return r

      
class Graphic:
   def __init__(self, frameSets, priority, animating=False, parent=None, immovable=False):
      
      self.frameSets = frameSets
      self.parent = parent
      self.priority = priority
      self.frameSetIndex = 0
      self.frameIndex = 0
      self.animating = animating
      self.playCount = -1
      self.stillPlaying = True
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()
      self.immovable = immovable
      self.flip = False
      self.rotateAngle = 0

   def update(self, gH):
      # possibly update the animation state here etc
      if self.animating and self.stillPlaying:
         self.frameIndex += 1
         self.frameIndex = self.frameIndex % len(self.frameSets[self.frameSetIndex])
         if self.frameIndex == 0 and self.playCount > 0:
            self.playCount -= 1
            if self.playCount == 0:
               self.stillPlaying = False
               self.playCount = -1
               # when we stop playing it, we probably want to finish on the
               # last frame in the set
               self.frameIndex = len(self.frameSets[self.frameSetIndex])-1
      
      if self.flip:
         i = pygame.transform.flip(self.frameSets[self.frameSetIndex][self.frameIndex], True, False)
      else:
         i = self.frameSets[self.frameSetIndex][self.frameIndex]
      


      i = pygame.transform.rotate(i, self.rotateAngle)
      gH.registerImage(i, self.parent.x, self.parent.y, 
                    self.priority, self.parent.debugName, self.immovable)
      
      #self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      #self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()


   # jump to a certain frame within a frame set
   def jumpToFrame(self, frame):
      self.frameIndex = frame

   def changeFrameSet(self, frameSet):
      self.frameSetIndex = frameSet
      self.frameIndex = 0

   def continueOrStartFrameSet(self, frameSet, playCount=-1):
      if self.frameSetIndex != frameSet:
         self.frameSetIndex = frameSet
         self.frameIndex = 0
         
         if playCount != -1:
            self.playCount = playCount
            self.stillPlaying = True
         else:
            self.stillPlaying = True
            self.playCount = -1

   def setFlip(self, flip):
      if flip == "LEFT":
         self.flip = True
      else:
         self.flip = False


   def setRotate(self, angle):
      self.rotateAngle = angle

   def changeRotate(self, deltaangle):
      self.rotateAngle += deltaangle

   def getRotate(self):
      return self.rotateAngle

class Text:
   def __init__(self, text, font, colour, priority, xoffset=0, yoffset=0, immovable=False):
      self.text = text
      self.font = font
      self.colour = colour
      self.priority = priority
      self.xoffset = xoffset
      self.yoffset = yoffset
      self.immovable = immovable
   
   def update(self):
      registerText(self.text, self.font, self.colour,
                   self.parent.x+self.xoffset, self.parent.y+self.yoffset, 
                   1, self.priority, self.parent.debugName, self.immovable)



class Player:
   def __init__(self):
      # for now just use the dimensions of the image as collision BBs
      # later could pass in the dimensions of the BB per frame
      self.collider = Collider()
      self.mover = Mover()
      self.alive = True
   
   def update(self, keys, level):
      self.mover.gravity()
      self.mover.friction()

      if keyBinding("LEFT") in keys:
         self.mover.left(constant("PLAYER_ACCELERATION"))
      if keyBinding("RIGHT") in keys:
         self.mover.right(constant("PLAYER_ACCELERATION"))
      if keyBinding("JUMP") in keys:
         self.mover.jump()
         keys.remove(keyBinding("JUMP"))
      
      self.collider.setDimensions(self.parent.x, self.parent.y,
            self.parent.graphic.width, self.parent.graphic.height)

      (collidedy, deltay) = level.calculateYCollision(self.collider, 
                                         self.mover.getDelta("y"))

      if collidedy:
         self.mover.yCollision()



      (collidedx, deltax) = level.calculateXCollision(self.collider, 
                                         self.mover.getDelta("x"))

    
      if collidedx:
         self.mover.xCollision()


      # flipping the graphic
      if deltax > 0:
         self.parent.graphic.setFlip("RIGHT")
      elif deltax < 0:
         self.parent.graphic.setFlip("LEFT")

      # choosing animations
      # moving in x
      if math.fabs(deltax) > 0:
         self.parent.graphic.continueOrStartFrameSet(1)

      # still in x
      else:
         self.parent.graphic.continueOrStartFrameSet(0)


      # falling (takes precedence over walk animation
      if deltay > 0:
         self.parent.graphic.continueOrStartFrameSet(3)
         if self.parent.graphic.getRotate() > 0:
            self.parent.graphic.changeRotate(-1)
         elif self.parent.graphic.getRotate() < 0:
            self.parent.graphic.changeRotate(1)
      #rising:
      elif deltay < 0 or not self.mover.onGround:
         self.parent.graphic.continueOrStartFrameSet(2)
         if deltax > 0:
            self.parent.graphic.setRotate(deltax*constant("JUMP_ROTATION_MODIFIER"))
         elif deltax < 0:
            self.parent.graphic.setRotate(deltax*constant("JUMP_ROTATION_MODIFIER"))

         deltax = deltax * constant("JUMP_SPEEDUP_MODIFIER")
      else:
         self.parent.graphic.setRotate(0)

      self.parent.x += deltax
      self.parent.y += deltay


   def kill(self):
      self.alive = False

   def isDead(self):
      return not self.alive

class Hazard:
   def __init__(self, name):
      self.name = name
      self.mover = None


   def update(self, level):
      # later can do different things for different hazards

      # if we touch the player, kill it
      player = level.findObjectByName("Player")
      if player.getRect().colliderect(self.parent.getRect()):
         player.player.kill()
      
      elif self.name == "FallingSpike" or self.name == "RisingSpike":
         (px, py) = player.getCoordinates()
         if math.fabs(int(px)-self.parent.x) <= constant("SPIKE_EPSILON"):
            #if not self.mover:
            if True:
               self.mover = Mover()
               self.collider = Collider()
               if self.name == "RisingSpike":
                  self.mover.up(constant("SPIKE_SPEED"))
               if self.name == "FallingSpike":
                  self.mover.down(constant("SPIKE_SPEED"))

      elif self.name == "LeftSpike" or self.name == "RightSpike":
         (px, py) = player.getCoordinates()
         if math.fabs(int(py)-self.parent.y) <= constant("SPIKE_EPSILON"):
            #if not self.mover:
            if True:
               self.mover = Mover()
               self.collider = Collider()
               if self.name == "LeftSpike":
                  self.mover.right(constant("SPIKE_SPEED"))
               elif self.name == "RightSpike":
                  self.mover.left(constant("SPIKE_SPEED"))
               


      # apply physics and collisions if we're doing that
      if self.mover and self.collider:
         self.mover.gravity()
         self.collider.setDimensions(self.parent.x, self.parent.y,
            self.parent.graphic.width, self.parent.graphic.height)
      
         (collidedx, deltax) = level.calculateXCollision(self.collider, 
                                         self.mover.getDelta("x"))
         (collidedy, deltay) = level.calculateYCollision(self.collider, 
                                         self.mover.getDelta("y"))
      
         if collidedx:
            self.mover.xCollision()
         if collidedy:
            self.mover.yCollision()
         
         self.parent.x += deltax
         self.parent.y += deltay





class Mover:
   def __init__(self, xv=0, yv=0, onGround=False,
                maxSpeed=constant("PLAYER_MAX_SPEED")):
      self.xv = xv
      self.yv = yv
      self.onGround = onGround
      self.maxSpeed = maxSpeed
      
   

   def xCollision(self):
      self.xv = 0

   def yCollision(self):
      if self.yv > 0:
         # falling down
         self.onGround = True
      self.yv = 0
      

   def jump(self):
      if self.onGround:
         self.yv -= constant("JUMP_ACCELERATION")
         self.onGround = False

   def right(self, v):
      # watch out for this, in here so live tweaking works
      self.maxSpeed = constant("PLAYER_MAX_SPEED")

      if self.xv < 0:
         self.xv = 0

      else:
         self.xv += v
         if self.xv > self.maxSpeed:
            self.xv = self.maxSpeed
   
   def left(self, v):
      # watch out for this, in here so live tweaking works
      self.maxSpeed = constant("PLAYER_MAX_SPEED")
      if self.xv > 0:
         self.xv = 0
         
      else:
         self.xv -= v
         if self.xv < -self.maxSpeed:
            self.xv = -self.maxSpeed

   def up(self, v):
      self.yv -= v
   
   def down(self, v):
      self.yv += v
   
   def gravity(self):
      self.yv += constant("GRAVITY")

   def friction(self):
      if self.xv > 0:
         self.xv -= constant("FRICTION")
         self.xv = max(self.xv, 0)
      
      elif self.xv < 0:
         self.xv += constant("FRICTION")
         self.xv = min(self.xv, 0)
      

   def stop(self):
      self.xv = 0

   def getDelta(self ,axis):
      if axis == "x":
         return self.xv
      if axis == "y":
         return self.yv
   




class Collider:
   def __init__(self):
      self.x = -1
      self.y = -1
      self.width = -1
      self.height = -1
   
   def setDimensions(self, x, y, width, height):
      self.x = x
      self.y = y
      self.width = width
      self.height = height

   def get(self, what):
      if what == "x":
         return int(self.x)
      if what == "y":
         return int(self.y)
      if what == "width":
         return self.width
      if what == "height":
         return self.height
      if what == "right":
         return int(self.x)+(self.width) - 1
      if what == "bottom":
         return int(self.y)+self.height

   

   def leadingEdge(self, direction):
      if direction == "LEFT":
         return int(self.x)
      elif direction == "RIGHT":
         return int(self.x) + self.width
      elif direction == "UP":
         return int(self.y)
      elif direction == "DOWN":
         return int(self.y)+self.height
