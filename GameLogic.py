import pygame
import time
import random
import json

SCORE_FILE = "scores.json"

def load_best_score():
    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("best_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_best_score(score):
    best_score = load_best_score()
    if score > best_score:
        with open(SCORE_FILE, "w") as file:
            json.dump({"best_score": score}, file)

def init_game():
    return {
        "score": 0,
        "strikes": 0,
        "max_strikes": 3,
        "active_fruits": [],
        "fruit_types": ['melon', 'orange', 'pomegranate', 'guava', 'bomb'],
        "best_score": load_best_score()
    }

def handle_key_press(game_data, key):
    fruits_to_remove = []
    combo_count = 0

    for fruit in game_data["active_fruits"]:
        if fruit["name"] == key:
            apply_fruit_effect(game_data, fruit)
            fruits_to_remove.append(fruit)
            combo_count += 1
    
    if combo_count > 1:
        check_combo(game_data, combo_count)
    
    for fruit in fruits_to_remove:
        game_data["active_fruits"].remove(fruit)

def apply_fruit_effect(game_data, fruit):
    if fruit["name"] in ["melon", "orange", "pomegranate", "guava"]:
        update_score(game_data, 1)
    elif fruit["name"] == "bomb":
        end_game(game_data)

def check_combo(game_data, count):
    combo_bonus = count - 1
    update_score(game_data, combo_bonus)

def add_strike(game_data):
    game_data["strikes"] += 1
    if game_data["strikes"] >= game_data["max_strikes"]:
        end_game(game_data)

def update_score(game_data, points):
    game_data["score"] += points

def end_game(game_data):
    print(f"Game Over! Final Score: {game_data['score']}")
    save_best_score(game_data["score"])
    pygame.quit()
    exit()

def update_game_state(game_data):
    for fruit in game_data["active_fruits"][:]:
        if fruit["y"] > 600:
            add_strike(game_data)
            game_data["active_fruits"].remove(fruit)

def spawn_fruit(game_data):
    fruit_name = random.choice(game_data["fruit_types"])
    new_fruit = {"name": fruit_name, "y": 0}
    game_data["active_fruits"].append(new_fruit)
