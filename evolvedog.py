#!/usr/bin/env python3

import random
import time
import sys
import numpy

#---- global variables ----
# mutation variables
sigmaA = 1 # (example) mutation sigma for mutate A
sigmaB = 1 # (example) mutation sigma for mutate B

#stop types
MAX_GEN = 1 #for setting the maximum generations
MIN_CONF = 2 #for setting the minimum dog confidence
MAX_TIME = 3 #for setting max amount of time

#---- end of global variables ----

# class for storing the image to evolve
class dogImage(object):

    # image data needed on initialisation
    def __init__(self, image_data):
        self.image_data = image_data
        # objective calculated later, False when not yet calculated
        self.obj = False

    # calculates objective value and stores it under self.obj
    def calcObj(self):
        self.obj = True


    # mutates the image
    def mutate(self):

        # does different mutations based on randomly generated number p
        p = random.random()
        if p<0.5:
            self.mutateA()
        else:
            self.mutateB()

    # one type of mutation
    def mutateA(self):
        pass

    # another type of mutation
    def mutateB(self):
        pass

    # this function returns a new dogImage object
    # new dogImage must have a /copy/ of the image_data
    def makeCopy(self):
        return self


def endCondition(stopType, stopValue, gen, bestConf, currentTime):
    if stopType==MAX_GEN:
        return gen>stopValue
    elif stopType==MIN_CONF:
        return bestConf>=stopValue
    elif stopType==MAX_TIME:
        return currentTime>=stopValue
    else:
        #pretend it is max time of 10 seconds
        return currentTime>=10


# ---- evolves startImage to be more dog ----
#
# Inputs:
# startImage = image to be turned into dog
# numChildren = number of children generated per generation
# stopType = type of stop condition. MAX_GEN, MIN_CONF, or MAX_TIME
#            if not properly specified, defaults to MAX_TIME
# stopValue = the value (of stopType) to stop evolving at
#            if stopType not properly specified, defaults to 10 seconds
#
# Output:
# parentHistory = list of parents for each generation
#                 parentHistory[-1] is the final image
# totalGen = total number of generations
# runTime = total run time


def Evolve(startImage, numChildren, stopType, stopValue):
    # initialise parent
    parent = startImage
    parent.calcObj()

    # initialise tracker variables
    bestConf = parent.obj
    gen = 1
    startTime = time.time()
    currentTime = time.time() - startTime

    # initialise parent history
    parentHistory = [parent]

    # runs until endCondition(...) is True
    while not endCondition(stopType, stopValue, gen, bestConf, currentTime):

        # make, mutate, and evaluate children      
        children = [parent.makeCopy() for i in range(numChildren)]
        [child.mutate() for child in children]
        [child.calcObj() for child in children]

        # find the best child, if better than parent
        best = parent
        for child in children:
            if child.obj>bestConf:
                best = child
                bestConf = child.obj

        # best is now the parent, add it to history
        parent = best
        parentHistory += [parent]

        # update stats
        currentTime = time.time() - startTime
        gen += 1

        # some stats for nerds
        print("Generation:",gen,"\tBest conf:", bestConf, "\tRun time (s):",\
              round(currentTime,1))

    # get final times
    totalGen = gen - 1
    runTime = startTime - time.time()
    return(parentHistory, totalGen, runTime)


# function that returns the position of a random rectangle in an image,
# optionally taking the size of the rectangle as an argument
# returns two arrays of two, in the form [row, column],[row,column]
# for the top left and bottom right corners of the rectangle
def getRandomRect(image, height=False, width=False):
    # TODO: percentage pixels
    if height==False:
        height=random.randrange(20,100)
    if width==False:
        width=random.randrange(20,100)
    maxHeight = len(origarray)
    maxWidth = len(origarray[0])
    topx = random.randrange(0,maxWidth-width)
    topy = random.randrange(0,maxHeight-height)
    bottomx = topx+width
    bottomy = topy+height
    return([[topx, topy],[bottomx, bottomy]])

# Function that moves the contents of one rectangle into another rectangle of the same size
# Takes arguments for starting Rect and ending Rect, with rectangles defined as they are
# in the comments for getRandomRect
def moveRect(imgarray, startRect, endRect):
    #TODO: validate input by e.g. verifying size of rects is identical
    for i in range(startRect[0][0], startRect[0][1]):
        for j in range(startRect[1][0], startRect[1][1]):
            #print("blah" + str(i) + ' ' + str(j))
            #TODO: finish writing function


print("Hello dog")
if len(sys.argv) != 2:
    #origfile = "f.png" 
    sys.exit("Usage: %s imagefile" % sys.argv[0])

import keras

origfile = sys.argv[1]
orig = keras.preprocessing.image.load_img(origfile)
# Some debug crap
print(type(orig))
print(orig.format)
print(orig.mode)
print(orig.size)
orig.show()
origarray = keras.preprocessing.image.img_to_array(orig)

# for i, row in enumerate(origarray):
#     for j, column in enumerate(origarray):
#         if 50<=i<=100 and 100<=j<=150:
#             origarray[i][j] = [0,0,0]
# newimage = keras.preprocessing.image.array_to_img(origarray)
# newimage.show()

startRect=getRandomRect(origarray)
print(startRect)
endRect=startRect
print(endRect)
moveRect(origarray, startRect, endRect)


#fliparray = numpy.flip(origarray, [0])
#flipimage = keras.preprocessing.image.array_to_img(fliparray)
#flipimage.show()




