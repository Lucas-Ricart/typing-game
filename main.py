#fruit slicer
import pygame
import random

pygame.init()

difficulty = 1
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
HEIGHT = 480
WIDTH = 854
DIMENSIONS = WIDTH, HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 25
clock = pygame.time.Clock()
pygame.display.set_caption("typing_game.py")
gameDisplay = pygame.display.set_mode((DIMENSIONS))
#fonts
font = pygame.font.SysFont(None, 50)


    
slash = pygame.image.load("images/slash.png")

def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,WIDTH-50),
        'y' : HEIGHT,
        'speed_x': random.randint(-15,15),
        'speed_y': random.randint(-38, -38),
        'throw': False,
        'gravity': 0,
        'hit': False,
        'letter':random.choice(letters)
    }
    if random.random() >= 0.99:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False
data = {}
A = 65
letters = []
for i in range(26) :
    letters.append([chr(A + i)])
for fruit in fruits:
    generate_random_fruits(fruit)

running = True
while running :
    pressed = ""
    gameDisplay.fill((BLACK))
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.KEYDOWN :
            if 97 <= event.key <= 122 :
                pressed = chr(event.key).upper()
                print(pressed)
        
    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['gravity'])
            value['gravity'] += 0.3
            if value['x'] <= 0 or value['x'] >= WIDTH-40 :
                value['speed_x'] = -value['speed_x']
            if value['y'] <= HEIGHT:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
                letter = str(value['letter']).strip("[]'")
                letter_surface = font.render(letter, 1, WHITE)
                gameDisplay.blit(letter_surface, letter_surface.get_rect(center=(value['x'], value['y'])))
            else:
                generate_random_fruits(key)
        else :
            generate_random_fruits(key)
        try :
            if not value['hit'] and pressed == value['letter'] :
                if key == 'bomb' :
                    half_fruit_path = "images/explosion.png"
                else :
                    half_fruit_path = "images/" + "half_" + key + ".png"
                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] = -value['speed_x']
                value['speed_y'] += -5
        except ValueError :
            None
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()