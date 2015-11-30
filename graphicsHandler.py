# Abstract data object and type to handle what gets shown on the screen
from logging import *
from constants import *
import pygame


# a GraphicsObject is something that will shortly be displayed
# doesn't get updated other than a frame counter
# type = "image" "rect" "circle" etc.

class GraphicsObject:
   def __init__(self, type, representation, screenx, screeny, 
                priority, debugName, immovable=False):
      self.type = type
      self.rep = representation
      self.screenx = screenx
      self.screeny = screeny
      self.priority = priority
      self.debugName = debugName
      self.immovable = immovable

   def show(self, screen, camerax, cameray):   

      if self.type == "image":
         # in this case, rep is a straight image
         if self.immovable:
            screen.blit(self.rep, (self.screenx, self.screeny))
         
         else:
            screen.blit(self.rep, (self.screenx-camerax, self.screeny-cameray))
      
      # todo add camera to these types, for now assume they're immovable
      elif self.type == "rect":
         # in this case, rep is a RectangleWrapper
         pygame.draw.rect(screen, self.rep.colour, self.rep.rect, self.rep.thickness)
      elif self.type == "text":
         # the rep is a TextWrapper
         label = self.rep.thefont.render(self.rep.text, False, self.rep.colour)
         if not self.immovable:
            screen.blit(label, (self.rep.left-camerax, self.rep.top-cameray))
         else:
            screen.blit(label, (self.rep.left, self.rep.top))           
         

class TextWrapper:
   def __init__(self, text, thefont, colour, left, top):
      self.text = text
      self.thefont = thefont
      self.colour = colour
      self.left = left
      self.top = top

class RectangleWrapper:
   def __init__(self, colour, thickness, left, top, width, height):
      self.rect = pygame.Rect(left, top, width, height)
      self.colour = colour
      self.thickness = thickness
                         
class GraphicsHandler:
   def __init__(self):
      self.objects = [] 
      
   # put an image i.e. .png into the queue of things to be shown
   def registerImage(self, image, screenx, screeny, 
                     priority=1, debugName="", immovable=False):
      
      g = GraphicsObject("image", image, screenx, screeny,
                         priority, debugName, immovable)
      self.objects.append(g)
      

   def registerRect(self, colour,thickness, left, top, width, height, 
                 priority, debugName):
      r = RectangleWrapper(colour, thickness, left, top, width, height)
      g = GraphicsObject("rect", r, left, top, 
                      priority, debugName)
      self.objects.append(g)
   
   def registerText(self, text, thefont, colour, left, top,
                    priority, debugName, immovable=False):
      t = TextWrapper(text, thefont, colour, left, top)
      g = GraphicsObject("text", t, left, top,
                     priority, debugName, immovable)
   
      self.objects.append(g)



   def displayAll(self, screen, cameraX=0, cameraY=0):
        
      background = pygame.Surface(screen.get_size())
      background = background.convert()
      background.fill((0, 0, 0))
      screen.blit(background, (0, 0))

      # sort the graphics objects by priority: high priority -> drawn last
      self.objects.sort(key=lambda x: x.priority) 

      for o in self.objects:
         o.show(screen, cameraX, cameraY)     
   
      self.objects = []

      pygame.display.flip()


# little helper function to load a frameset
# e.g. loadFrameset("graphics/walk", 1, 3, 4)
# multiplicity is how many times each frame plays


def loadFrameset(baseFileName, smallIndex, bigIndex, multiplicity):
   frames = []
   for n in range(smallIndex, bigIndex+1):
      i = pygame.image.load(baseFileName + str(n) + ".png")
      for k in range(0, multiplicity):
         frames.append(i)

   return frames
