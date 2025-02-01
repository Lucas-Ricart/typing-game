#fruit slicer
import pygame
import random

pygame.init()

fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube']
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

def spawn_fruit(fruit):
    '''Generate fruits'''
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,WIDTH-40),
        'y' : HEIGHT,
        'speed_x': random.randint(-15,15),          #lateral speed
        'speed_y': random.randint(-38, -38),            #elevating speed
        'throw': False,
        'gravity': 0,
        'hit': False,
        'letter':random.choice(letters)
    }
    if random.random() >= 0.99:         #spawn rate
        if fruit == 'bomb' :          #reduce bomb spawn probability
            if random.random() >= 0.855 :
                data[fruit]['throw'] = True
        elif fruit == 'ice_cube' :            #reduce ice_cube spawn probability
            if random.random() >= 0.95 :
                data[fruit]['throw'] = True
        else :
            data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

def draw_fruit() :
    if value['y'] <= HEIGHT :
        value['img'] = pygame.transform.rotate(value['img'], 90)            #rotate the fruit
        gameDisplay.blit(value['img'], value['img'].get_rect(center=(value['x'], value['y'])))
        rect = value['img'].get_rect(center=(value['x'], value['y']))
        center_x = rect.left
        center_y = rect.top
        letter_surface = font.render(str(value['letter']).strip("[]'"), 1, WHITE)
        if not value['hit'] :           #letter disappear when hit
            gameDisplay.blit(letter_surface, letter_surface.get_rect(center=(center_x, center_y)))
    else :
        spawn_fruit(key)

def cut() :
            if not value['hit'] and pressed == str(value['letter']).strip("[]'") :
                if key == 'bomb' :
                    half_fruit_path = "images/explosion.png"
                elif key == 'ice_cube' :
                    half_fruit_path = "images/break_ice_cube.png"
                else :
                    half_fruit_path = "images/half_" + key + ".png"
                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] = -value['speed_x']            #fruit go in opposite direction
                if value['speed_y'] > 0 :           #if dropping fruit do a little jump
                    value['speed_y'] = 0
                    value['speed_y'] += -20
                else :
                    if value['speed_x'] < 0 :           #add a bit of speed
                        value['speed_x'] -= 5
                    else :
                        value['speed_x'] += 5
                value['hit'] = True

def update_fruit_positions() :
    if value['throw']:
        value['x'] += value['speed_x']
        value['y'] += value['speed_y']
        value['speed_y'] += (1 * value['gravity'])
        value['gravity'] += 0.3             #dropping speed
        if value['x'] <= 20 or value['x'] >= WIDTH-20 :
            value['speed_x'] = -value['speed_x']
        draw_fruit()
    else:
        spawn_fruit(key)
    cut()

data = {}
letters = ['Z', 'Q', 'S', 'D']          #letters to press to hit fruits

for fruit in fruits:
    spawn_fruit(fruit)

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
        
    for key, value in data.items():
        update_fruit_positions() 
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()