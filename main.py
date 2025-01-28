#fruit slicer
import pygame

pygame.init()

HEIGHT = 480
WIDTH = 854
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman_Game.py")
run = True

while run :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False


pygame.quit()