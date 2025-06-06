import numpy as np
import random
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_max_height(arena):
    for y in range(20):
        if np.any(arena[y, :] == 1):
            return 20 - y
    return 0

def get_holes(arena):
    holes = 0
    for x in range(12):
        column = arena[:, x]
        first_block = np.where(column == 1)[0]
        if len(first_block) > 0:
            top = first_block[0]
            holes += np.sum(column[top:] == 0)
    return holes

def get_bumpiness(arena):
    heights = [np.where(arena[:, x] == 1)[0][0] if np.any(arena[:, x] == 1) else 20 for x in range(12)]
    bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(11))
    return bumpiness

def simulate_drop(arena, piece, pos_x):
    arena_copy = np.copy(arena)
    pos = {'x': pos_x, 'y': 0}
    while True:
        pos['y'] += 1
        for y, row in enumerate(piece):
            for x, val in enumerate(row):
                if val and (pos['y'] + y >= 20 or arena_copy[pos['y'] + y, pos['x'] + x]):
                    pos['y'] -= 1
                    for y, row in enumerate(piece):
                        for x, val in enumerate(row):
                            if val:
                                arena_copy[pos['y'] + y, pos['x'] + x] = 1
                    return arena_copy, pos['y']
    return arena_copy, pos['y']

def get_binned_state(state):
    arena = np.array(state['arena'])
    max_height = get_max_height(arena)
    holes = get_holes(arena)
    pieces = ['T', 'O', 'L', 'J', 'I', 'S', 'Z']
    current_piece = state['currentPiece']
    piece_key = None
    for i, piece in enumerate(pieces):
        piece_matrix = (
            [[0, 0, 0], [1, 1, 1], [0, 1, 0]] if piece == 'T' else
            [[1, 1], [1, 1]] if piece == 'O' else
            [[0, 0, 1], [1, 1, 1], [0, 0, 0]] if piece == 'L' else
            [[1, 0, 0], [1, 1, 1], [0, 0, 0]] if piece == 'J' else
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]] if piece == 'I' else
            [[0, 1, 1], [1, 1, 0], [0, 0, 0]] if piece == 'S' else
            [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
        )
        piece_matrix_np = np.array(piece_matrix)
        current_piece_np = np.array(current_piece)
        matches = False
        for _ in range(4):
            if np.array_equal(current_piece_np, piece_matrix_np):
                matches = True
                break
            piece_matrix_np = np.rot90(piece_matrix_np)
        if matches:
            piece_key = piece
            break
    if piece_key is None:
        piece_key = pieces[0]
    pos_x = state['position']['x']
    height_bin = min(3, max_height // 5)
    holes_bin = min(2, holes // 3)
    pos_x_bin = min(3, pos_x // 3)
    return (piece_key, height_bin, holes_bin, pos_x_bin)

def load_q_table():
    try:
        with open('best_q_table.json', 'r') as f:
            q_table_raw = json.load(f)
        q_table = {}
        for k, v in q_table_raw.items():
            state_action = eval(k)
            q_table[state_action] = v
        print("Q-tabela wczytana z pliku q_table.json")
        return q_table
    except FileNotFoundError:
        print("Błąd: Plik q_table.json nie istnieje. Uruchom najpierw train_model.py, aby wytrenować model.")
        exit(1)

q_table = load_q_table()

def get_action(state, training=False):
    binned_state = get_binned_state(state)
    actions = ['left', 'right', 'rotate', 'drop']
    q_values = [q_table.get((binned_state, action), 0) for action in actions]
    max_q = max(q_values) if q_values else 0
    best_actions = [action for action, q in zip(actions, q_values) if q == max_q]
    q_action = random.choice(best_actions)

    if max_q > 0:
        return q_action

    best_action = None
    best_score = float('-inf')
    arena = np.array(state['arena'])
    piece = state['currentPiece']
    pos_x = state['position']['x']

    for dx in range(-5, 6):
        for rot in range(4):
            piece_copy = np.array(piece)
            for _ in range(rot):
                piece_copy = np.rot90(piece_copy)
            new_pos_x = pos_x + dx
            if new_pos_x < 0 or new_pos_x + piece_copy.shape[1] > 12:
                continue
            new_arena, drop_y = simulate_drop(arena, piece_copy.tolist(), new_pos_x)
            holes = get_holes(new_arena)
            bumpiness = get_bumpiness(new_arena)
            max_height = get_max_height(new_arena)
            score = -holes * 2 - bumpiness * 1 - max_height * 1
            if score > best_score:
                best_score = score
                if dx < 0:
                    best_action = 'left'
                elif dx > 0:
                    best_action = 'right'
                elif rot > 0:
                    best_action = 'rotate'
                else:
                    best_action = 'drop'

    if best_action is None:
        best_action = q_action
    return best_action

def play_in_browser():
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "main.html")
        driver.get(f"file:///{html_path}")
        print("Gra uruchomiona w przeglądarce (tryb widoczny).")

        def get_game_state():
            state = driver.execute_script("return window.tetris.getGameState();")
            if 'game_over' not in state:
                print("Błąd: 'game_over' nie znaleziono w stanie gry. Sprawdź main.html.")
                raise KeyError("'game_over' not found in game state")
            return state

        def send_ai_control(move=0, rotate=0, drop=False):
            control = {"move": move, "rotate": rotate, "drop": drop}
            driver.execute_script(f"window.tetris.setAIControl({json.dumps(control)});")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "game-container"))
        )
        print("Oczekiwanie na wybór trybu gry...")
        while True:
            try:
                start_menu = driver.execute_script("return document.getElementById('start-menu').classList.contains('active');")
                if not start_menu:
                    break
                time.sleep(0.5)
            except Exception as e:
                print(f"Błąd podczas sprawdzania menu startowego: {e}")
                break

        is_ai_game = driver.execute_script("return window.tetris.isAIGame();")
        print(f"Wybrano tryb: {'AI' if is_ai_game else 'Gracz'}")

        while True:
            try:
                state = get_game_state()
                if state['game_over']:
                    print(f"Gra zakończona. Wynik: {state['score']}")
                    print("Czekam na wybór trybu ponownej gry w przeglądarce...")
                    while state['game_over']:
                        time.sleep(1)
                        state = get_game_state()
                    is_ai_game = driver.execute_script("return window.tetris.isAIGame();")
                    print(f"Nowy tryb gry: {'AI' if is_ai_game else 'Gracz'}")
                else:
                    if is_ai_game:
                        action = get_action(state, training=False)
                        if action == 'left':
                            send_ai_control(move=-1)
                        elif action == 'right':
                            send_ai_control(move=1)
                        elif action == 'rotate':
                            send_ai_control(rotate=1)
                        elif action == 'drop':
                            send_ai_control(drop=True)
                    time.sleep(0.01)
            except Exception as e:
                print(f"Błąd w pętli gry: {e}")
                break
    except Exception as e:
        print(f"Błąd Selenium: {e}")
        print("Przeglądarka pozostanie otwarta. Możesz ją ręcznie zamknąć.")
    finally:
        print("Skrypt zakończony. Przeglądarka pozostaje otwarta.")

if __name__ == "__main__":
    play_in_browser()