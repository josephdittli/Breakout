# This is the class that runs the game.
# Joseph's breakout game is a classic breakout game with the twist that the bricks can move around.
# JBD 8/18/2021.

from Position import *
from CollidableObject import *
from Level import *
import datetime
import pygame
import os

class Launcher:
    def __init__(self):
        self.microseconds = 0
        self.lastSampling = datetime.datetime.now()
        self.currentLevel = 0
        self.levels = []
        self.levels.append(CarLevel())
        self.levels.append(TestLevel())
        self.WIDTH = 1040
        self.HEIGHT = 600
        pygame.init()
        info = pygame.display.Info()
        size = width, height = info.current_w, info.current_h
        self.WINWIDTH = width
        self.WINHEIGHT = height
        self.WIN = pygame.display.set_mode(size)
        self.screen = pygame.Surface((1040,600))
        pygame.display.set_caption("Joseph's breakout game")
        self.createBall()
        self.createPaddle()
        self.createWalls()

    def createBall(self):      
        ballMovement = FreeMovement(520,400,0,0,0,0,100000)  #stationary ball
        self.ball = Ball(ballMovement)

    def createWalls(self):      
        self.walls = Walls(self.HEIGHT, self.WIDTH)

    def createPaddle(self):
        paddleMovement = FreeMovement(self.WIDTH/2,self.HEIGHT-10,0,0,0,0,100000)
        self.paddle = Paddle(paddleMovement)

    # Called periodically, as several methods in the Position class will use the time variables to determine position of objects.
    def updateTime(self):
        now = datetime.datetime.now()
        elapsed = now - self.lastSampling
        self.microseconds = self.microseconds + elapsed.microseconds
        self.lastSampling = now    
        
    # Advance the level.  If that was the last level, we won.
    def checkVictoryAfterAdvanceLevel(self):
        self.currentLevel += 1
        if self.currentLevel >= self.levels.__len__():
            return True
        self.createBall()
        self.createPaddle()
        self.createWalls()
        self.microseconds = 0
        return False

    # Refresh the screen and call the various display methods in my owned objects.
    def display(self):                
        self.screen.fill(BLACK)     
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))           
        self.levels[self.currentLevel].drawScreen(self.screen, self.WIDTH, self.HEIGHT)
        self.levels[self.currentLevel].display(self.screen, self.microseconds)
        #draw ball and paddle
        self.ball.display(self.screen, self.microseconds)
        self.paddle.display(self.screen, self.microseconds)
        self.WIN.blit(pygame.transform.scale(self.screen, (self.WINWIDTH, self.WINHEIGHT)), (0,0))
        pygame.display.update()

    # Handle paddle movement based on mouse movement.  
    # I choose to go with velocity rather than absolute position here, which gives the paddle a bit of a lag
    # A bigger problem is when the mouse goes off the monitor and has to come back on the monitor in order to start moving
    # the paddle again.  I think it would be better to base movement on mouse delta as opposed to mouse absolute value.
    def setPaddleVelocity(self, _microseconds):
        MouseXPos = pygame.mouse.get_pos()[0] * self.WIDTH / self.WINWIDTH
        if MouseXPos < 0:
            MouseXPos = 0
        if MouseXPos > self.WIDTH - self.paddle.width:
            MouseXPos = self.WIDTH - self.paddle.width
        distance = MouseXPos - self.paddle.Position.getXPos(_microseconds)
        velocity = distance / 3
        if velocity > 10:
            velocity += 5
        if velocity < -10:
            velocity -= 5
        self.paddle.Position.setVelocity(velocity, 0)

    def main(self):
        self.display()
        FPS = 60

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.updateTime()
            if self.microseconds > 2500000 and self.ball.Position.xVelocity == 0 and self.ball.Position.yVelocity == 0:
                #Start the ball moving.
                self.ball.Position.setVelocity(10,30)

            # Handle paddle movement based on mouse X position
            self.setPaddleVelocity(self.microseconds)
            self.levels[self.currentLevel].checkCollisions(self.ball, self.microseconds)
            self.paddle.checkCollision(self.ball, self.microseconds)
            self.walls.checkCollision(self.ball, self.microseconds)
            # Check victory
            if self.levels[self.currentLevel].checkLevelComplete():
                if self.checkVictoryAfterAdvanceLevel():
                    run = False
                    break         #todo:  Play some sort of victory music so they know they won the game.

            # Draw stuff
            self.display()
            # handle user quitting game or loosing the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == BALL_LOST:
                    pygame.time.delay(2500)
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
        
        pygame.quit()

myLauncher = Launcher()
myLauncher.main()
