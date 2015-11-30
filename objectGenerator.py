import pygame
from gameObject import *
import copy

class ObjectGenerator:
   def __init__(self):
      pass


   def loadObjects(self):
      # later we could specify the level here so we don't
      # load absolutely everything at once
      self.objects = {}
      
      # Player
      playerStand = loadFrameset("graphics/stand", 1, 1, 1)
      playerWalk = loadFrameset("graphics/walk", 1, 3, 4)
      playerJump = loadFrameset("graphics/jump", 1, 1, 1)
      playerFall = loadFrameset("graphics/fall", 1, 1, 1)
      playerGraphic = Graphic([playerStand,playerWalk, playerJump,
                               playerFall], 10, animating=True)
      playerPlayer = Player()
      
      playerObject = GameObject("Player", -1, -1, graphic=playerGraphic, 
                                player=playerPlayer)
      self.objects["Player"] = playerObject


      # Floor
      floorFrames = loadFrameset("graphics/floor", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 10, animating=False)
      floorObject = GameObject("Floor", -1, -1, graphic=floorGraphic)
      self.objects["Floor"] = floorObject

      # Exit Door
      doorImage = loadFrameset("graphics/door", 1, 1, 1)
      doorGraphic = Graphic([doorImage], 9, animating=False)
      doorObject = GameObject("Exit", -1, -1, graphic=doorGraphic)
      self.objects["Exit"] = doorObject



   def get(self, name, x, y):
      # bug with deepcopying surfaces means I have to do it manually
      o = self.objects[name]
      target = GameObject(name, x, y, 
                          graphic=copy.copy(o.graphic),
                          text=copy.copy(o.text), 
                          player=copy.copy(o.player))
      
      return target
