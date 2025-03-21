#!/usr/bin/env python3
import csv
from random import random
from tourneyket import Bracket

BOLD = '\033[1m'
END = '\033[0m'
PURPLE = '\033[95m'

brackets_2025 =     [["South Region",
                        [{"name": "Auburn", "seed": 1},
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
                        {"name": "Bryant", "seed": 15}]],
                    ["East Region",
                        [{"name": "Duke", "seed": 1},
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
                        {"name": "Robert Morris", "seed": 15}]],
                    ["West Region",
                        [{"name": "Florida", "seed": 1},
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
                        {"name": "Omaha", "seed": 15}]],
                    ["Midwest Region",
                        [{"name": "Houston", "seed": 1},
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
                        {"name": "Wofford", "seed": 15}]]]

class Matchup():
    def __init__(self, team_seed, opp_seed):
        self.team_seed = team_seed
        self.opp_seed = opp_seed
        self.games = 0
        self.team_wins = 0
        self.opp_wins = 0

    def add_win(self):
        self.games += 1
        self.team_wins += 1 

    def add_loss(self):
        self.games += 1 
        self.opp_wins += 1

    def get_list(self):
        try:
            self.pct = round(self.team_wins/self.games, 3)
        except ZeroDivisionError:
            self.pct = "NaN"
        listform = [self.team_seed, self.opp_seed, self.games, self.team_wins, self.opp_wins, self.pct]
        return listform


def populate_stats(matchups):
    with open("data/combined.csv", "r", newline="") as fp:
        reader = csv.reader(fp)
        next(reader)
        for y, r, wtn, wts, wtsc, ltn, lts, ltsc in reader:
            # Populate win 
            matchups[int(wts)-1][int(lts)-1].add_win()
            # Populate loss 
            matchups[int(lts)-1][int(wts)-1].add_loss()

def generate_matchup_stats():
    seeds = [x for x in range(1, 17)]
    matchups = []

    for xseed in seeds:
        inner_matchups = []
        for yseed in seeds:
            inner_matchups.append(Matchup(xseed, yseed))
        matchups.append(inner_matchups)
    
    populate_stats(matchups)

    with open("data/matchup_stats.csv", "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["team_seed", "opp_seed", "games", "wins", "losses", "pct"])
        for xseed in matchups:
            for yseed in xseed:
                writer.writerow(yseed.get_list())

def load_csv():
    matchup_stats = []
    with open("data/matchup_stats.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)
        for line in reader:
            matchup_stats.append(line)
    return matchup_stats

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
    

if __name__ == "__main__":
    try:
        print("Using found matchup_stats.csv")
        matchup_stats = load_csv()
    except FileNotFoundError:
        print("Generating matchup_stats.csv...")
        generate_matchup_stats()
        matchup_stats = load_csv()

    for region_name, region_bracket in brackets_2025:
        bracket_object = Bracket(region_bracket)
        bracket_object.play_out_bracket(pick_winner_by_seed)
        print(BOLD + PURPLE + f"\n{region_name}:\n" + END)
        bracket_object.print_bracket(formatting=lambda t: f" {t["seed"]} {t["name"]}")
