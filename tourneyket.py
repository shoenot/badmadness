from math import floor
from random import choice


def equal_chance(a, b):
    return choice([a, b]) 

class BracketError(Exception):
    pass


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

    def __init__(self, initial_bracket, pick_winner = equal_chance, spaces = 20):
        if not ((len(initial_bracket) & (len(initial_bracket)-1) == 0) and len(initial_bracket) != 0):
            raise BracketError("Starting bracket size is not a power of 2")
        self.bracket = []
        self.bracket.append(initial_bracket)
        self.first_round_size = len(initial_bracket)
        self.spaces = spaces
        self.progress_bracket(pick_winner)

    def get_spacing(self, level):
        if level == 0:
            return ""
        else:
            return (" " * self.spaces * (level - 1) + "|" + "-" * (self.spaces * 1 - 1))

    def pivot(self, bracket, output_list, level):
        midpoint_idx = floor(len(output_list)/2)
        team = self.key(bracket[level].pop(0))
        output_list[midpoint_idx] = "{}{}".format(self.get_spacing(level), team)
        if level > 0:
            output_list[:midpoint_idx] = self.pivot(bracket, [None] * len(output_list[:midpoint_idx]), level - 1)
            output_list[midpoint_idx+1:] = self.pivot(bracket, [None] * len(output_list[:midpoint_idx]), level -1)
        return output_list

    def print_bracket(self, key=lambda t: t):
        self.key = key
        output_list = [None] * (self.first_round_size * 2 - 1)
        bracket_to_pop = list.copy(self.bracket)
        level = len(self.bracket) - 1
        output_list = self.pivot(bracket_to_pop, output_list, level)
        for item in output_list:
            print(item)
