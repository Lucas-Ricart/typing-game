#fruit slicer
import pygame
import random

pygame.init()

fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
HEIGHT = 480
WIDTH = 854
WHITE =(255, 255, 255)
FPS = 15
clock = pygame.time.Clock()
pygame.display.set_caption("typing_game.py")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))


def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),               
        'y' : 800,
        'speed_x': random.randint(-10,10),    
        'speed_y': random.randint(-80, -60),    
        'throw': False,                       
        't': 0,                               
        'hit': False,
    }
    if random.random() >= 0.75:     
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

running = True
while running :
    gameDisplay.fill((WHITE))
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
    
    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1
            if value['y'] <= WIDTH:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()