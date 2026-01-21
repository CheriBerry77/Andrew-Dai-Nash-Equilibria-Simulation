"""
Author: Andrew Dai

AI Usage:
None
"""

import sys
import random
import matplotlib.pyplot as plt
import ternary

class Player:
    def __init__(self, name, num_choices):
        self.name = name
        self.num_choices = num_choices
        self.preferences = [1 / num_choices] * num_choices
        self.total_score = 0.0
        self.num_games = 0
        self.preference_history = []

    def choose_strategy(self):
        return random.choices(
            range(self.num_choices),
            weights=self.preferences,
            k=1
        )[0]

    def update_preferences(self, strategy_index, payoff):
        avg_score = (
            self.total_score / self.num_games
            if self.num_games > 0 else 0
        )

        delta = (payoff - avg_score) / 100
        self.preferences[strategy_index] += delta

        self.preferences[strategy_index] = max(
            0.0, min(1.0, self.preferences[strategy_index])
        )

        total = sum(self.preferences)
        if total == 0:
            self.preferences = [1 / self.num_choices] * self.num_choices
        else:
            self.preferences = [p / total for p in self.preferences]

        self.preference_history.append(self.preferences.copy())
        self.total_score += payoff
        self.num_games += 1

def parse_game_file(filename):
    lines = []
    with open(filename, "r") as file:
        for line in file:
            li = line.strip()
            if li and not li.startswith("#"):
                lines.append(li)

    num_choices = int(lines[0])
    title = lines[1]
    strategies = []
    payoff_matrix = []

    for line in lines[2:]:
        tokens = line.split()
        strategies.append(tokens[0])
        payoff_matrix.append(list(map(int, tokens[1:])))

    return {
        "num_choices": num_choices,
        "title": title,
        "strategies": strategies,
        "payoff_matrix": payoff_matrix,
    }

def play_game(player1, player2, game):
    s1 = player1.choose_strategy()
    s2 = player2.choose_strategy()

    row = game["payoff_matrix"][s1]
    payoff1 = row[2 * s2]
    payoff2 = row[2 * s2 + 1]

    player1.update_preferences(s1, payoff1)
    player2.update_preferences(s2, payoff2)

def run_round_robin(players, game):
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            play_game(players[i], players[j], game)

def plot_simplex_pair(player1, player2, strategies, title, fig_num):
    p1_x = [p[0] for p in player1.preference_history]
    p1_y = [1 - x for x in p1_x]
    p2_x = [p[0] for p in player2.preference_history]
    p2_y = [1 - x for x in p2_x]

    sizes = [30 + i for i in range(len(p1_x))]
    plt.figure(fig_num, figsize=(6, 6))
    plt.scatter(p1_x, p1_y, s=sizes, alpha=0.5, label="P1", color="blue")
    plt.scatter(p2_x, p2_y, s=sizes, alpha=0.5, label="P2", color="orange")
    plt.plot([0, 1], [1, 0], linestyle="--", color="gray")
    plt.xlabel(strategies[0])
    plt.ylabel(strategies[1])
    plt.title(title)
    plt.axis("equal")
    plt.grid(True)
    plt.legend()

def plot_rps_ternary(player1, player2, strategies, title):
    fig, tax = ternary.figure(scale=1.0)
    fig.set_size_inches(6, 6)
    p1_points = [tuple(p) for p in player1.preference_history]
    p2_points = [tuple(p) for p in player2.preference_history]
    sizes = [20 + i for i in range(len(p1_points))]
    tax.scatter(p1_points, color="blue", label="P1", s=sizes, alpha=0.6)
    tax.scatter(p2_points, color="orange", label="P2", s=sizes, alpha=0.6)
    tax.boundary()
    tax.gridlines(multiple=0.1, linewidth=0.5)
    tax.bottom_axis_label(strategies[0])
    tax.left_axis_label(strategies[1])
    tax.right_axis_label(strategies[2])
    tax.set_title(title)
    tax.legend()
    tax.clear_matplotlib_ticks()

def main():
    if len(sys.argv) < 2:
        print("Usage: python AndrewDaiNashEquilibriaSim.py <game_file.txt>")
        sys.exit(1)

    game = parse_game_file(sys.argv[1])
    players = [Player(f"P{i+1}", game["num_choices"]) for i in range(10)]

    for _ in range(50):
        run_round_robin(players, game)

    #create 5 plots
    for i in range(5):
        if game["num_choices"] == 2:
            plot_simplex_pair(
                players[i],
                players[i + 1],
                game["strategies"],
                f"{game['title']} (P{i+1} vs P{i+2})",
                fig_num=i + 1
            )
        else:
            plot_rps_ternary(
                players[i],
                players[i + 1],
                game["strategies"],
                f"{game['title']} (P{i+1} vs P{i+2})"
            )
    plt.show()

if __name__ == "__main__":
    main()
