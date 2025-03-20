#!/usr/bin/env python3
import csv
from random import random
from math import floor

south_region =      [{"name": "Auburn", "seed": 1},
                    {"name": "Alabama St.", "seed": 16},
                    {"name": "Louisville", "seed": 8},
                    {"name": "Creighton", "seed": 9},
                    {"name": "Michigan", "seed": 5},
                    {"name": "UC San Diego", "seed": 12},
                    {"name": "Texas A&M", "seed": 4},
                    {"name": "Yale", "seed": 13},
                    {"name": "Ole Miss", "seed": 6},
                    {"name": "North Carolina", "seed": 11},
                    {"name": "Iowa St.", "seed": 3},
                    {"name": "Lipscomb", "seed": 14},
                    {"name": "Marquette", "seed": 7},
                    {"name": "New Mexico", "seed": 10},
                    {"name": "Michigan St.", "seed": 2},
                    {"name": "Bryant", "seed": 15}]

east_region =       [{"name": "Duke", "seed": 1},
                    {"name": "Mount St. Mary's", "seed": 16},
                    {"name": "Mississippi St.", "seed": 8},
                    {"name": "Baylor", "seed": 9},
                    {"name": "Oregon", "seed": 5},
                    {"name": "Liberty", "seed": 12},
                    {"name": "Arizona", "seed": 4},
                    {"name": "Akron", "seed": 13},
                    {"name": "BYU", "seed": 6},
                    {"name": "VCU", "seed": 11},
                    {"name": "Wisconsin", "seed": 3},
                    {"name": "Montana", "seed": 14},
                    {"name": "St. Mary's", "seed": 7},
                    {"name": "Vanderbilt", "seed": 10},
                    {"name": "Alabama", "seed": 2},
                    {"name": "Robert Morris", "seed": 15}]

west_region =       [{"name": "Florida", "seed": 1},
                    {"name": "Norfolk St.", "seed": 16},
                    {"name": "UConn", "seed": 8},
                    {"name": "Oklahoma", "seed": 9},
                    {"name": "Memphis", "seed": 5},
                    {"name": "Colorado St.", "seed": 12},
                    {"name": "Maryland", "seed": 4},
                    {"name": "Grand Canyon", "seed": 13},
                    {"name": "Missouri", "seed": 6},
                    {"name": "Drake", "seed": 11},
                    {"name": "Texas Tech", "seed": 3},
                    {"name": "UNC Wilmington", "seed": 14},
                    {"name": "Kansas", "seed": 7},
                    {"name": "Arkansas", "seed": 10},
                    {"name": "St John's", "seed": 2},
                    {"name": "Omaha", "seed": 15}]

midwest_region =    [{"name": "Houston", "seed": 1},
                    {"name": "SIU Edwardsville", "seed": 16},
                    {"name": "Gonzaga", "seed": 8},
                    {"name": "Georgia", "seed": 9},
                    {"name": "Clemson", "seed": 5},
                    {"name": "McNeese", "seed": 12},
                    {"name": "Purdue", "seed": 4},
                    {"name": "High Point", "seed": 13},
                    {"name": "Illinois", "seed": 6},
                    {"name": "Xavier", "seed": 11},
                    {"name": "Kentucky", "seed": 3},
                    {"name": "Troy", "seed": 14},
                    {"name": "UCLA", "seed": 7},
                    {"name": "Utah St.", "seed": 10},
                    {"name": "Tennessee", "seed": 2},
                    {"name": "Wofford", "seed": 15}]

class Bracket():
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
        self.bracket = []
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
    south_bracket = Bracket(south_region, pick_winner_by_seed)
    print("South Region: \n")
    south_bracket.print_bracket()

    east_bracket = Bracket(east_region, pick_winner_by_seed)
    print("East Region: \n")
    east_bracket.print_bracket()

    west_bracket = Bracket(west_region, pick_winner_by_seed)
    print("West Region: \n")
    west_bracket.print_bracket()

    midwest_bracket = Bracket(midwest_region, pick_winner_by_seed)
    print("Midwest Region: \n")
    midwest_bracket.print_bracket()


if __name__ == "__main__":
    main()
