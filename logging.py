# contains functions to print testing output, write game log files etc.
import os
import glob

LOGGING_ON = True
DEBUG_PRINTING_ON = True
HARD_ASSERTS_ON = True

# quick debug printing
def dprint(line):
   if(DEBUG_PRINTING_ON):
      print line

# writes line to stream.txt
def log(stream, line, newLine=True):
   if(LOGGING_ON):
      f = open(str(stream)+".txt", 'a')
      f.write(str(line))
      if(newLine):
         f.write("\n")
      f.close()

# empties the specified log file
def cleanLog(stream):
   if not ".txt" in stream:
      stream += ".txt"
        
   # just make this file blank
   f = open(str(stream), "w")
   f.write("")
   f.close()
   

# empties all txt files in /logs
# make sure you call this at the start not the end...
def cleanAllLogs():
   files=glob.glob("*.txt")
   for filename in files:
      cleanLog(filename)
  

# wrapper for assert that I can turn on and off
def wAssert(statement, identifier=""):
   if not statement:
      if HARD_ASSERTS_ON:
         assert statement, str(identifier)
      else:
         dPrint("Assertion Failed: " + str(identifier))
         log("failedAsserts", str(identifier))  
