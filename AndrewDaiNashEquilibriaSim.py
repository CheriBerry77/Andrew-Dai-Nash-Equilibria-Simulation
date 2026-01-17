"""
Author: Andrew Dai

AI Usage:
None
"""

import sys
import random

class Player:
    """
    Represents a player in the simulation
    """
    def __init__(self, name, num_choices):
        """
        Initializes a player

        Arguments:
        name (str): player identifier
        num_choices (int): number of strategies
        """
        self.name = name
        self.num_choices = num_choices
        self.preferences = [1 / num_choices] * num_choices
        self.total_score = 0.0
        self.num_games = 0
        self.preference_history = []

    def choose_strategy(self):
        """
        Chooses a strategy index

        Returns:
        int: chosen strategy index
        """
        return random.choices(
            range(self.num_choices),
            weights=self.preferences,
            k=1
        )[0]

    def update_preferences(self, strategy_index, payoff):
        """
        Updates strategy preferences after a game

        Arguments:
        strategy_index (int): strategy used
        payoff (float): payoff received
        """
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
    """
    Parses a game definition file

    Arguments:
    filename (str): path to the game file

    Returns:
    dict: parsed game data
    """
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
    """
    Plays a single game between two players

    Argument:
    player1 (Player)
    player2 (Player)
    game (dict)
    """
    s1 = player1.choose_strategy()
    s2 = player2.choose_strategy()

    idx = s1 * game["num_choices"] * 2 + s2 * 2
    row = game["payoff_matrix"][s1]

    payoff1 = row[2 * s2]
    payoff2 = row[2 * s2 + 1]

    player1.update_preferences(s1, payoff1)
    player2.update_preferences(s2, payoff2)

def run_round_robin(players, game):
    """
    Runs a complete round robin tournament

    Args:
    players (list[Player])
    game (dict)
    """
    num_players = len(players)
    for i in range(num_players):
        for j in range(i + 1, num_players):
            play_game(players[i], players[j], game)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <game_file.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    game = parse_game_file(filename)

    print("\n Game Loaded")
    print(f"Title: {game['title']}")
    print(f"Strategies: {game['strategies']}")
    print("Beginning simulation...\n")

    players = [Player(f"P{i+1}", game["num_choices"]) for i in range(10)]
    sessions = 50
    for session in range(sessions):
        run_round_robin(players, game)

    print("Simulation Complete\n")
    for p in players:
        print(
            f"{p.name}: preferences={p.preferences}, "
            f"avg_score={p.total_score / p.num_games:.2f}"
        )

if __name__ == "__main__":
    main()
