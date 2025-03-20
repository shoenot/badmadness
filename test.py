from tourneyket import Bracket

starting_bracket = [x for x in range(1,17)]

def pick_higher(a, b):
    return sorted([a, b], key=lambda d: int(d))[0]

MyBracket = Bracket(starting_bracket, pick_winner = pick_higher, spaces=10)
MyBracket.print_bracket()
