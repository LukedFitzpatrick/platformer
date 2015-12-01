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
      playerWalk = loadFrameset("graphics/roughwalk", 1, 6, 2)
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

      # Roof
      roofFrames = loadFrameset("graphics/roof", 1, 1, 1)
      roofGraphic = Graphic([roofFrames], 10, animating=False)
      roofObject = GameObject("Roof", -1, -1, graphic=roofGraphic)
      self.objects["Roof"] = roofObject


      # Exit Door
      doorImage = loadFrameset("graphics/door", 1, 1, 1)
      doorGraphic = Graphic([doorImage], 9, animating=False)
      doorObject = GameObject("Exit", -1, -1, graphic=doorGraphic)
      self.objects["Exit"] = doorObject

      # Spikes
      spikesImage = loadFrameset("graphics/spikes", 1, 1, 1)
      spikesGraphic = Graphic([spikesImage], 9, animating=False)
      spikesHazard = Hazard("Spike")
      spikesObject = GameObject("Spikes", -1, -1, graphic=spikesGraphic,
                                hazard=spikesHazard)
      self.objects["Spikes"] = spikesObject

      # Falling spike
      fSpikeImage = loadFrameset("graphics/fallingspike", 1, 1, 1)
      fSpikeGraphic = Graphic([fSpikeImage], 9, animating=False)
      fSpikeHazard = Hazard("FallingSpike")
      fSpikeObject = GameObject("FallingSpike", -1, -1,
                     graphic=fSpikeGraphic, hazard=fSpikeHazard)
      self.objects["FallingSpike"] = fSpikeObject
      
      
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




      # Platform
      platformImage = loadFrameset("graphics/platform", 1, 1, 1)
      platformGraphic = Graphic([platformImage], 10, animating=False)
      platformObject=GameObject("Platform",-1,-1,graphic=platformGraphic)
      self.objects["Platform"] = platformObject

   def get(self, name, x, y):
      # bug with deepcopying surfaces means I have to do it manually
      o = self.objects[name]
      target = GameObject(name, x, y, 
                          graphic=copy.copy(o.graphic),
                          text=copy.copy(o.text), 
                          player=copy.copy(o.player),
                          hazard=copy.copy(o.hazard))
      
      return target
