import csv
from random import random

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

def get_stats(first_seed, second_seed):
    global matchup_stats
    index = (first_seed - 1) * 16 + (second_seed - 1)
    return matchup_stats[index]

def pick_winner_by_seed(a, b):
    first_seed = a["seed"]
    second_seed = b["seed"]
    stats = get_stats(first_seed, second_seed)
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
    
class Bracket():
    bracket = []
    matchup_stats = []

    def progress_bracket(self, pick_winner):
        last_round_winners = list.copy(self.bracket)
        while len(last_round_winners) > 1:
            i = 0 
            winners = []
            while i < (len(last_round_winners) / 2):
                winners.append(pick_winner(last_round_winners[i], last_round_winners[i+1]))
                i += 2
            for winner in winners:
                self.bracket.append(winner)
            last_round_winners = list.copy(winners)

    def __init__(self, bracket, matchup_stats, pick_winner):
        self.bracket = list.copy(bracket)
        self.first_round_size = len(bracket)
        self.matchup_stats = matchup_stats
        self.progress_bracket(pick_winner)

    def print_bracket(self):
        print(f"{self.bracket[0]["name"]}\t\t")
        print(f"{self.bracket[1]["name"]}\t\t")
        print(f"{self.bracket[2]["name"]}\t\t")
        print(f"{self.bracket[3]["name"]}\t\t")
        print(f"{self.bracket[4]["name"]}\t\t{self.bracket[16]["name"]}\t\t")
        print(f"{self.bracket[5]["name"]}\t\t{self.bracket[17]["name"]}\t\t")
        print(f"{self.bracket[6]["name"]}\t\t{self.bracket[18]["name"]}\t\t{self.bracket[24]["name"]}\t\t")
        print(f"{self.bracket[7]["name"]}\t\t{self.bracket[19]["name"]}\t\t{self.bracket[25]["name"]}\t\t{self.bracket[28]["name"]}\t\t{self.bracket[30]["name"]}\t\t")
        print(f"{self.bracket[8]["name"]}\t\t{self.bracket[20]["name"]}\t\t{self.bracket[26]["name"]}\t\t{self.bracket[29]["name"]}\t\t")
        print(f"{self.bracket[9]["name"]}\t\t{self.bracket[21]["name"]}\t\t{self.bracket[27]["name"]}\t\t")
        print(f"{self.bracket[10]["name"]}\t\t{self.bracket[22]["name"]}\t\t")
        print(f"{self.bracket[11]["name"]}\t\t{self.bracket[23]["name"]}\t\t")
        print(f"{self.bracket[12]["name"]}\t\t")
        print(f"{self.bracket[13]["name"]}\t\t")
        print(f"{self.bracket[14]["name"]}\t\t")
        print(f"{self.bracket[15]["name"]}\t\t")


def load_csv():
    matchup_stats = []
    with open("matchup_stats.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)
        for line in reader:
            matchup_stats.append(line)
    return matchup_stats

def main():
    matchup_stats = load_csv()
    sim_bracket = Bracket(starting_bracket, matchup_stats)
    sim_bracket.print_bracket()


if __name__ == "__main__":
    main()
