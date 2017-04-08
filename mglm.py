# -*- coding: utf-8 -*-

# Matchbox Learning Machines
# Python 3

from functools import reduce
from itertools import combinations, permutations
from random import uniform

# choose a random key from a dictionary
# of key: weight items

def weighted_choice(choices):
    total = sum(choices.values())
    if total == 0:
        return None
    r = uniform(0, total)
    upto = 0
    for choice, weight in choices.items():
      if upto + weight >= r:
         return choice
      upto += weight
    assert False, "Shouldn't get here"

_,X,O = 0,1,2  # don't change willy nilly

class Position():
    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6))             # diagonals
            
    # the symmetries of a square
    # this group is known as D4

    # the dihedral group D4 of the 3x3 square
    # http://mathworld.wolfram.com/DihedralGroupD4.html
    
    symmetries = [
     [0,1,2,3,4,5,6,7,8],    # identity (no-op)
     [2,5,8,1,4,7,0,3,6],    # rotate right
     [6,3,0,7,4,1,8,5,2],    # rotate left
     [8,7,6,5,4,3,2,1,0],    # rotate 180°
     [2,1,0,5,4,3,8,7,6],    # flip across middle column
     [6,7,8,3,4,5,0,1,2],    # flip across middle row
     [0,3,6,1,4,7,2,5,8],    # flip across main diagonal
     [8,5,2,7,4,1,6,3,0]]    # flip acroos antidiagonal

    def __init__(self, pos=None):
        self.pos = pos or [_]*9

    def __getitem__(self, i):
        return self.pos[i]

    def __setitem__(self, i, mark):
        self.pos[i] = mark
        
    def __str__(self):
        mark_at = lambda i: [' ', 'X' , 'O'][self[i]] 

        ttt_str  = ' %s | %s | %s \n' % (mark_at(0), mark_at(1), mark_at(2))
        ttt_str += '---+---+---\n'
        ttt_str += ' %s | %s | %s \n' % (mark_at(3), mark_at(4), mark_at(5))
        ttt_str += '---+---+---\n'
        ttt_str += ' %s | %s | %s \n' % (mark_at(6), mark_at(7), mark_at(8))
        ttt_str += ''
        return ttt_str
        
    def apply(self, sym):
        return [self.pos[i] for i in sym]
        
    def __hash__(self):
        def num(pos):
            return reduce(lambda x,y: 3*x+y, pos, 0)
        return min( [num(self.apply(sym)) for sym in Position.symmetries] )

    def __eq__(self, other):
        def eq_by(sym):
            return [self.pos[i] for i in sym] == other.pos
        return any(eq_by(sym) for sym in Position.symmetries)
        
    def __ne__(self, other):
        return not self == other
    
    def is_X_win(self):
        return any(all(self.pos[i] == X for i in win) for win in Position.wins)
    
    def is_O_win(self):
        return any(all(self.pos[i] == O for i in win) for win in Position.wins)
        
    def is_leaf(self):
        def three_in_a_row(tri):
            return all(t == X for t in tri) or all(t == O for t in tri)
        def is_win(pos):        
            return any(three_in_a_row([pos[x] for x in win]) for win in Position.wins)
        def is_full(pos):
            return not any(square == _ for square in pos)

        return is_win(self.pos) or is_full(self.pos)

        
#  Matchbox Learning Machine
#  reset
#  new game
#  move
        print(s)
#  youwin
#  youlose

# gamegraph has dict semantics
#  gg[pos] = list of positions 

class Machine():

    class Box():
        def __init__(self, states, bead_count):
            self.beads = {state: bead_count for state in states}

        def choose(self):
            bead = weighted_choice(self.beads)
            if bead is not None:
                self.beads[bead] -= 1
            return bead

        def reward(self, state, amount):
            self.beads[state] += amount

        def __str__(self):
            return str(self.beads)

    def __init__(self, gamegraph, bead_count = 10):
        self.gamegraph = gamegraph
        self.bead_count = bead_count
        self.boxes = dict()
        self.moves = list()
        self.newgame()
    
    def newgame(self):
        self.moves.clear()

    def move(self, state):
        if state not in self.boxes:
            self.boxes[state] = Machine.Box(self.gamegraph[state], self.bead_count)

        move = self.boxes[state].choose()
        if move is not None:
            self.moves.append((state, move))
        return move

    def update(self, amount):
        for (a,b) in self.moves:
            self.boxes[a].beads[b] += amount
        self.newgame()

    def reward(self):
        # go through moves list and reward these moves
        self.update(12)
    
    # def punish(self):
    #     self.update(-1)

    def __str__(self):
        return str([str(state) + ": " + str(box) for (state,box) in self.boxes.items()])


# def count_distinct_complete():
#     def is_even(n):amount
#         return n % 2 == 0
        
#     def f(pos, distinct_positions, nMarks):
#         exists = any(ttt_eq(pos,existing) for existing in distinct_positions[nMarks])
#         if exists: 
#             return
        
#         distinct_positions[nMarks].append(pos)
#         if is_leaf(pos):
#             if is_X_win(pos):
#                 X_wins[namountMarks] += 1
#             elif is_O_win(pos):amount
#                 O_wins[nMarks] += 1
#             else:
#                 Cat_wins[nMarks] += 1
#             return
        
#         mark = X if is_even(nMarks) else O
#         for i in range(9):
#             if pos[i] == _:
#                 new_pos = list(pos)

#                 new_pos[i] = mark
#                 f(new_pos, distinct_positions, nMarks+1)
            
#     distinct_positions = [[] for i in range(10)]
#     X_wins, O_wins, Cat_wins = [0]*10, [0]*10, [0]*10
    
#     pos = [_ for i in range(9)]
#     nMarks = 0
    
#     f(pos, distinct_positions, nMarks)
    
#     total = 0
#     print " m  #pos    X   O  Cat"
#     print "----------------------"
#     for i in range(10):print(nim5[4])
#         n = len(distinct_positions[i])
#         total += n
#         print '{:2d}: {:4d}  {:3d} {:3d} {:3d}'.format(i, n, X_wins[i], O_wins[i], Cat_wins[i])
#         #if n < 20:
#         #    for p in distinct_positions[i]:
#         #        draw_ttt(p)w w in choices.items()
#     print "======================"
#     print "     {:3d}".format(total)

class Nim5():
    def __init__(self):
        pass

    def __getitem__(self, state):
        if state is None:
            return 5
        elif state > 1:
            return [state-1, state-2]
        elif state == 1:
            return [0]
        else:
            assert state == 0
            return []

nim5 = Nim5()
players = [Machine(nim5), Machine(nim5)]

def playone():
    players[0].newgame()
    players[1].newgame()
    
    s = nim5[None]
    turn = 0
    while s is not None:
        s = players[turn].move(s)
        turn = 1 - turn
    # whoever's turn it is is the loser
    # players[turn].punish()
    players[1-turn].reward()

for _ in range(10000):
    playone()

print(players[0])
print(players[1])
