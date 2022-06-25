import pygame
from pygame.locals import *
import pyautogui
#_________________________
pygame.init()
height,width = pyautogui.size()
x = height/2.5
y = width/1.5
size = [x,y]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Monopoly World')

background = pygame.image.load("/Users/xx_hype_beast_xx/Desktop/Monopoly/board.png")
background = pygame.transform.scale(background,size)

def draw():
    screen.blit(background, [0,0])
    pygame.draw.circle(screen, (0, 0, 235),
                                     (x/2,y/2),
                                      13)

run = True
while run == True: 
    draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
            pygame.quit()
