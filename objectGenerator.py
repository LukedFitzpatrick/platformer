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
      playerStand = loadFrameset("graphics/catwalk", 1, 1, 1)
      playerWalk = loadFrameset("graphics/catwalk", 1, 4, 5)
      playerJump = loadFrameset("graphics/catwalk", 1, 1, 1)
      playerFall = loadFrameset("graphics/catwalk", 1, 1, 1)
      playerGraphic = Graphic([playerStand,playerWalk, playerJump,
                               playerFall], 10, animating=True)
      playerPlayer = Player()
      
      playerObject = GameObject("Player", -1, -1, graphic=playerGraphic, 
                                player=playerPlayer)
      self.objects["Player"] = playerObject


      # Floor
      floorFrames = loadFrameset("graphics/floor", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 10, animating=False)
      floorObject = GameObject("Floor", -1, -1,solid=True,
                               graphic=floorGraphic)
      self.objects["Floor"] = floorObject


      # castle stuff
      floorFrames = loadFrameset("graphics/level1floortop", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 10, animating=False)
      floorObject = GameObject("Level1FloorTop", -1, -1,solid=True,
                               graphic=floorGraphic)
      self.objects["Level1FloorTop"] = floorObject

      floorFrames = loadFrameset("graphics/level1floorbottom", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 10, animating=False)
      floorObject = GameObject("Level1FloorBottom", -1, -1,solid=True,
                               graphic=floorGraphic)
      self.objects["Level1FloorBottom"] = floorObject

      floorFrames = loadFrameset("graphics/level1floordecoration", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 11, animating=False)
      floorObject = GameObject("Level1FloorDecoration", -1, -1,solid=False,
                               graphic=floorGraphic)
      self.objects["Level1FloorDecoration"] = floorObject
      
      floorFrames = loadFrameset("graphics/level1wall", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 2, animating=False)
      floorObject = GameObject("Level1Wall", -1, -1,solid=False,
                               graphic=floorGraphic)
      self.objects["Level1Wall"] = floorObject

      floorFrames = loadFrameset("graphics/level1window", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 2, animating=False)
      floorObject = GameObject("Level1Window", -1, -1,solid=False,
                               graphic=floorGraphic)
      self.objects["Level1Window"] = floorObject
      
      floorFrames = loadFrameset("graphics/level1bigwindow", 1, 1, 1)
      floorGraphic = Graphic([floorFrames], 2, animating=False)
      floorObject = GameObject("Level1BigWindow", -1, -1,solid=False,
                               graphic=floorGraphic)
      self.objects["Level1BigWindow"] = floorObject




      # Falling spike
      fSpikeImage = loadFrameset("graphics/fallingspike", 1, 1, 1)
      fSpikeGraphic = Graphic([fSpikeImage], 9, animating=False)
      fSpikeHazard = Hazard("FallingSpike")
      fSpikeObject = GameObject("FallingSpike", -1, -1,
                     graphic=fSpikeGraphic, hazard=fSpikeHazard)
      self.objects["FallingSpike"] = fSpikeObject
      
      
      # Rising spike
      rSpikeImage = loadFrameset("graphics/risingspike", 1, 1, 1)
      rSpikeGraphic = Graphic([rSpikeImage], 0, animating=False)
      rSpikeHazard = Hazard("RisingSpike")
      rSpikeObject = GameObject("RisingSpike", -1, -1,
                     graphic=rSpikeGraphic, hazard=rSpikeHazard)
      self.objects["RisingSpike"] = rSpikeObject

      # left and right shooting spikes
      lSpikeImage = loadFrameset("graphics/leftspike", 1, 1, 1)
      lSpikeGraphic = Graphic([lSpikeImage], 9, animating=False)
      lSpikeHazard = Hazard("LeftSpike")
      lSpikeObject = GameObject("LeftSpike", -1, -1,
                     graphic=lSpikeGraphic, hazard=lSpikeHazard)
      self.objects["LeftSpike"] = lSpikeObject

      rSpikeImage = loadFrameset("graphics/rightspike", 1, 1, 1)
      rSpikeGraphic = Graphic([rSpikeImage], 9, animating=False)
      rSpikeHazard = Hazard("RightSpike")
      rSpikeObject = GameObject("RightSpike", -1, -1,
                     graphic=rSpikeGraphic, hazard=rSpikeHazard)
      self.objects["RightSpike"] = rSpikeObject

      
      # Platform type 1
      platformImage = loadFrameset("graphics/platform", 1, 1, 1)
      platformGraphic = Graphic([platformImage], 10, animating=False)
      platformObject=GameObject("Platform",-1,-1,solid=True,graphic=platformGraphic)
      self.objects["Platform"] = platformObject


      # Platform type 2
      platformImage = loadFrameset("graphics/platformb", 1, 1, 1)
      platformGraphic = Graphic([platformImage], 10, animating=False)
      platformObject=GameObject("Platformb",-1,-1,solid=True,graphic=platformGraphic)
      self.objects["Platformb"] = platformObject

      


   def get(self, name, x, y):
      # bug with deepcopying surfaces means I have to do it manually
      o = self.objects[name]
      target = GameObject(name, x, y, o.solid, 
                          graphic=copy.copy(o.graphic),
                          text=copy.copy(o.text), 
                          player=copy.copy(o.player),
                          hazard=copy.copy(o.hazard))
      
      return target
