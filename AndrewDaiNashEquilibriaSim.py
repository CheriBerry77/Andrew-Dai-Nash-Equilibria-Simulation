"""
Author: Andrew Dai
Date: 01/20/2026

AI Usage:
None
"""

import sys
import random
import matplotlib.pyplot as plt

#for RPS
try:
    import ternary
except ImportError:
    ternary = None


class Player:
    #represents a player in the simulation

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

#plotting

def plot_pair(player1, player2, strategies, title):
    #scatter plot for 2-strategy games
    p1_vals = [p[0] for p in player1.preference_history]
    p2_vals = [p[0] for p in player2.preference_history]

    sizes = [10 + i for i in range(len(p1_vals))]

    plt.figure()
    plt.scatter(
        p1_vals,
        p2_vals,
        s=sizes,
        alpha=0.4
    )
    plt.xlabel(f"{player1.name} prob({strategies[0]})")
    plt.ylabel(f"{player2.name} prob({strategies[0]})")
    plt.title(title)
    plt.grid(True)
    plt.show()


def plot_rps(players):
    #ternary plot for RPS

    scale = 1
    fig, tax = ternary.figure(scale=scale)
    tax.set_title("RPS Mixed Strategy Convergence", fontsize=14)

    for p in players:
        for pref in p.preference_history:
            tax.scatter(
                [(pref[0], pref[1], pref[2])],
                color="blue",
                alpha=0.1,
                marker='o'
            )

    tax.left_axis_label("Paper", fontsize=12)
    tax.right_axis_label("Scissors", fontsize=12)
    tax.bottom_axis_label("Rock", fontsize=12)
    tax.clear_matplotlib_ticks()
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <game_file.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    game = parse_game_file(filename)

    print("\n Game Loaded")
    print(f"Title: {game['title']}")
    print(f"Strategies: {game['strategies']}")

    players = [Player(f"P{i+1}", game["num_choices"]) for i in range(10)]

    sessions = 50
    for _ in range(sessions):
        run_round_robin(players, game)

    print("\n Simulation Complete")

    #pairwise plots
    if game["num_choices"] == 2:
        pairings = [(0,1),(2,3),(4,5),(6,7),(8,9)]
        for i, j in pairings:
            plot_pair(
                players[i],
                players[j],
                game["strategies"],
                game["title"]
            )
    else:
        plot_rps(players)

if __name__ == "__main__":
    main()
