from gameObject import *
import pygame
from graphicsHandler import *
from objectGenerator import *
import random
import math


class CollisionMarker:
   def __init__(self, solid):
      self.solid = solid
   

   def setSolid(self, solid):
      self.solid = solid

   def isSolid(self):
      return self.solid


class Level:
   def __init__(self):
      self.gameObjects = []
      self.width = 0
      self.height = 0
      self.collisionMap = []
      
   def setDimensions(self, width, height):
      self.width = width
      self.height = height
      self.collisionMap = []

      for x in range(0, self.width/constant("TILE_SIZE")):
         column = []
         for y in range(0, self.height/constant("TILE_SIZE")):
            c = CollisionMarker(False)
            column.append(c)

         self.collisionMap.append(column)
         
   def displayCollisionMap(self):
      for y in range(0, self.height/constant("TILE_SIZE")):
         for x in range(0, self.width/constant("TILE_SIZE")):
            if self.collisionMap[x][y].solid:
               print "#",
            else:
               print ".",
         
         print ""

   def setCollision(self, x, y, solid):
      self.collisionMap[x][y].setSolid(solid)

   def tileToCoord(self, tileNumber):
      return tileNumber*constant("TILE_SIZE")

   def coordToTile(self, coord):
      return int(coord/constant("TILE_SIZE"))

   # distance in pixels between two tile/coords
   def distance(self, a, atype, b, btype):
      
      if atype == "TILE" and btype == "TILE":
         if b > a: (a, b) = (b, a)
         return (self.tileToCoord(a)+constant("TILE_SIZE") - 
                   self.tileToCoord(b))
      elif atype == "COORD" and btype == "COORD":
         if b>a: (a, b) = (b, a)
         return a - b
      elif atype == "TILE" and btype == "COORD":
         acoord = self.tileToCoord(a)
         if b>acoord:           
            return acoord+constant("TILE_SIZE") - b
         else:
            return acoord - b

      elif atype == "COORD" and btype == "TILE":
         return distance(b, "TILE", a, "COORD")




   def findObjectByName(self, name):
      for o in self.gameObjects:
         if o.debugName == name:
            return o


   def calculateXCollision(self, collider, deltax):    
      # figure out which way we're going
      if deltax >= 0: xDir = "RIGHT"
      else: xDir = "LEFT"
      
      # find the horizontal lines we're intersecting
      topTile = self.coordToTile(collider.get("y"))
      bottomTile = self.coordToTile(collider.get("bottom"))-1
      linesToCheck = []
      for i in range(topTile, bottomTile+1): linesToCheck.append(i)

      # find the closest obstacle in the collision map
      if xDir == "LEFT": increment = -1
      if xDir == "RIGHT": increment = 1
      checkx = self.coordToTile(collider.leadingEdge(xDir))
      nearestColliderX = -1
      
      checked = 0
      # assume that we never move further than 4 tiles in one frame
      while (nearestColliderX==-1 and checked < 4 and  checkx >= 0
             and checkx < self.coordToTile(self.width)):
            
         for y in linesToCheck:
            if self.collisionMap[checkx][y].isSolid():
               nearestColliderX = checkx
              
         checkx += increment
         checked += 1
         
      # now in nearestColliderX is the nearest tile x which is an obstacle
      # we want to only move up to this tile if our distance to it is
      # less than delta x.
      colliderDistance = self.distance(nearestColliderX, "TILE", 
                                       collider.leadingEdge(xDir), "COORD")
      
      if math.fabs(colliderDistance) < math.fabs(deltax):
         xMove = colliderDistance     
         collided = True

      else: 
         xMove = deltax
         collided = False

      return (collided, xMove)


   def calculateYCollision(self, collider, deltay):    
      # figure out which way we're going
      if deltay >= 0: yDir = "DOWN"
      else: yDir = "UP"
      
      # find the horizontal lines we're intersecting
      leftTile = self.coordToTile(collider.get("x"))
      rightTile = self.coordToTile(collider.get("right"))-1
      linesToCheck = []
      for i in range(leftTile, rightTile+1): linesToCheck.append(i)

      # find the closest obstacle in the collision map
      if yDir == "UP": increment = -1
      if yDir == "DOWN": increment = 1
      
      checky = self.coordToTile(collider.leadingEdge(yDir))
      nearestColliderY = -1
      
      checked = 0
      # assume that we never move further than 4 tiles in one frame
      while (nearestColliderY==-1 and checked < 4 and  checky >= 0
             and checky < self.coordToTile(self.height)):
            
         for x in linesToCheck:
            if self.collisionMap[x][checky].isSolid():
               nearestColliderY = checky
              
         checky += increment
         checked += 1
         
      # now in nearestColliderY is the nearest tile y which is an obstacle
      # we want to only move up to this tile if our distance to it is
      # less than delta y.
      colliderDistance = self.distance(nearestColliderY, "TILE", 
                                       collider.leadingEdge(yDir), "COORD")
      
      if math.fabs(colliderDistance) < math.fabs(deltay):
         yMove = colliderDistance     
         collided = True

      else: 
         yMove = deltay
         collided = False

      return (collided, yMove)





def generateLevel(levelNumber):
   gameObjects = []
   level = Level()

   oG = ObjectGenerator()
   oG.loadObjects()
   # hopefully replace this with a level generator print out reader
   if levelNumber == 1:
      level.setDimensions(1024, 480)
      
      # make the player object
      gameObjects.append(oG.get("Player", 100, level.height-100))
      
      # boundary floors
      for x in range(0, level.width/16):
         gameObjects.append(oG.get("Floor",x*16,level.height-16))
         level.setCollision(x, level.coordToTile(level.height-16), True)
         
         gameObjects.append(oG.get("Floor",x*16,0))
         level.setCollision(x, 0, True)
      
      for y in range(0, level.height/16):
         gameObjects.append(oG.get("Floor", 0, y*16))
         level.setCollision(0, y, True)
         gameObjects.append(oG.get("Floor", level.width-16,y*16))
         level.setCollision(level.coordToTile(level.width-16), y, True)
      

      # level floors
      startx = 20
      for y in range(26, 19, -2): 
         for x in range(startx, startx+4):
            gameObjects.append(oG.get("Floor", x*16, level.tileToCoord(y)))
            level.setCollision(x, y, True)
         startx += 10

      # spikes
      for x in range(20, 60):
         gameObjects.append(oG.get("Spikes", x*16, 448))

      # make the exit door
      gameObjects.append(oG.get("Exit", level.width-48, level.height-48))


   level.gameObjects = gameObjects
   return level

   
