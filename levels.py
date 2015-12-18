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
      self.levelLines = []
      self.deletedLines = []
      self.levelLineIndex = 0
      self.levelNumber = -1
      self.editMode = constant("EDIT_NONE")
      self.currentAddingTile = 'Floor'

   def changeAddingTile(self):
      s = raw_input("Tile to add:")
      oG = ObjectGenerator()
      oG.loadObjects()
      try:
         o = oG.get(s, 0, 0)
      except:
         print "Failed to get " + str(s)
         return

      self.currentAddingTile = s


      self.currentAddingTile

   def setEditMode(self, editMode):
      self.editMode = editMode
            
   def getEditMode(self):
      return self.editMode

      
   def addLevelLine(self, line):
      self.levelLines.append(line)
      self.levelLineIndex += 1


   def clearLevelLines(self):
      self.levelLines = []
      self.levelLineIndex = 0


   def undoDeleteLevelLine(self):
      if len(self.deletedLines) > 0:
         self.addLevelLine(self.deletedLines.pop())
         self.restartLevel()
      
   def deleteLevelLine(self, lineIndex):
      self.deletedLines.append(self.levelLines[lineIndex])
      self.levelLines[lineIndex] = ""
      
      
   def getLevelLineIndex(self):
      return self.levelLineIndex

   def getAllLevelLines(self):
      return self.levelLines

   def getLevelLine(self, index):
      return self.levelLines[index]

   def resetCollisionMap(self):
      self.collisionMap = []
      for x in range(0, self.width/constant("TILE_SIZE") + 5):
         column = []
         for y in range(0, self.height/constant("TILE_SIZE") + 5):
            c = CollisionMarker(False)
            column.append(c)

         self.collisionMap.append(column)



   def setDimensions(self, width, height):
      self.width = width
      self.height = height
      self.collisionMap = []

      for x in range(0, self.width/constant("TILE_SIZE") + 5):
         column = []
         for y in range(0, self.height/constant("TILE_SIZE") + 5):
            c = CollisionMarker(False)
            column.append(c)

         self.collisionMap.append(column)
         
   def displayCollisionMap(self, gH):
      for y in range(0, self.height/constant("TILE_SIZE")):
         for x in range(0, self.width/constant("TILE_SIZE")):
            if self.collisionMap[x][y].solid:
               #print "#",
               s = constant("TILE_SIZE")
               gH.registerRect((255, 0, 0), 1, x*s,y*s,s,s,15,"collide")
            else:
               pass#print ".",
            

   def setCollision(self, x, y, solid=True):
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
      for i in range(topTile, bottomTile+1): 
         linesToCheck.append(i)

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


   def interpretLevelLine(self, c, oG):
      if len(c) > 0 and c[0] != "width" and c[0] != "height":
         if False:
            pass
         # making an object
         else:
            if "range" in c[1]:
               xrange = c[1].split(' ')
               startx = int(xrange[1])
               endx = int(xrange[2]) + 1
               jumpx = int(xrange[3])
            else:
               startx = int(c[1])
               # needs to be plus one because of Python's range strangeness
               endx = int(c[1]) + 1
               jumpx = 1

            if "range" in c[2]:
               yrange = c[2].split(' ')
               starty = int(yrange[1])
               endy = int(yrange[2]) + 1
               jumpy = int(yrange[3])
            else:
               starty = int(c[2])
               endy = int(c[2]) + 1
               jumpy = 1
            
            for x in range(startx, endx, jumpx):
               for y in range(starty, endy, jumpy):
                  o = oG.get(str(c[0]), x, y)
                  o.setLevelLineIndex(self.getLevelLineIndex())
                  self.gameObjects.append(o)
                  if o.isSolid():
                     s = constant("TILE_SIZE")
                     coly = y + (o.graphic.height - s)
                     for colx in range(x, x+(o.graphic.width), s):
                        self.setCollision(self.coordToTile(colx), 
                                          self.coordToTile(coly), True)

      
      self.addLevelLine(c)


   def readLevelFromFile(self, levelNumber, oG, 
                         reload=False, staticplayer=None):
      self.levelNumber = levelNumber
      
      
      if reload:
         commands = self.getAllLevelLines()
         self.clearLevelLines()
      else:
         with open("levels/level"  + str(levelNumber) +".txt") as f:
            lines = f.readlines()

         commands = []
         for l in lines:
            if l[0] != '#':
               l = l.split(',')
               c = []
               for x in l: 
                  x=x.rstrip()
                  c.append(x)
               if len(c) > 1:
                  commands.append(c)
      

         # the first and second line should be the width and height
         self.setDimensions(int(commands[0][1]), int(commands[1][1]))
   
      self.gameObjects = []
      for c in commands:
         self.interpretLevelLine(c, oG)
      

      if staticplayer:
         p = self.findObjectByName("Player") 
         p.x = staticplayer.x
         p.y = staticplayer.y

   def writeLevelToFile(self):
      with open("levels/level"  + str(self.levelNumber) +".txt", "w") as f:
         for l in self.getAllLevelLines():
            if len(l) > 1:
               for p in l:
                  f.write(p)
                  f.write(',')
               f.write('\n')


   def deleteInPlace(self, x, y):
      for o in self.gameObjects:
         if o.getRect().collidepoint(x, y):
            print "Deleted this:"
            print self.getLevelLine(o.getLevelLineIndex())
            self.deleteLevelLine(o.getLevelLineIndex())
            
            # now we also have to delete the collision
            
            self.restartLevel()

   def getTileToAdd(self):
      return self.currentAddingTile


   def addInPlace(self, normx, normy):
      
      line = [self.getTileToAdd(), str(normx), str(normy)]
      self.addLevelLine(line)
      self.restartLevel()


               
   def dealWithClick(self, pos, cameraX, cameraY):
      x=pos[0]+cameraX
      y=pos[1]+cameraY
      tilex = self.coordToTile(x)
      tiley = self.coordToTile(y)
      normx = self.tileToCoord(tilex)
      normy = self.tileToCoord(tiley)

      #print "Coords: x:"+str(x)+", y:"+str(y)          
      #print "Tile: x:"+str(tilex)+", y:"+ str(tiley)
      #print "Norm Coords: x:"+str(normx)+", y:"+str(normy) 
      #print ""

      mode = self.getEditMode()
      if constant("EDIT_ON"):
         if mode == constant("EDIT_DELETE"):
            self.deleteInPlace(x, y)
         
         elif mode == constant("EDIT_ADD"):
            self.addInPlace(normx, normy)


   def restartLevel(self, keepPosition=True):
      oG = ObjectGenerator()
      oG.loadObjects()
      if keepPosition:
         player = self.findObjectByName("Player")
      else:
         player = None
      self.resetCollisionMap()
      self.gameObjects = []
      self.readLevelFromFile(self.levelNumber, oG, 
                             reload=True, staticplayer=player)
      


def generateLevel(levelNumber):
   gameObjects = []
   level = Level()
   oG = ObjectGenerator()
   oG.loadObjects()

   level.readLevelFromFile(levelNumber, oG)
   
   return level

   
