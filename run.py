import pygame
from classes import Button, vs, single

#intialize pygame
pygame.init()

#intialize framerate
clock = pygame.time.Clock()
FPS = 60

#initialize display
dislen = 1000
diswid = 600
gamewindow = pygame.display.set_mode((dislen, diswid))
pygame.display.set_caption("Pong+")

#intialize fonts
titlefont = pygame.font.SysFont("arial", 50)
buttonfont = pygame.font.SysFont("arial", 30)

#initializes text
title = Button("Pong+", titlefont, 425, 100)
singleplayerbutton = Button("Volley Mode", buttonfont, 225, 300)
multiplayerbutton = Button("VS Match", buttonfont, 600, 300)


game = True
while game == True:

    #update mouse position
    mouse = pygame.mouse.get_pos()

    #event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if multiplayerbutton.Click(mouse):
                vs(gamewindow)
            if singleplayerbutton.Click(mouse):
                single(gamewindow)
            
    #drawing
    #clears the screen
    gamewindow.fill((255,255,255))

    #draws
    title.Draw(gamewindow)
    singleplayerbutton.Draw(gamewindow)
    multiplayerbutton.Draw(gamewindow)
    
    #updates
    pygame.display.update()
    clock.tick(FPS)

#exiting
pygame.quit()
quit()