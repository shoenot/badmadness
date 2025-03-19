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

def get_stats(first_seed, second_seed, matchup_stats):
    index = (first_seed - 1) * 16 + (second_seed - 1)
    return matchup_stats[index]
        
def flip_coin(first_seed, second_seed, matchup_stats):
    stats = get_stats(first_seed, second_seed, matchup_stats)
    decrementer = 1
    while stats[5] == "NaN":
        stats = get_stats(first_seed, second_seed - decrementer, matchup_stats)
        decrementer += 1
    pct = float(stats[5])
    if pct >= 0.985:
        pct = 0.985
    elif pct <= 0.015:
        pct = 0.015
    return 1 if random() < pct else 0

def progress_bracket(bracket, matchup_stats):
    i = 0
    return_bracket = list.copy(bracket)
    while i < (len(bracket) / 2):
        first_seed = return_bracket[i]["seed"]
        second_seed = return_bracket[i+1]["seed"]
        return_bracket.pop(flip_coin(first_seed, second_seed, matchup_stats) + i)
        i += 1
    return return_bracket

def play_out_bracket(bracket, matchup_stats):
    first_round = bracket
    second_round = progress_bracket(first_round, matchup_stats)
    third_round = progress_bracket(second_round, matchup_stats)
    fourth_round = progress_bracket(third_round, matchup_stats)
    winner = progress_bracket(fourth_round, matchup_stats)
    print("{}	    {}	    {}	    {}	    {}".format(first_round[0]["name"], second_round[0]["name"], third_round[0]["name"], fourth_round[0]["name"], winner[0]["name"]))
    print("{}	    {}	    {}	    {}".format(first_round[1]["name"], second_round[1]["name"], third_round[1]["name"], fourth_round[1]["name"]))
    print("{}	    {}	    {}".format(first_round[2]["name"], second_round[2]["name"], third_round[2]["name"]))
    print("{}	    {}	    {}".format(first_round[3]["name"], second_round[3]["name"], third_round[3]["name"]))
    print("{}	    {}".format(first_round[4]["name"], second_round[4]["name"]))
    print("{}	    {}".format(first_round[5]["name"], second_round[5]["name"]))
    print("{}	    {}".format(first_round[6]["name"], second_round[6]["name"]))
    print("{}	    {}".format(first_round[7]["name"], second_round[7]["name"]))
    for i in range (8, 16):
        print(first_round[i]["name"])

        
def main():
    matchup_stats = load_csv()
    play_out_bracket(starting_bracket, matchup_stats)

if __name__ == "__main__":
    main()
