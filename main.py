import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize the mixer for audio
pygame.mixer.init()

# Load background music
pygame.mixer.music.load(r"c:\\Users\\loren\\Downloads\\bruitage-bouton-v1-274125.mp3")
pygame.mixer.music.play(-1)  # Play the music in a loop

# Define window dimensions
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)

# Load background image
BACKGROUND = pygame.image.load(r"c:\\Users\\loren\Downloads\\Arrière-plan Réunion Virtuelle Élégant Générique pour la Nouvelle année en Noir et Doré  (1).png")

# Load fruit images
FRUITS = [pygame.image.load(r"c:\\Users\\loren\Downloads\\32343watermelon_98881.png") for _ in range(6)]

# Define fonts
FONT = pygame.font.Font(None, 74)
BUTTON_FONT = pygame.font.Font(None, 50)

# Define button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60

# Define fruit class
class Fruit:
    def __init__(self, image):
        self.image = image
        self.x = random.randint(0, WIDTH - image.get_width())
        self.y = random.randint(0, HEIGHT - image.get_height())
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5, 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0 or self.x >= WIDTH - self.image.get_width():
            self.speed_x *= -1
        if self.y <= 0 or self.y >= HEIGHT - self.image.get_height():
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    fruits = [Fruit(random.choice(FRUITS)) for _ in range(6)]
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint((mouse_x, mouse_y)):
                    game_loop()
                if score_button.collidepoint((mouse_x, mouse_y)):
                    show_scores()
                if quit_button.collidepoint((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()

        # Draw the background
        WINDOW.blit(BACKGROUND, (0, 0))

        # Move and draw fruits
        for fruit in fruits:
            fruit.move()
            fruit.draw(WINDOW)

        # Draw the title
        draw_text("", FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 4)

        # Draw the buttons
        start_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        score_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        quit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 2 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Change button color on hover
        if start_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(WINDOW, LIGHT_GRAY, start_button)
        else:
            pygame.draw.rect(WINDOW, GRAY, start_button)

        if score_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(WINDOW, LIGHT_GRAY, score_button)
        else:
            pygame.draw.rect(WINDOW, GRAY, score_button)

        if quit_button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(WINDOW, LIGHT_GRAY, quit_button)
        else:
            pygame.draw.rect(WINDOW, GRAY, quit_button)

        draw_text("Jouer", BUTTON_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 2)
        draw_text("Score", BUTTON_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT)
        draw_text("Quitter", BUTTON_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 2 + 2 * BUTTON_HEIGHT)

        pygame.display.flip()

def game_loop():
    fruits = [Fruit(random.choice(FRUITS)) for _ in range(10)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background
        WINDOW.blit(BACKGROUND, (0, 0))

        # Move and draw fruits
        for fruit in fruits:
            fruit.move()
            fruit.draw(WINDOW)

        # Draw a black rectangle in the center of the screen
        pygame.draw.rect(WINDOW, BLACK, (WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100))

        pygame.display.flip()

def show_scores():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # Draw the background
        WINDOW.blit(BACKGROUND, (0, 0))

        # Draw the scores (placeholder text)
        draw_text("Scores", FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 4)
        draw_text("1. Player1 - 100", BUTTON_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 2)
        draw_text("2. Player2 - 80", BUTTON_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
