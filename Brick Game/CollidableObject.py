# Balls, walls, bricks, and paddles are all objects that can have collisions.

from Position import Position, AnimationFrames, RotatingCircle, FreeMovement
import pygame
from abc import ABC, abstractmethod
import math
import os
pygame.mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (255, 255, 0)
BALL_LOST = pygame.USEREVENT + 1
WALL_HIT_SOUND = pygame.mixer.Sound(os.path.join('Brick Game' , 'Assets', 'Wall.wav'))
BALL_LOSS_SOUND = pygame.mixer.Sound(os.path.join('Brick Game' , 'Assets', 'BallLoss.mp3'))
BRICK_HIT_SOUND = pygame.mixer.Sound(os.path.join('Brick Game' , 'Assets', 'Brick.wav'))
MOVING_BRICK_HIT_SOUND = pygame.mixer.Sound(os.path.join('Brick Game' , 'Assets', 'Brick2.mp3'))
PADDLE_HIT_SOUND = pygame.mixer.Sound(os.path.join('Brick Game' , 'Assets', 'Paddle.wav'))

class CollidableObject(ABC):
    @abstractmethod
    def __init__(self, _position):
        self.Position = _position

    @abstractmethod
    def display(self, _win, _microseconds):
        pass

    @abstractmethod
    def getRect(self, _microseconds):
        pass


class Brick(CollidableObject):

    def __init__(self, _position, _color, _width = 70, _height = 30, _borderColor = BLACK):
        super().__init__(_position)
        self.color = _color
        self.width = _width
        self.height = _height
        self.borderColor = _borderColor
    
    def getRect(self, _microseconds):
        return pygame.Rect(self.Position.getXPos(_microseconds), self.Position.getYPos(_microseconds), self.width, self.height)
    
    def display(self, _win, _microseconds):        
        pygame.draw.rect(_win, self.color, self.getRect(_microseconds), 0, 3)        
        pygame.draw.rect(_win, self.borderColor, self.getRect(_microseconds), 3, 3)
        #Todo:  Figure out how to draw a rotated brick.  Would this need to be a polygon?
        

    def checkCollision(self,  _ball, _microseconds):
        if self.getRect(_microseconds).colliderect(_ball.getRect(_microseconds)):
            #Get the point where the ball crossed the bottom or top of the brick.            
            if _ball.Position.yVelocity > 0:
                # Moving down, so find where it would have crossed the top of the brick.
                timeback = (_ball.Position.getYPos(_microseconds) - self.Position.getYPos(_microseconds)) / _ball.Position.yVelocity
                xPosition = _ball.Position.getXPos(_microseconds) - (_ball.Position.xVelocity * timeback)
                if (xPosition < self.Position.getXPos(_microseconds)):
                    _ball.Position.xVelocity = abs(_ball.Position.xVelocity) * -1
                else :
                    if (xPosition > self.Position.getXPos(_microseconds) + self.width):
                        _ball.Position.xVelocity = abs(_ball.Position.xVelocity)
                    else:
                        _ball.Position.yVelocity = abs(_ball.Position.yVelocity) * -1
            else:
                # Moving up, so find where it would have crossed the bottom of the brick.
                if (_ball.Position.yVelocity != 0):
                    timeback = (self.Position.getYPos(_microseconds) + self.height - _ball.Position.getYPos(_microseconds)) / _ball.Position.yVelocity
                    xPosition = _ball.Position.getXPos(_microseconds) - (_ball.Position.xVelocity * timeback)
                    if (xPosition < self.Position.getXPos(_microseconds)):
                        _ball.Position.xVelocity = abs(_ball.Position.xVelocity) * -1
                    else :
                        if (xPosition > self.Position.getXPos(_microseconds) + self.width):
                            _ball.Position.xVelocity = abs(_ball.Position.xVelocity)
                        else:
                            _ball.Position.yVelocity = abs(_ball.Position.yVelocity)
            if self.Position is AnimationFrames or self.Position is FreeMovement:
                MOVING_BRICK_HIT_SOUND.play()  #not working.  Figure out how to do class check in python
            else:
                BRICK_HIT_SOUND.play()
            return True
        return False



class Ball(CollidableObject):
    def __init__(self, _position, _color = WHITE, _radius = 8):
        super().__init__(_position)
        self.color = _color
        self.radius = _radius

    # todo representing the ball as a rectangle behind the scenes instead of as a circle makes it simpler to write collision logic, but 
    # might affect the accuracy of our collision detection.
    def getRect(self, _microseconds):
        return pygame.Rect(self.Position.getXPos(_microseconds), self.Position.getYPos(_microseconds), self.radius * 2, self.radius * 2)

    def display(self, _win, _microseconds):
        pygame.draw.circle(_win, self.color, (self.Position.getXPos(_microseconds), self.Position.getYPos(_microseconds)), self.radius)
        # Todo:  replace with an image when we get to the point that we need to be able to show ball spin.

class Paddle(CollidableObject):
    def __init__(self, _position, _color = BLUE, _width = 160, _height = 10):
        self.Position = _position
        self.color = _color
        self.width = _width
        self.height = _height

    def getRect(self, _microseconds):
        return pygame.Rect(self.Position.getXPos(_microseconds), self.Position.getYPos(_microseconds), self.width, self.height)

    def display(self, _win, _microseconds):        
        pygame.draw.rect(_win, self.color, self.getRect(_microseconds), 0, 5)

    def sign(self, x): 
        return 1-(x<=0) 

    def checkCollision(self,  _ball, _microseconds):
        if self.getRect(_microseconds).colliderect(_ball.getRect(_microseconds)):
            #_ball.Position.yVelocity = abs(_ball.Position.yVelocity) * -1
            #Want to be able to handle other angles.  X should not remain constant.  
            # a^2 + b^2 = c^2
            speed = math.sqrt(_ball.Position.xVelocity * _ball.Position.xVelocity + _ball.Position.yVelocity * _ball.Position.yVelocity)
            offset = _ball.Position.getXPos(_microseconds) - self.Position.getXPos(_microseconds) - self.width / 2
            horizontalVelocityComponent = offset / self.width * 2 * speed
            _ball.Position.xVelocity = (_ball.Position.xVelocity + horizontalVelocityComponent) / 1.75
            if speed * .98 < abs(_ball.Position.xVelocity):  #Ensure no imaginary numbers when we take the square root.
                _ball.Position.xVelocity = abs(speed) * .98 * self.sign(_ball.Position.xVelocity)
            _ball.Position.yVelocity = math.sqrt(speed * speed - _ball.Position.xVelocity * _ball.Position.xVelocity) * -1
            PADDLE_HIT_SOUND.play()
            return True
        return False

# We could have created four instances of wall class each with a different edge of the board, but I prefer this approach.
class Walls(CollidableObject):
    def __init__(self, _screenHeight, _screenWidth):
        #each border is a rectangle just off the screen edge.
        self.leftRect = pygame.Rect(-100, -100, 100, _screenHeight + 200)
        self.rightRect = pygame.Rect(_screenWidth, -100, 100, _screenHeight + 200)
        self.topRect = pygame.Rect(-100, -100, _screenWidth + 200, 100)
        self.bottomRect = pygame.Rect(-100, _screenHeight, _screenWidth + 200, 100)

    # This method was useful for testing, but is not otherwise used.
    def display(self, _win, _microseconds):        
        pygame.draw.rect(_win, YELLOW, self.leftRect, 0, 5)
        pygame.draw.rect(_win, YELLOW, self.rightRect, 0, 5)
        pygame.draw.rect(_win, YELLOW, self.topRect, 0, 5)
        pygame.draw.rect(_win, YELLOW, self.bottomRect, 0, 5)
    
    # Well, this is a bit awkward.  We don't use this method, but are forced to have it
    # because our parent class has declared it as abstract.
    def getRect(self, _microseconds):
        return self.leftRect

    def checkCollision(self, _ball, _microseconds):
        ballRect = _ball.getRect(_microseconds)
        if ballRect.colliderect(self.leftRect):
            _ball.Position.xVelocity = abs(_ball.Position.xVelocity)
            WALL_HIT_SOUND.play()
        if ballRect.colliderect(self.rightRect):
            _ball.Position.xVelocity = abs(_ball.Position.xVelocity) * -1
            WALL_HIT_SOUND.play()
        if ballRect.colliderect(self.topRect):
            _ball.Position.yVelocity = abs(_ball.Position.yVelocity)
            WALL_HIT_SOUND.play()
        if ballRect.colliderect(self.bottomRect):
            BALL_LOSS_SOUND.play()
            pygame.event.post(pygame.event.Event(BALL_LOST))