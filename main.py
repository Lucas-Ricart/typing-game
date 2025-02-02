# Fruit Slicer
import pygame
import random

pygame.init()
pressed = ""
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube']
# Define dimensions
HEIGHT = 480
WIDTH = 854
DIMENSIONS = WIDTH, HEIGHT

# Define button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (170, 170, 170)
LIGHT_GREY = (200, 200, 200)

# Define refresh
FPS = 15
clock = pygame.time.Clock()

#Define window
pygame.display.set_caption("typing_game.py")
gameDisplay = pygame.display.set_mode((DIMENSIONS))

# Define fonts
FONT = pygame.font.Font(None, 50)

# Load background image
BACKGROUND = pygame.image.load("assets/background.png")

def spawn_fruit(fruit) :
    '''Generate fruits'''
    fruit_path = "assets/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,WIDTH-100),
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

def draw_fruit(key, value) :
    '''Draw entities and associate letters'''
    if value['y'] <= HEIGHT :
        value['img'] = pygame.transform.rotate(value['img'], 90)            #rotate the fruit
        gameDisplay.blit(value['img'], value['img'].get_rect(center=(value['x'], value['y'])))
        rect = value['img'].get_rect(center=(value['x'], value['y']))
        center_x = rect.left
        center_y = rect.top
        if not value['hit'] :           #letter disappear when hit
            draw_text(str(value['letter']).strip("[]'"), FONT, BLACK, gameDisplay, center_x, center_y)
            draw_text(str(value['letter']).strip("[]'"), FONT, WHITE, gameDisplay, center_x + 1, center_y + 1)
    else :
        spawn_fruit(key)

def cut(key, value, pressed) :
    '''Manage cutting animations'''
    if not value['hit'] and pressed == str(value['letter']).strip("[]'") :
        if key == 'bomb' :
            half_fruit_path = "assets/explosion.png"
        elif key == 'ice_cube' :
            half_fruit_path = "assets/break_ice_cube.png"
        else :
            half_fruit_path = "assets/half_" + key + ".png"
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
    elif value['hit'] :
        if key == 'bomb' :
            None
        else :
            half_fruit_path = "assets/half_" + key + ".png"
            value['img'] = pygame.image.load(half_fruit_path)
                

def update_fruit_positions(key, value, pressed) :
    '''Modify fruits position'''
    if value['throw']:
        value['x'] += value['speed_x']
        value['y'] += value['speed_y']
        value['speed_y'] += value['gravity']
        value['gravity'] += 0.3         #dropping speed
        if value['x'] <= value['img'].get_width() // 3 or value['x'] >= WIDTH - value['img'].get_width() // 3 :
            value['speed_x'] *= -1
        draw_fruit(key, value)
    else:
        spawn_fruit(key)
    cut(key, value, pressed)

def game_loop() :
    while True :
        gameDisplay.blit(BACKGROUND, (0, 0))
        pressed = ""
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if 97 <= event.key <= 122 :
                    pressed = chr(event.key).upper()
            
        for key, value in data.items():
            update_fruit_positions(key, value, pressed) 
        
        pygame.display.update()
        clock.tick(FPS)

data = {}
letters = ['Z', 'Q', 'S', 'D']          #letters to press to hit fruits

for fruit in fruits:
    spawn_fruit(fruit)

"""attention ajout code lorenzo"""


# Load background music
LOOP = pygame.mixer.Sound("assets/lemon_jelly.mp3")
BUTTON_SOUND = pygame.mixer.Sound("assets/button.mp3")
LOOP.play(-1)         # Play the music in a loop

def draw_text(text, font, color, surface, x, y):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

def spawn_fruit_menu(fruit) :
    fruit_path = "assets/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,WIDTH-100),
        'y' : random.randint(100,HEIGHT-100),
        'speed_x': random.choice([-10,10]),          #lateral speed
        'speed_y': random.choice([-10, 10]),            #elevating speed
        'throw': True,
        'gravity': 0.2,
        'hit': True,
        'letter':random.choice(letters)
    }
def move(key, value) :
    if value['throw']:
        value['x'] += value['speed_x'] + value['gravity']
        value['y'] += value['speed_y'] + value['gravity']
        if value['x'] <= value['img'].get_width() // 3 or value['x'] >= WIDTH - value['img'].get_width() // 3 :
            value['speed_x'] = -value['speed_x']
        elif value['y'] <= value['img'].get_height() // 3 or value['y'] >= HEIGHT - value['img'].get_height() // 3 :
            value['speed_y'] = -value['speed_y']
    else :
        spawn_fruit_menu(key)
def main_menu():
    while True:
        # Draw the background
        gameDisplay.blit(BACKGROUND, (0, 0))
        for key, value in data.items() :
            if key == 'ice_cube' :
                None
            else :
                draw_fruit(key, value)
                move(key, value)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    cut(key, value, pressed)
                    game_loop()
                if score_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    show_scores()
                if quit_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    clock.tick(8)
                    pygame.quit()

        # Draw the title
        draw_text("FRUIT SLICER", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 8)
        draw_text("FRUIT SLICER", FONT, WHITE, gameDisplay, WIDTH // 2 + 1, HEIGHT // 8 + 1)

        # Draw the buttons
        start_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT * 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
        score_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
        quit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT * 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Change button color on hover
        if start_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(gameDisplay, GREY, start_button)
        else:
            pygame.draw.rect(gameDisplay, LIGHT_GREY, start_button)
        if score_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(gameDisplay, GREY, score_button)
        else:
            pygame.draw.rect(gameDisplay, LIGHT_GREY, score_button)
        if quit_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(gameDisplay, GREY, quit_button)
        else:
            pygame.draw.rect(gameDisplay, LIGHT_GREY, quit_button)

        # Draw button text
        draw_text("Jouer", FONT, BLACK, gameDisplay, start_button.centerx, start_button.centery)
        draw_text("Jouer", FONT, WHITE, gameDisplay, start_button.centerx + 1, start_button.centery + 1)
        draw_text("Score", FONT, BLACK, gameDisplay, score_button.centerx, score_button.centery)
        draw_text("Score", FONT, WHITE, gameDisplay, score_button.centerx + 1, score_button.centery + 1)
        draw_text("Quitter", FONT, BLACK, gameDisplay, quit_button.centerx, quit_button.centery)
        draw_text("Quitter", FONT, WHITE, gameDisplay, quit_button.centerx + 1, quit_button.centery + 1)

        pygame.display.update()
        clock.tick(FPS)

def show_scores():
    while True:
        # Draw the background
        gameDisplay.blit(BACKGROUND, (0, 0))
        for key, value in data.items() :
            if key == 'ice_cube' :
                None
            else :
                draw_fruit(key, value)
                move(key, value)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # Draw the scores (placeholder text)
        draw_text("Scores", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 4)
        draw_text("1. Player1 - 100", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 2)
        draw_text("2. Player2 - 80", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT)

        pygame.display.update()
        clock.tick(FPS)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()