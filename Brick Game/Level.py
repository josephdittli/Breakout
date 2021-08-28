# Each child class here represents a seperate level that the player can play through.

from CollidableObject import *
from Position import *
import array
from abc import ABC, abstractmethod

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKRED = (100, 0, 0)
LIGHTGREY = (200, 200, 200)
ORANGE = (226,127,0)  #e27f00
DARKGREY = (100,100,100)

class Level(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display(self, _win):
        pass

    @abstractmethod
    def checkCollisions(self, _ball, _time):
        pass

    @abstractmethod
    def checkLevelComplete(self):
        pass

    @abstractmethod
    def drawScreen(self, _win, _width, _height):
        pass

# a very basic level used to test the walls, paddle, and basic physics.
class TestLevel(Level):
    def __init__(self):
        self.topRowBricks = []
        self.secondRowBricks = []
        for i in range(0, 14):
            self.secondRowBricks.append(Brick(Position(20 + i * 70, 20), WHITE,70,30,LIGHTGREY))
            self.secondRowBricks.append(Brick(Position(20 + i * 70, 120), RED,70,30,DARKRED))

    def display(self, _win, _microseconds):
        for i in range(0, self.topRowBricks.__len__()):
            self.topRowBricks[i].display(_win, _microseconds)
        for i in range(0, self.secondRowBricks.__len__()):
            self.secondRowBricks[i].display(_win, _microseconds)

    def checkCollisions(self, _ball, _microseconds):
        for i in range(0, self.topRowBricks.__len__()):
            if self.topRowBricks[i].checkCollision(_ball, _microseconds):
                del self.topRowBricks[i]
                return
        for i in range(0, self.secondRowBricks.__len__()):
            if self.secondRowBricks[i].checkCollision(_ball, _microseconds):
                del self.secondRowBricks[i]
                return

    def checkLevelComplete(self):
        if self.topRowBricks.__len__() == 0 and self.secondRowBricks.__len__() == 0:
            return True
        return False

    def drawScreen(self, _win, _width, _height):
        pygame.draw.rect(_win, BLACK, pygame.Rect(0, 0, _width, _height), 0, 0)

# A hot orange racecar.  Moving bricks, background image.
class CarLevel(Level):
    def __init__(self):
        self.carBricks = []
        self.wheelBricks = []
        
        wheelMovement1 = RotatingCircle(170,210,112,32,10000000)  #(_xPos, _yPos, _diameter, _frames, _microseconds)
        for i in range(0, 8):
            self.wheelBricks.append(Brick(wheelMovement1.CloneAnimationWithOffset(i*4), BLACK,40,40,WHITE))
        
        wheelMovement2 = RotatingCircle(760,220,102,32,10000000)  #(_xPos, _yPos, _diameter, _frames, _microseconds)
        for i in range(0, 8):
            self.wheelBricks.append(Brick(wheelMovement2.CloneAnimationWithOffset(i*4), BLACK,40,40,WHITE))

        pavementMovement = AnimationFrames(1040, 360, -70, 0, 0, 0, 30000000)   #_xPos=0, _yPos=0, _xVelocity=0, _yVelocity=0, _rad=0, _radVelocity=0, _microseconds = 0):
        for i in range(0, 16):
            pavementMovement.addFrame()
        pavementMovement.setVelocity(0, -400)  #send them around the top of the screen, off the edges and out of sight.
        pavementMovement.addFrame()
        pavementMovement.setVelocity(1200, 0)
        pavementMovement.addFrame()
        pavementMovement.setVelocity(0, 400)
        pavementMovement.addFrame()

        for i in range(0, len(pavementMovement.xPoint)):
            self.carBricks.append(Brick(pavementMovement.CloneAnimationWithOffset(i), WHITE,70,30,LIGHTGREY))

        #Bottom of car
        for i in range(0, 3):
            self.carBricks.append(Brick(Position(70 + i * 70, 320), BLACK,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(3, 9):
            self.carBricks.append(Brick(Position(80 + i * 70, 320), ORANGE,70,30,LIGHTGREY)) #Center of car
        for i in range(9, 12):
            self.carBricks.append(Brick(Position(90 + i * 70, 320), BLACK,70,30,LIGHTGREY)) #Forward Tire
        for i in range(12, 13):
            self.carBricks.append(Brick(Position(90 + i * 70, 320), ORANGE,70,30,LIGHTGREY)) #front bumper

        #second row of car
        for i in range(0, 1):
            self.carBricks.append(Brick(Position(70 + i * 70, 290), ORANGE,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(1, 3):
            self.carBricks.append(Brick(Position(70 + i * 70, 290), BLACK,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(3, 9):
            self.carBricks.append(Brick(Position(80 + i * 70, 290), ORANGE,70,30,LIGHTGREY)) #Center of car
        for i in range(9, 12):
            self.carBricks.append(Brick(Position(90 + i * 70, 290), BLACK,70,30,LIGHTGREY)) #Forward Tire
        for i in range(12, 13):
            self.carBricks.append(Brick(Position(90 + i * 70, 290), ORANGE,70,30,LIGHTGREY)) #front bumper

            
        #third row of car
        for i in range(0, 1):
            self.carBricks.append(Brick(Position(70 + i * 70, 260), ORANGE,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(1, 3):
            self.carBricks.append(Brick(Position(70 + i * 70, 260), BLACK,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(3, 4):
            self.carBricks.append(Brick(Position(80 + i * 70, 260), ORANGE,70,30,LIGHTGREY)) #Center of car
        for i in range(4, 9):
            self.carBricks.append(Brick(Position(80 + i * 70, 260), BLACK,70,30,LIGHTGREY)) #Center of car
        for i in range(9, 12):
            self.carBricks.append(Brick(Position(90 + i * 70, 260), BLACK,70,30,LIGHTGREY)) #Forward Tire
        for i in range(12, 13):
            self.carBricks.append(Brick(Position(90 + i * 70, 260), ORANGE,70,30,LIGHTGREY)) #front bumper
            
        #fourth row of car
        for i in range(0, 1):
            self.carBricks.append(Brick(Position(70 + i * 70, 230), ORANGE,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(1, 3):
            self.carBricks.append(Brick(Position(70 + i * 70, 230), BLACK,70,30,LIGHTGREY))  #tail exhaust pipe, rear tire
        for i in range(3, 4):
            self.carBricks.append(Brick(Position(80 + i * 70, 230), ORANGE,70,30,LIGHTGREY)) #Center of car
        for i in range(4, 9):
            self.carBricks.append(Brick(Position(80 + i * 70, 230), BLACK,70,30,LIGHTGREY)) #Center of car
        for i in range(9, 11):
            self.carBricks.append(Brick(Position(90 + i * 70, 230), BLACK,70,30,LIGHTGREY)) #Forward Tire
        for i in range(11, 13):
            self.carBricks.append(Brick(Position(90 + i * 70, 230), ORANGE,70,30,LIGHTGREY)) #front bumper

            
        #fifth row of car
        for i in range(0, 1):
            self.carBricks.append(Brick(Position(80 + i * 70, 200), ORANGE,70,30,LIGHTGREY))  
        for i in range(1, 3):
            self.carBricks.append(Brick(Position(80 + i * 70, 200), BLACK,70,30,LIGHTGREY))  
        for i in range(3, 4):
            self.carBricks.append(Brick(Position(80 + i * 70, 200), ORANGE,70,30,LIGHTGREY)) 
        for i in range(4, 7):
            self.carBricks.append(Brick(Position(80 + i * 70, 200), BLACK,70,30,LIGHTGREY)) 
        for i in range(7, 9):
            self.carBricks.append(Brick(Position(80 + i * 70, 200), ORANGE,70,30,LIGHTGREY)) #Forward section
        for i in range(9, 12):
            self.carBricks.append(Brick(Position(90 + i * 70, 200), ORANGE,70,30,LIGHTGREY)) #Forward section

            
        #sixth row of car
        for i in range(0, 7):
            self.carBricks.append(Brick(Position(90 + i * 70, 170), ORANGE,70,30,LIGHTGREY))  
        for i in range(7, 9):
            self.carBricks.append(Brick(Position(90 + i * 70, 170), BLACK,70,30,LIGHTGREY))  
        for i in range(9, 10):
            self.carBricks.append(Brick(Position(80 + i * 70, 170), ORANGE,70,30,LIGHTGREY)) 

        
        #Seventh row of car
        for i in range(2, 4):
            self.carBricks.append(Brick(Position(90 + i * 70, 140), ORANGE,70,30,LIGHTGREY))  
        for i in range(4, 9):
            self.carBricks.append(Brick(Position(90 + i * 70, 140), BLACK,70,30,LIGHTGREY))  

        
        #eight row of car
        for i in range(0, 2):
            self.carBricks.append(Brick(Position(50 + i * 70, 110), DARKGREY,70,30,LIGHTGREY))  
        for i in range(4, 8):
            self.carBricks.append(Brick(Position(90 + i * 70, 110), BLACK,70,30,LIGHTGREY))  

    def display(self, _win, _microseconds):
        for i in range(0, self.carBricks.__len__()):
            self.carBricks[i].display(_win, _microseconds)
        for i in range(0, self.wheelBricks.__len__()):
            self.wheelBricks[i].display(_win, _microseconds)

    def checkCollisions(self, _ball, _microseconds):
        for i in range(0, self.carBricks.__len__()):
            if self.carBricks[i].checkCollision(_ball, _microseconds):
                del self.carBricks[i]
                return
        for i in range(0, self.wheelBricks.__len__()):
            if self.wheelBricks[i].checkCollision(_ball, _microseconds):
                del self.wheelBricks[i]
                return

    def checkLevelComplete(self):
        if self.carBricks.__len__() == 0 and self.wheelBricks.__len__() == 0:
            return True
        return False

    def drawScreen(self, _win, _width, _height):
        #CarBackground = pygame.transform.scale( pygame.image.load(os.path.join('Brick Game' , 'Assets', 'RaceCar.jpg')) , (_width, _height))
        CarBackground = pygame.transform.scale( pygame.image.load(os.path.join('Brick Game' , 'Assets', 'RaceCar2.png')) , (_width, _height))
        #CarBackground = pygame.transform.scale( pygame.image.load(os.path.join('Brick Game' , 'Assets', 'MetalCar.jpg')) , (_width, _height))  Too low, sometimes paddle collision misses
        #CarBackground = pygame.transform.scale( pygame.image.load(os.path.join('Brick Game' , 'Assets', 'YellowCar.png')) , (_width, _height))  incorrect proportions
        #CarBackground = pygame.transform.scale( pygame.image.load(os.path.join('Brick Game' , 'Assets', 'StreetCar.jpg')) , (_width, _height))  paddle collision misses
        _win.blit(CarBackground, (0, 0))
        #pygame.draw.rect(_win, BLACK, pygame.Rect(0, 0, _width, _height), 0, 0)
