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



def load_csv():
    matchup_stats = []
    with open("matchup_stats.csv", "r") as fp:
        reader = csv.reader(fp)
        next(reader)
        for line in reader:
            matchup_stats.append(line)
    return matchup_stats
        
def flip_coin(first_seed, second_seed, matchup_stats):
    index = 1 + (first_seed - 1) * 16 + second_seed
    stats = matchup_stats[index]
    if stats[5] == "NaN":
        pct = 0.5
    else:
        pct = float(stats[5])
        if pct > 0.98:
            pct = 0.98
        elif pct < 0.02:
            pct = 0.02
    return 1 if random() < pct else 0

def progress_bracket(bracket, matchup_stats):
    i = 0
    return_bracket = list.copy(bracket)
    while len(return_bracket) != (len(bracket) / 2):
        first_seed = bracket[i]["seed"]
        second_seed = bracket[i+1]["seed"]
        return_bracket.pop(flip_coin(first_seed, second_seed, matchup_stats) + i)
        i += 1
    return return_bracket
        
def main():
    matchup_stats = load_csv()
    print("Progressing Bracket...\n")
    for line in progress_bracket(starting_bracket, matchup_stats):
        print(line)

if __name__ == "__main__":
    main()
