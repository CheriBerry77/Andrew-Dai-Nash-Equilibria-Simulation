"""
Author: Andrew Dai

AI Usage:
None
"""

import sys

def parse_game_file(filename):
    lines = []
    with open(filename, "r") as file:
        for line in file:
            li = line.strip()
            if li != "" and not li.startswith("#"):
                lines.append(li)

    num_choices = int(lines[0])
    title = lines[1]
    strategies = []
    payoff_matrix = []

    for line in lines[2:]:
        tokens = line.split()
        strategy_name = tokens[0]
        payoffs = list(map(int, tokens[1:]))

        if len(payoffs) != num_choices * 2:
            raise ValueError("Incorrect number of payoffs in row")

        strategies.append(strategy_name)
        payoff_matrix.append(payoffs)

    return {
        "num_choices": num_choices,
        "title": title,
        "strategies": strategies,
        "payoff_matrix": payoff_matrix,
    }

def log_game_data(game):
    print("\nGame Parsed")
    print(f"Title: {game['title']}")
    print(f"Number of strategies per player: {game['num_choices']}")
    print("\nStrategies:")
    for s in game["strategies"]:
        print(f"  - {s}")

    print("\nPayoff Matrix:")
    for i, row in enumerate(game["payoff_matrix"]):
        print(f"{game['strategies'][i]}: {row}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <game_file.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    game = parse_game_file(filename)
    log_game_data(game)

if __name__ == "__main__":
    main()
