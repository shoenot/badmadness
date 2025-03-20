import csv
from random import random
from math import floor

starting_bracket = [{"name": "one", "seed": 1},
                    {"name": "sixteen", "seed": 16},
                    {"name": "eight", "seed": 8},
                    {"name": "nine", "seed": 9},
                    {"name": "five", "seed": 5},
                    {"name": "twelve", "seed": 12},
                    {"name": "four", "seed": 4},
                    {"name": "thirteen", "seed": 13},
                    {"name": "six", "seed": 6},
                    {"name": "eleven", "seed": 11},
                    {"name": "three", "seed": 3},
                    {"name": "fourteen", "seed": 14},
                    {"name": "seven", "seed": 7},
                    {"name": "ten", "seed": 10},
                    {"name": "two", "seed": 2},
                    {"name": "fifteen", "seed": 15}]

class Bracket():
    bracket = []
    matchup_stats = []

    def progress_bracket(self, pick_winner):
        last_round_winners = list.copy(self.bracket[-1])
        while len(last_round_winners) > 1:
            i = 0 
            winners = []
            while i < (len(last_round_winners)):
                winners.append(pick_winner(last_round_winners[i], last_round_winners[i+1]))
                i += 2
            self.bracket.append(winners)
            last_round_winners = list.copy(winners)

    def __init__(self, initial_bracket, pick_winner):
        self.bracket.append(initial_bracket)
        self.first_round_size = len(initial_bracket)
        self.progress_bracket(pick_winner)

    def pivot(self, bracket, output_list, level):
        midpoint_idx = floor(len(output_list)/2)
        output_list[midpoint_idx] = "{}{}".format(" " * 10 * level, bracket[level].pop(0)["name"])
        if level > 0:
            output_list[:midpoint_idx] = self.pivot(bracket, [None] * len(output_list[:midpoint_idx]), level - 1)
            output_list[midpoint_idx+1:] = self.pivot(bracket, [None] * len(output_list[:midpoint_idx]), level -1)
        return output_list

    def print_bracket(self):
        output_list = [None] * (self.first_round_size * 2 - 1)
        bracket_to_pop = list.copy(self.bracket)
        level = len(self.bracket) - 1
        output_list = self.pivot(bracket_to_pop, output_list, level)
        for item in output_list:
            print(item)


def load_csv():
    matchup_stats = []
    with open("matchup_stats.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)
        for line in reader:
            matchup_stats.append(line)
    return matchup_stats

matchup_stats = load_csv()

def get_stats(first_seed, second_seed):
    global matchup_stats
    index = (first_seed - 1) * 16 + (second_seed - 1)
    return matchup_stats[index]

def pick_winner_by_seed(a, b):
    first_seed = a["seed"]
    second_seed = b["seed"]
    stats = get_stats(first_seed, second_seed)
    # stats[5] is the win pct for the seed matchup 
    # some matchups have never happened in the NCAAT yet
    # so it just looks at the numbers for a matchup vs a higher oppponent seed 
    decrementer = 1
    while stats[5] == "NaN":
        stats = get_stats(first_seed, second_seed - decrementer)
        decrementer += 1
    pct = float(stats[5])
    if pct >= 0.985:
        pct = 0.985
    elif pct <= 0.015:
        pct = 0.015
    return a if random() < pct else b
    
def main():
    sim_bracket = Bracket(starting_bracket, pick_winner_by_seed)
    sim_bracket.print_bracket()


if __name__ == "__main__":
    main()
