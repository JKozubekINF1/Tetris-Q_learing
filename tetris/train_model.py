import numpy as np
import random
import json
import matplotlib.pyplot as plt

# --- Definicja klocków Tetrisa ---
pieces = {
    'T': [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
    'O': [[1, 1], [1, 1]],
    'L': [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
    'J': [[1, 0, 0], [1, 1, 1], [0, 0, 0]],
    'I': [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    'S': [[0, 1, 1], [1, 1, 0], [0, 0, 0]],
    'Z': [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
}

# --- Klasa symulacji Tetrisa ---
class TetrisSim:
    def __init__(self):
        self.reset()

    def reset(self):
        self.arena = np.zeros((20, 12), dtype=int)
        self.pos = {'x': 5, 'y': 0}
        self.current_key = random.choice(list(pieces.keys()))
        self.current = pieces[self.current_key]
        self.next_key = random.choice(list(pieces.keys()))
        self.next = pieces[self.next_key]
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.consecutive_clears = 0

    def collide(self):
        for y, row in enumerate(self.current):
            for x, val in enumerate(row):
                if val and (self.pos['y'] + y >= 20 or self.pos['x'] + x < 0 or
                            self.pos['x'] + x >= 12 or self.arena[self.pos['y'] + y, self.pos['x'] + x]):
                    return True
        return False

    def merge(self):
        for y, row in enumerate(self.current):
            for x, val in enumerate(row):
                if val:
                    self.arena[self.pos['y'] + y, self.pos['x'] + x] = 1

    def clear_lines(self):
        lines = np.all(self.arena == 1, axis=1)
        num_lines = np.sum(lines)
        self.score += num_lines * 100
        self.lines_cleared += num_lines
        self.arena = np.vstack((np.zeros((num_lines, 12), dtype=int), self.arena[~lines]))
        return num_lines

    def move(self, dx):
        self.pos['x'] += dx
        if self.collide():
            self.pos['x'] -= dx
            return False
        return True

    def rotate(self):
        old_piece = self.current
        self.current = np.rot90(self.current).tolist()
        if self.collide():
            self.current = old_piece
            return False
        return True

    def drop(self):
        self.pos['y'] += 1
        if self.collide():
            self.pos['y'] -= 1
            self.merge()
            lines_cleared = self.clear_lines()
            if lines_cleared > 0:
                self.consecutive_clears += 1
            else:
                self.consecutive_clears = 0
            self.current_key = self.next_key
            self.current = self.next
            self.next_key = random.choice(list(pieces.keys()))
            self.next = pieces[self.next_key]
            self.pos = {'x': 5, 'y': 0}
            if self.collide():
                self.game_over = True
            return lines_cleared
        return 0

    def get_state(self):
        return {
            'arena': self.arena.tolist(),
            'currentPiece': self.current,
            'current_key': self.current_key,
            'nextPiece': self.next,
            'next_key': self.next_key,
            'position': self.pos.copy(),
            'score': self.score,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over,
            'consecutive_clears': self.consecutive_clears
        }

# --- Funkcje pomocnicze ---
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
    surface = get_surface_profile(arena)
    return sum(abs(surface[i] - surface[i + 1]) for i in range(len(surface) - 1))

def get_potential_clears(arena):
    potential = 0
    for y in range(20):
        row = arena[y, :]
        filled = np.sum(row)
        if 8 <= filled <= 11:
            potential += 1
    return potential

def get_line_completeness(arena):
    completeness = 0
    for y in range(20):
        row = arena[y, :]
        filled = np.sum(row)
        if filled > 0 and filled < 12:
            completeness += filled / 12
    return completeness

def get_surface_profile(arena):
    surface = []
    for x in range(12):
        column = arena[:, x]
        first_block = np.where(column == 1)[0]
        surface.append(20 - first_block[0] if len(first_block) > 0 else 0)
    return surface

def get_piece_width(piece):
    return max(len(row) for row in piece)

def get_piece_height(piece):
    return sum(1 for row in piece if any(val == 1 for val in row))

def get_binned_state(state):
    arena = np.array(state['arena'])
    max_height = get_max_height(arena)
    holes = get_holes(arena)
    bumpiness = get_bumpiness(arena)
    potential_clears = get_potential_clears(arena)
    piece_key = state['current_key']
    next_piece_key = state['next_key']
    pos_x = state['position']['x']
    current_piece = state['currentPiece']
    piece_width = get_piece_width(current_piece)
    piece_height = get_piece_height(current_piece)
    surface = get_surface_profile(arena)
    lines_cleared = state['lines_cleared']

    height_bin = min(5, max_height // 4)
    holes_bin = min(4, holes // 2)
    bumpiness_bin = min(3, bumpiness // 10)
    potential_clears_bin = min(3, potential_clears)
    pos_x_bin = min(11, pos_x)
    width_bin = min(2, piece_width - 1) if piece_key != 'O' else 0
    height_piece_bin = min(2, piece_height - 1)
    surface_diff = np.std(surface) if surface else 0
    surface_bin = min(3, int(surface_diff // 2))
    lines_cleared_bin = min(3, lines_cleared // 10)

    return (piece_key, next_piece_key, height_bin, holes_bin, bumpiness_bin, potential_clears_bin, pos_x_bin, width_bin, height_piece_bin, surface_bin, lines_cleared_bin)

# --- Q-Learning ---
q_table = {}
learning_rate = 0.1
discount_factor = 0.9
epsilon = 1.0
epsilon_decay = 0.99
min_epsilon = 0.05

def get_action(state, training=True):
    binned_state = get_binned_state(state)
    actions = ['left', 'right', 'rotate', 'drop']
    if training and random.random() < epsilon:
        return random.choice(actions)
    else:
        q_values = [q_table.get((binned_state, action), 0) for action in actions]
        max_q = max(q_values) if q_values else 0
        best_actions = [action for action, q in zip(actions, q_values) if q == max_q]
        return random.choice(best_actions)

# --- Trening w symulacji ---
def train_ai(max_games=500):
    global epsilon
    scores = []
    lines_cleared_per_game = []
    actions = ['left', 'right', 'rotate', 'drop']
    game_over_count = 0
    best_lines_cleared = 0
    best_q_table = {}
    for game_num in range(max_games):
        game = TetrisSim()
        game.reset()
        total_reward = 0
        total_lines_cleared = 0
        steps = 0
        early_game_over = False
        while not game.game_over and steps < 2000:
            state = game.get_state()
            binned_state = get_binned_state(state)
            action = get_action(state, training=True)

            if action == 'left' or action == 'right':
                success = game.move(-1 if action == 'left' else 1)
                if success:
                    new_arena = np.array(game.get_state()['arena'])
                    completeness = get_line_completeness(new_arena)
                    surface = get_surface_profile(new_arena)
                    surface_smoothness = -np.std(surface) * 10
                    reward = 40 + completeness * 30 + surface_smoothness
                else:
                    reward = -25
            elif action == 'rotate':
                success = game.rotate()
                if success:
                    new_arena = np.array(game.get_state()['arena'])
                    completeness = get_line_completeness(new_arena)
                    surface = get_surface_profile(new_arena)
                    surface_smoothness = -np.std(surface) * 10
                    reward = 50 + completeness * 40 + surface_smoothness
                else:
                    reward = -25
            elif action == 'drop':
                lines_cleared = game.drop()
                total_lines_cleared += lines_cleared
                new_arena = np.array(game.get_state()['arena'])
                holes = get_holes(new_arena)
                max_height = get_max_height(new_arena)
                completeness = get_line_completeness(new_arena)
                surface = get_surface_profile(new_arena)
                surface_smoothness = -np.std(surface) * 20
                bumpiness = get_bumpiness(new_arena)
                potential_clears = get_potential_clears(new_arena)

                if game.game_over:
                    if steps < 50:
                        reward = -800
                        early_game_over = True
                    else:
                        reward = -400
                elif lines_cleared > 0:
                    if lines_cleared == 4:
                        reward = 4000
                    elif lines_cleared == 3:
                        reward = 3000
                    elif lines_cleared == 2:
                        reward = 2000
                    else:
                        reward = 1000
                    consecutive_bonus = min(1500, 750 * state['consecutive_clears']) if state['consecutive_clears'] > 1 else 0
                    reward += consecutive_bonus + completeness * 200 + steps * 4 + potential_clears * 50
                else:
                    reward = 200 - holes * 300 - max_height * 40 - bumpiness * 15 + completeness * 400 + surface_smoothness + potential_clears * 50

            total_reward += reward
            new_state = game.get_state()
            next_binned_state = get_binned_state(new_state)

            if (binned_state, action) not in q_table:
                q_table[(binned_state, action)] = 0
            max_next_q = max([q_table.get((next_binned_state, next_action), 0) for next_action in actions])
            q_table[(binned_state, action)] += learning_rate * (
                reward + discount_factor * max_next_q - q_table[(binned_state, action)])

            steps += 1

        if early_game_over:
            game_over_count += 1
        scores.append(total_reward)
        lines_cleared_per_game.append(total_lines_cleared)
        if total_lines_cleared > best_lines_cleared:
            best_lines_cleared = total_lines_cleared
            best_q_table = q_table.copy()
            with open('best_q_table.json', 'w') as f:
                json.dump({str(k): v for k, v in best_q_table.items()}, f)
        print(
            f"Gra {game_num + 1}/{max_games}, Wynik: {total_reward:.1f}, Linie: {total_lines_cleared}, Epsilon: {epsilon:.3f}, Q-table size: {len(q_table)}, Early Game Overs: {game_over_count}")
        epsilon = max(min_epsilon, epsilon * epsilon_decay)

    with open('q_table.json', 'w') as f:
        json.dump({str(k): v for k, v in q_table.items()}, f)
    print("Q-tabela zapisana do pliku q_table.json")
    print(f"Najlepsza liczba linii: {best_lines_cleared}, Q-tabela zapisana do best_q_table.json")

    print("Trening zakończony, generuję wykres...")
    plt.plot(range(1, max_games + 1), scores, label='Wynik gry')
    plt.xlabel('Numer gry')
    plt.ylabel('Wynik')
    plt.title('Wyniki AI podczas treningu')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_results.png')
    plt.close()
    print("Wykres zapisany jako training_results.png")

# --- Główny program ---
if __name__ == "__main__":
    train_ai(max_games=500)