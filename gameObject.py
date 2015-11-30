from graphicsHandler import *
from keybindings import *
from constants import *
import random
import math

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, text=None, player=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      
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
         
   def update(self, level, keys, gH):

      if(self.graphic):
         self.graphic.update(gH)
      if(self.player):
         self.player.update(keys, level)
      if(self.text):
         self.text.update()
      
      return (level, keys)


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
      
      gH.registerImage(i, self.parent.x, self.parent.y, 
                    self.priority, self.parent.debugName, self.immovable)
      
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()


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
   
   def update(self, keys, level):
      # temporary!
      if keyBinding("LEFT") in keys:
         self.parent.graphic.continueOrStartFrameSet(1)
         self.parent.graphic.setFlip("LEFT")
         deltax = -4

      elif keyBinding("RIGHT") in keys:
         self.parent.graphic.continueOrStartFrameSet(1)
         self.parent.graphic.setFlip("RIGHT")
         deltax = 4

      else:
         deltax = 0
         self.parent.graphic.continueOrStartFrameSet(0)
      

      self.collider.setDimensions(self.parent.x, self.parent.y,
            self.parent.graphic.width, self.parent.graphic.height)

      # may have to update the collider in between these two?
      deltax = level.calculateXCollision(self.collider, deltax)
      


      # cheesy gravity
      deltay = 1
      deltay = level.calculateYCollision(self.collider, deltay)

      
      self.parent.x += deltax
      self.parent.y += deltay


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
         return self.x
      if what == "y":
         return self.y
      if what == "width":
         return self.width
      if what == "height":
         return self.height
      if what == "right":
         return self.x+self.width
      if what == "bottom":
         return self.y+self.height

   

   def leadingEdge(self, direction):
      if direction == "LEFT":
         return self.x
      elif direction == "RIGHT":
         return self.x + self.width
      elif direction == "UP":
         return self.y
      elif direction == "DOWN":
         return self.y+self.height
