import pygame
from random import uniform
from time import sleep

#Player class
class Playeractive():
    def __init__(self, posx, posy):
        self.image = pygame.Surface((25, 150))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.speed = 4
    
    def move(self, ymove):
        self.rect.y += ymove * self.speed

#Ball class
class Ball():
    def __init__(self, posx, posy):
        #surface
        self.image = pygame.image.load("assets/images/pongball.png")
        # self.image = pygame.Surface((25,25))
        # self.image.fill((0,0,255))
        #keeps track of position
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        #x/y direction
        self.xmove = -.5
        self.ymove = 0
        #speed
        self.speed = 5

    #moves the ball
    def move(self):
        self.rect.x += self.xmove * self.speed
        self.rect.y += self.ymove * self.speed

    #bounces the ball of surfaces
    # 0 is a horizontal bounce, 1 is a vertical bounce
    def bounce(self, direction):
        multiplier = (-1 + uniform(-2.5, 2.5))

        #horizontal
        if direction == 0:
            self.xmove *= -1
            if self.ymove <= 0:
                self.ymove = uniform(.5, 2.5)
            elif self.ymove >= 0:
                self.ymove = uniform(-.5, -2.5)
        #vertical
        if direction == 1:
            self.ymove *= -1
            if self.xmove >= 0:
                self.xmove = uniform(.5, 2.0)
            elif self.xmove <= 0:
                self.xmove = uniform(-.5, -2.0)
    
    #collision check
    def collide(self, player):
        return self.rect.colliderect(player.rect)

#button class
class Button():
    def __init__(self, text, font, posx, posy):
        self.image = font.render(text, True, (0, 0, 0), (237, 237, 237))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
    
    #draws buttons onto the screen
    def Draw(self, surface):
        surface.blit(self.image, self.rect)

    #checks for clicks    
    def Click(self, mouse):
        if mouse[0] > self.rect.topleft[0] and mouse[0] < self.rect.topright[0]:
            if mouse[1] > self.rect.topleft[1] and mouse[1] < self.rect.bottomleft[1]:
                return True

def single(display):
    #framerate
    clock = pygame.time.Clock()
    FPS = 60

    #frame buffer for collision detection
    buffer = 10

    #initialize scoreboard/countdown fonts
    scorefont = pygame.font.SysFont("arial", 30)
    count = (3,2,1)
    countfont = pygame.font.SysFont("arial", 100)
    
    #initialize players
    Player1 = Playeractive(50, 200)
    Player2 = Playeractive(950, 200)

    #scores/goals
    p1score = 0
    p2goal = False

    #hearts
    heart = pygame.image.load("assets/images/heart.png")

    #initialize ball
    Pball = Ball(500, 300)

    gstart = True
    gamewon = False
    lives = 5

    while True:
        #event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
        #movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            if Player1.rect.y >= 0:
                Player1.move(-1)
        elif pressed[pygame.K_s]:
            if Player1.rect.y <= 600 - 150:
                Player1.move(1)
        
        #AI movement
        Player2.rect.y = Pball.rect.center[1] - 75

        #check for vertical bounce
        if Pball.rect.y <= 0 or Pball.rect.y >= 575:
            Pball.bounce(1)

        #collision detection/bouncing
        if Pball.collide(Player1) or Pball.collide(Player2):
            if buffer <= 0:
                Pball.bounce(0)
                buffer = 10
        if Pball.collide(Player1):
            p1score += 1
        
        #scoring
        if Pball.rect.x <= 0:
            p2goal = True
            gstart = True

        #moves the ball
        Pball.move()

        #update the score
        text = "Score: " + str(p1score)
        scoreboard = scorefont.render(text, True, (0, 0, 0), (237, 237, 237))

        #drawing
        #clears the screen
        display.fill((255,255,255))

        #drawing
        #hearts
        i = 1
        while i <= lives:
            heartx =  75 + 35 * (i - 1)
            display.blit(heart, (heartx, 10))
            i += 1

        display.blit(Player1.image, Player1.rect)
        display.blit(Player2.image, Player2.rect)
        display.blit(scoreboard, (500, 50))
        display.blit(Pball.image, Pball.rect)

        #updates
        pygame.display.update()
        clock.tick(FPS)
        buffer -= 1

        ##########################
        ##########################
        #countdown for game start/scoring
        while gstart:
            #goals
            
            if p2goal:
                lives -= 1
                p2goal = False
            
            #gameover
            if lives == 0:
                #update highscore
                #read highscore
                highscore = open("highscore.txt", "r")
                hs = highscore.readline()
                hs = int(hs)
                highscore.close()
                # overwrite highscore
                if p1score > hs:
                    highscore = open("highscore.txt", "w")
                    highscore.write(str(p1score))
                    highscore.close()
                    hs = p1score
                #gameover screen
                if gameover(display, p1score, "volley"):
                    p1score = 0
                    lives = 5
                else:
                    return hs
            
            #countdown
            for num in count:
                counter = countfont.render(str(num), True, (0,0,0), (237, 237, 237))
                display.blit(counter, (500,200))
                pygame.display.update()
                clock.tick(FPS)
                sleep(1)   
            #reset paddles/ball
            Player1.rect.y = 200
            Player2.rect.y = 200
            Pball.rect.y = 300
            Pball.rect.x = 500
            Pball.xmove = -.5
            Pball.ymove = 0 
            gstart = False

def vs(display):

    #framerate
    clock = pygame.time.Clock()
    FPS = 60

    #frame buffer for collision detection
    buffer = 10

    #initialize scoreboard/countdown fonts
    scorefont = pygame.font.SysFont("arial", 30)
    count = (3,2,1)
    countfont = pygame.font.SysFont("arial", 100)
    

    #initialize players
    Player1 = Playeractive(50, 200)
    Player2 = Playeractive(950, 200)

    #scores/goals
    p1score = 0
    p2score = 0
    p1goal = False
    p2goal = False

    #initialize ball
    Pball = Ball(500, 300)

    gstart = True
    gamewon = False
    while True:
        #event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
        #movement
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            if Player1.rect.y >= 0:
                Player1.move(-1)
        elif pressed[pygame.K_s]:
            if Player1.rect.y <= 600 - 150:
                Player1.move(1)
        if pressed[pygame.K_UP]:
            if Player2.rect.y >= 0:
                Player2.move(-1)
        elif pressed[pygame.K_DOWN]:
            if Player2.rect.y <= 600 -150:
                Player2.move(1)
        
        #check for vertical bounce
        if Pball.rect.y <= 0 or Pball.rect.y >= 575:
            Pball.bounce(1)

        #collision detection/bouncing
        if Pball.collide(Player1) or Pball.collide(Player2):
            if buffer <= 0:
                Pball.bounce(0)
                buffer = 10

        #moves the ball
        Pball.move()

        #scoring
        if Pball.rect.x >= 1000:
            p1goal = True
            gstart = True
        
        if Pball.rect.x <= 0:
            p2goal = True
            gstart = True
        
        #update the score
        text = str(p1score) + "-" + str(p2score)
        scoreboard = scorefont.render(text, True, (0, 0, 0), (237, 237, 237))
        #drawing
        #clears the screen
        display.fill((255,255,255))

        #draws
        display.blit(Player1.image, Player1.rect)
        display.blit(Player2.image, Player2.rect)
        display.blit(scoreboard, (500, 50))
        display.blit(Pball.image, Pball.rect)

        #updates
        pygame.display.update()
        clock.tick(FPS)
        buffer -= 1

        ##########################
        ##########################
        #countdown for game start/scoring
        while gstart:
            #goals
            if p1goal:
                p1score += 1
                p1goal = False
            if p2goal:
                p2score += 1
                p2goal = False
            
            #winning
            if p1score == 10:
                win = 1
                gamewon = True
                break
            elif p2score == 2:
                win = 2
                gamewon = True
                break

            for num in count:
                counter = countfont.render(str(num), True, (0,0,0), (237, 237, 237))
                display.blit(counter, (500,200))
                pygame.display.update()
                clock.tick(FPS)
                sleep(1)   
            #reset paddles/ball
            Player1.rect.y = 200
            Player2.rect.y = 200
            Pball.rect.y = 300
            Pball.rect.x = 500
            Pball.xmove = -.5
            Pball.ymove = 0 
            gstart = False
        
        #winning
        if p1score == 10:
            win = 1
            gamewon = True
        elif p2score == 10:
            win = 2
            gamewon = True
        
        if gamewon:
            if gameover(display, win, "vs"):
                gstart = True
                p1score = 0
                p2score = 0
                gamewon = False
            else:
                return

#restarts the game
#use gstart, pscore(s), and pgoal(s)
def gameover(display, winner, mode):
    font = pygame.font.SysFont("arial", 30)
    clock = pygame.time.Clock()
    FPS = 60

    #clears screen
    display.fill((255,255,255))
    pygame.display.update()

    #make buttons/text
    if mode == "vs":
        text = font.render("Player " + str(winner) + " Wins! " + "Would you like to play again?", True, (0,0,0), (237,237,237))
        textpos = (200, 100)
    elif mode == "volley":
        text = font.render("Would you like to play again?", True, (0,0,0), (237,237,237))
        textpos = (350, 100)
        score = font.render("Score: " + str(winner), True, (0,0,0), (237,237,237))
        scorepos = (475, 200)
    yesbutton = Button("Yes", font, 275, 300)
    nobutton = Button("No", font, 700, 300)

    game = True
    while game:
        #update mouse position
        mouse = pygame.mouse.get_pos()

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if nobutton.Click(mouse):
                    return False
                if yesbutton.Click(mouse):
                    return True
        #drawing
        display.fill((255,255,255))
        display.blit(text, textpos)
        if mode == "volley":
            display.blit(score, scorepos)
        yesbutton.Draw(display)
        nobutton.Draw(display)
        pygame.display.update()
        clock.tick(FPS)