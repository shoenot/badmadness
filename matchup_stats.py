import csv 

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
    with open("combined.csv", "r", newline="") as fp:
        reader = csv.reader(fp)
        next(reader)
        for y, r, wtn, wts, wtsc, ltn, lts, ltsc in reader:
            # Populate win 
            matchups[int(wts)-1][int(lts)-1].add_win()
            # Populate loss 
            matchups[int(lts)-1][int(wts)-1].add_loss()

def main():
    seeds = [x for x in range(1, 17)]
    matchups = []

    for xseed in seeds:
        inner_matchups = []
        for yseed in seeds:
            inner_matchups.append(Matchup(xseed, yseed))
        matchups.append(inner_matchups)
    
    populate_stats(matchups)

    with open("matchup_stats.csv", "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["team_seed", "opp_seed", "games", "wins", "losses", "pct"])
        for xseed in matchups:
            for yseed in xseed:
                writer.writerow(yseed.get_list())


if __name__ == "__main__":
    main()
