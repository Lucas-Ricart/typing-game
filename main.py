# Fruit Slicer
import pygame
import random
import json

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
        'hit': True,
        'letter':random.choice(letters)
    }
    if random.random() >= 0.99:         #spawn rate
        if fruit == 'bomb' :          #reduce bomb spawn probability
            if random.random() >= 0.855 :
                data[fruit]['throw'] = True
                data[fruit]['hit'] = False
        elif fruit == 'ice_cube' :            #reduce ice_cube spawn probability
            if random.random() >= 0.1 :
                data[fruit]['throw'] = True
                data[fruit]['hit'] = False
        else :
            data[fruit]['throw'] = True
            data[fruit]['hit'] = False
    else:
        data[fruit]['throw'] = False
        data[fruit]['hit'] = True
    

def draw_fruit(key, value, freeze) :
    '''Draw entities and associate letters'''
    if value['y'] <= HEIGHT :
        gameDisplay.blit(value['img'], value['img'].get_rect(center=(value['x'], value['y'])))
        rect = value['img'].get_rect(center=(value['x'], value['y']))
        center_x = rect.left
        center_y = rect.top
        if not value['hit'] :           #letter disappear when hit
            draw_text(str(value['letter']).strip("[]'"), FONT, BLACK, gameDisplay, center_x, center_y)
            draw_text(str(value['letter']).strip("[]'"), FONT, WHITE, gameDisplay, center_x + 1, center_y + 1)
    else :
        if freeze != True :
            spawn_fruit(key)

def cut(key, value, pressed, lives, freeze, score, combo_count) :
    '''Manage cutting animations'''
    if not value['hit'] and pressed == str(value['letter']).strip("[]'") :
        if key == 'bomb' :
            game_over(lives, freeze, score, combo_count)
        if key == 'ice_cube' :
            value['hit'] = True
            half_fruit_path = "assets/break_ice_cube.png"
            freeze_loop(lives, score, combo_count)
            combo_count += 1
            value['img'] = pygame.image.load(half_fruit_path)
        if key != 'bomb' and key != 'ice_cube':
            half_fruit_path = "assets/half_" + key + ".png"
            combo_count += 1
            value['img'] = pygame.image.load(half_fruit_path)    
        score += 1
        '''if combo_count > 4 :
            score += combo_count-1
        if combo_count > 3 :
            score += combo_count-1
        if combo_count > 2 :
            score += combo_count-1
        if combo_count > 1 :
            score += combo_count-1
        combo_count = 0'''
        print(combo_count)
        print(score)
        if freeze != True :
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
            half_fruit_path = "assets/explosion.png"
        elif key == 'ice_cube' :
            half_fruit_path = "assets/break_ice_cube.png"
        else :
            half_fruit_path = "assets/half_" + key + ".png"
        value['img'] = pygame.image.load(half_fruit_path)
    return score, combo_count            

def update_fruit_positions(key, value, pressed, lives, freeze, score, combo_count) :
    '''Modify fruits position'''
    if value['throw']:
        if freeze != True :
            value['img'] = pygame.transform.rotate(value['img'], 90)            #rotate the fruit
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += value['gravity']
            value['gravity'] += 0.3         #dropping speed
            if value['x'] <= value['img'].get_width() // 3 or value['x'] >= WIDTH - value['img'].get_width() // 3 :
                value['speed_x'] *= -1
        draw_fruit(key, value, freeze)
    else:
        if freeze != True :
            spawn_fruit(key)
    score, combo_count = cut(key, value, pressed, lives, freeze, score, combo_count)
    return score, combo_count

def draw_lives(lives, score) :
    # Load lives image
    first_life = pygame.image.load("assets/white_lives.png")
    second_life = pygame.image.load("assets/white_lives.png")
    third_life = pygame.image.load("assets/white_lives.png")
    if lives < 3 :
        first_life = pygame.image.load("assets/red_lives.png")
    if lives < 2 :
        second_life = pygame.image.load("assets/red_lives.png")
    if lives < 1 :
        third_life = pygame.image.load("assets/red_lives.png")
    gameDisplay.blit(first_life, (5, 0))
    gameDisplay.blit(second_life, (first_life.get_width() + 5, 0))
    gameDisplay.blit(third_life, (2 * first_life.get_width() + 5, 0))

    gameDisplay.blit(first_life, (5, 0))
    gameDisplay.blit(second_life, (first_life.get_width() + 5, 0))
    gameDisplay.blit(third_life, (2 * first_life.get_width() + 5, 0))

def display_score(score) :
                display_score1 = FONT.render(str(score), True, BLACK)
                display_score2 = FONT.render(str(score), True, WHITE)
                score_rect1 = display_score1.get_rect(topright=(WIDTH -4, 0))
                score_rect2 = display_score1.get_rect(topright=(WIDTH -5, 1))
                gameDisplay.blit(display_score1, score_rect1)
                gameDisplay.blit(display_score2, score_rect2)

def game_loop(lives, freeze, score, combo_count) :
    while True :
        gameDisplay.blit(BACKGROUND, (0, 0))
        pressed = ""
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    pause_menu()
                elif 97 <= event.key <= 122 :
                    pressed = chr(event.key).upper()
        for key, value in data.items():
            score, combo_count = update_fruit_positions(key, value, pressed, lives, freeze, score, combo_count)
            lives = counter(key, value, lives)
            draw_lives(lives, score)
            display_score(score)
            if lives == 0 :
                game_over(lives, freeze, score, combo_count)
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
    '''Move the fruits in the menus'''
    if value['throw']:
        value['img'] = pygame.transform.rotate(value['img'], 90)            #rotate the fruit
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
        freeze = False
        # Draw the background
        gameDisplay.blit(BACKGROUND, (0, 0))
        for key, value in data.items() :
            if key == 'ice_cube' :
                None
            else :
                draw_fruit(key, value, freeze)
                move(key, value)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    lives = 3
                    score = 0
                    combo_count = 0
                    cut(key, value, pressed, lives, freeze, score, combo_count)
                    game_loop(lives,freeze, score, combo_count)
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
        freeze = False
        # Draw the background
        gameDisplay.blit(BACKGROUND, (0, 0))
        for key, value in data.items() :
            if key == 'ice_cube' :
                None
            else :
                draw_fruit(key, value, freeze)
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

def counter(key, value, lives) :
    '''Deduce life on fail'''
    if key != 'bomb' and key != 'ice_cube' and not value['hit'] :
        if value['y'] > HEIGHT :
            lives -= 1
    return lives

def freeze_loop(lives, score, combo_count) :
    freeze = True
    for i in range(4 * FPS) :           #temps de pause
        gameDisplay.blit(BACKGROUND, (0, 0))
        pressed = ""
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    pause_menu()
                elif 97 <= event.key <= 122 :
                    pressed = chr(event.key).upper()
        for key, value in data.items():
            score, combo_count = update_fruit_positions(key, value, pressed, lives, freeze, score, combo_count)
            lives = counter(key, value, lives)
            draw_lives(lives, score)
            display_score(score)
        pygame.display.update()
        clock.tick(FPS)
    freeze = False

def game_over(lives, freeze, score, combo_count):
    save_score_to_json(score)           # Enregistrer le score dans un fichier JSON
    while True:
        gameDisplay.blit(BACKGROUND, (0, 0))
        draw_text("GAME OVER", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 4)
        draw_text("GAME OVER", FONT, WHITE, gameDisplay, WIDTH // 2 + 1, HEIGHT // 4 + 1)

        # Boutons du menu game over
        retry_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        main_menu_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    lives = 0
                    freeze = False
                    score = 0
                    combo_count = 0
                    game_loop(lives, freeze, score, combo_count)
                if main_menu_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    main_menu()


        # Dessiner les boutons
        pygame.draw.rect(gameDisplay, LIGHT_GREY, retry_button)
        pygame.draw.rect(gameDisplay, LIGHT_GREY, main_menu_button)
        draw_text("Restart", FONT, BLACK, gameDisplay, retry_button.centerx, retry_button.centery)
        draw_text("Menu", FONT, BLACK, gameDisplay, main_menu_button.centerx, main_menu_button.centery)

        pygame.display.update()
        clock.tick(FPS)

def pause_menu():
    while True :
        gameDisplay.blit(BACKGROUND, (0, 0))
        draw_text("PAUSE", FONT, BLACK, gameDisplay, WIDTH // 2, HEIGHT // 4)
        draw_text("PAUSE", FONT, WHITE, gameDisplay, WIDTH // 2 + 1, HEIGHT // 4 + 1)

        # Buttons
        resume_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        main_menu_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    return  # Reprendre le jeu
                if main_menu_button.collidepoint((mouse_x, mouse_y)):
                    BUTTON_SOUND.play()
                    main_menu()  # Retour au menu principal

        # Dessiner les boutons
        pygame.draw.rect(gameDisplay, LIGHT_GREY, resume_button)
        pygame.draw.rect(gameDisplay, LIGHT_GREY, main_menu_button)
        draw_text("Continue", FONT, BLACK, gameDisplay, resume_button.centerx, resume_button.centery)
        draw_text("Menu", FONT, BLACK, gameDisplay, main_menu_button.centerx, main_menu_button.centery)

        pygame.display.update()
        clock.tick(FPS)

def save_score_to_json(score):
    '''Save the score to a JSON file'''
    score_data = {"score": score}
    with open("score.json", "w") as file:
        json.dump(score_data, file)



if __name__ == "__main__":
    main_menu()