import pygame
import time
import random

class GameLogic:
    def __init__(self):
        self.score = 0
        self.strikes = 0
        self.max_strikes = 3
        self.active_fruits = []  # List of fruits currently on screen
        self.frozen = False  # Indicates if time is stopped (ice fruit sliced)
        self.freeze_time = 0
        self.fruit_types = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']

    def handle_key_press(self, key):
        """Handles key press and checks if it matches a fruit on screen."""
        fruits_to_remove = []
        combo_count = 0

        for fruit in self.active_fruits:
            if fruit["name"] == key:
                self.apply_fruit_effect(fruit)
                fruits_to_remove.append(fruit)
                combo_count += 1
        
        if combo_count > 1:
            self.check_combo(combo_count)
        
        for fruit in fruits_to_remove:
            self.active_fruits.remove(fruit)
    
    def apply_fruit_effect(self, fruit):
        """Applies the effect of the fruit (score, freeze, explosion)."""
        if fruit["name"] in ["melon", "orange", "pomegranate", "guava"]:
            self.update_score(1)
        elif fruit["name"] == "bomb":
            self.end_game()  # Instantly lose the game
    
    def check_combo(self, count):
        """Adds bonus points for combos."""
        combo_bonus = count - 1  # Ex: 2 fruits = +1, 3 fruits = +2
        self.update_score(combo_bonus)
    
    def add_strike(self):
        """Adds a strike if a fruit reaches the bottom of the screen."""
        self.strikes += 1
        if self.strikes >= self.max_strikes:
            self.end_game()
    
    def update_score(self, points):
        """Adds points to the score."""
        self.score += points
    
    def end_game(self):
        """Triggers the end of the game."""
        print(f"Game Over! Final Score: {self.score}")
        pygame.quit()
        exit()
    
    def update_game_state(self):
        """Updates the game state by removing expired fruits and handling time freeze."""
        if self.frozen and time.time() > self.freeze_time:
            self.frozen = False  # Disable ice fruit effect
        
        for fruit in self.active_fruits:
            if fruit["y"] > 600:  # Assume screen height is 600px
                self.add_strike()
                self.active_fruits.remove(fruit)
    
    def spawn_fruit(self):
        """Adds a new random fruit to the screen."""
        fruit_name = random.choice(self.fruit_types)
        new_fruit = {"name": fruit_name, "y": 0}  # Representing a fruit as a dictionary
        self.active_fruits.append(new_fruit)
