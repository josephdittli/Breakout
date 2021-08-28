# These classes handles location, velocity and rotation.


from array import *
import math
from math import cos, sin


def rotate_origin_only(radians, xy):
    """Only rotate a point around the origin (0, 0)."""
    x, y = xy
    xx = x * math.cos(radians) + y * math.sin(radians)
    yy = -x * math.sin(radians) + y * math.cos(radians)

    return xx, yy


# Can be used for an item that doesn't move, a stationary brick.
class Position:
    def __init__(self, _xPos, _yPos):
        self.xPoint = _xPos
        self.yPoint = _yPos

    def getXPos(self, _microseconds):
        return self.xPoint

    def getYPos(self, _microseconds):
        return self.yPoint

# Set movement defined by an array of positions that repeats.  ie, eight bricks spin around to make a tire.
class AnimationFrames(Position):

    def __init__(self, _xPos=0, _yPos=0, _xVelocity=0, _yVelocity=0, _rad=0, _radVelocity=0, _microseconds = 0):
        self.xPoint = array('f')
        self.yPoint = array('f')
        self.rotation = array('f')
        if _microseconds != 0:
            self.xVelocity = _xVelocity
            self.yVelocity = _yVelocity
            self.xPoint.insert(0, _xPos)
            self.yPoint.insert(0, _yPos)
            self.rotation.insert(0, _rad)
            self.spin = _radVelocity
            self.ms = _microseconds
        
    # This can be useful to initialize the frames as offset from another animation.  
    # For instance, if we have eight bricks going around in a circle, then we can 
    # create the animation frames once and then give them to all eight bricks with eight different offsets.
    def CloneAnimationWithOffset(self, _offsetIn):
        _otherAnimation = AnimationFrames()
        index = 0
        while index < len(self.xPoint):
            offset = (index + _offsetIn) % (len(self.xPoint))
            _otherAnimation.xPoint.insert(index, self.xPoint[offset])
            _otherAnimation.yPoint.insert(index, self.yPoint[offset])
            _otherAnimation.rotation.insert(index, self.rotation[offset])
            _otherAnimation.ms = self.ms
            index += 1
        return _otherAnimation

    
    # change the velocity
    def setVelocity(self, _xVelocity, _yVelocity):
        self.xVelocity = _xVelocity
        self.yVelocity = _yVelocity

    # change the velocity
    def setSpin(self, _radVelociy):
        self.spin = _radVelociy   
        
    # compute new position without changing velocity
    def addFrame(self):
        newRadius = self.rotation[len(self.rotation)-1] + self.spin
        while newRadius < 0:
            newRadius += math.pi * 2
        while newRadius > math.pi * 2:
            newRadius -= math.pi * 2
        self.rotation.insert(len(self.rotation), newRadius)

        self.xPoint.insert(len(self.xPoint), self.xPoint[len(self.xPoint)-1] + self.xVelocity)
        self.yPoint.insert(len(self.yPoint), self.yPoint[len(self.yPoint)-1] + self.yVelocity)

    def getFrameAtTime(self, _microseconds):
        index = _microseconds % self.ms
        index = index / self.ms * len(self.xPoint)
        return index
    
    # determine location of object at given time.  Accepts non-integer input, which means it will need to 
    # compute the position somewhere between two frames
    def getXPos(self, _microseconds):
        frame = self.getFrameAtTime(_microseconds)
        nextframe = (int(frame) + 1) % len(self.xPoint)
        return self.xPoint[int(frame)] * (1 - (frame - int(frame))) + self.xPoint[nextframe] * (frame - int(frame))        
        
    def getYPos(self, _microseconds):
        frame = self.getFrameAtTime(_microseconds)
        nextframe = (int(frame) + 1) % len(self.yPoint)
        return self.yPoint[int(frame)] * (1 - (frame - int(frame))) + self.yPoint[nextframe] * (frame - int(frame))

    def getRotation(self, _microseconds):
        frame = self.getFrameAtTime(_microseconds)
        nextframe = (int(frame) + 1) % len(self.rotation)
        return self.rotation[int(frame)] * (1 - (frame - int(frame))) + self.rotation[nextframe] * (frame - int(frame))

class RotatingCircle(AnimationFrames):
    def __init__(self, _xPos, _yPos, _diameter, _frames, _microseconds):
        self.xPoint = array('f')
        self.yPoint = array('f')
        self.xVelocity = _diameter * math.pi / _frames
        self.yVelocity = 0
        self.xPoint.insert(0, int(_xPos + _diameter/4))
        self.yPoint.insert(0, _yPos)
        self.rotation = array('f')
        self.rotation.insert(0, 0)
        self.spin = - math.pi * 2 /_frames
        self.ms = _microseconds
        for i in range(0, _frames - 1):
            self.addFrame()

    def addFrame(self):
        xy = rotate_origin_only(self.spin, (self.xVelocity, self.yVelocity))
        x, y = xy
        self.xVelocity = x
        self.yVelocity = y
        super().addFrame()


# Free movement defined by current position and velocity.  Ie, the ball... but also the paddle
class FreeMovement(Position):
    def __init__(self, _xPos, _yPos, _xVelocity, _yVelocity, _rad, _radVelocity, _IntervalInMicroseconds):
        self.xPoint = _xPos
        self.yPoint = _yPos
        self.xVelocity = _xVelocity
        self.yVelocity = _yVelocity
        self.rotation = _rad
        self.spin = _radVelocity
        self.TimeInterval = _IntervalInMicroseconds
        self.ms = 0
    
    # change the velocity
    def setVelocity(self, _xVelocity, _yVelocity):
        self.xVelocity = _xVelocity
        self.yVelocity = _yVelocity

    # change the velocity
    def setSpin(self, _radVelociy):
        self.spin = _radVelociy

    def updatePosition(self, _microseconds):
        timeElapsed = _microseconds - self.ms
        if timeElapsed == 0:
            return
        self.ms = _microseconds
        Interval = timeElapsed / self.TimeInterval
        self.xPoint = self.xPoint + self.xVelocity * Interval
        self.yPoint = self.yPoint + self.yVelocity * Interval
        self.rotation = self.rotation + self.spin * Interval
        while (self.rotation < 0):
            self.rotation += math.pi * 2
        while (self.rotation > math.pi * 2):
            self.rotation -= math.pi * 2

    def getXPos(self, _microseconds):
        self.updatePosition(_microseconds)
        return int(self.xPoint)
        
    def getYPos(self, _microseconds):
        self.updatePosition(_microseconds)
        return int(self.yPoint)

    def getRotation(self, _microseconds):
        self.updatePosition(_microseconds)
        return self.rotation