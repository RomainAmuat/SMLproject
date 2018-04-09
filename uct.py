import time
import datetime
from math import sqrt, log
from parameters import Params


class Node:
    UCTK = 0.0001

    def __init__(self, board, ia, move, father, color, interestingness):
        self.board = board
        self.ia = ia

        self.father = father
        self.children = []
        self.color = -color

        self.move = None
        if move is not None:
            self.move = move

        self.val_exploit = interestingness
        self.p = None
        self.proba = None
        self.expansions = 1

        self.compute_ia_proba()
        self.update_proba()

    def add_child(self, move, father, value):
        nc = Node(self.board, self.ia, move, father, self.color, value)
        self.children.append(nc)

    def select_child_expand(self):
        if len(self.children) > 0:
            s = sorted(self.children, key=lambda c:
                       c.proba + c.val_exploit*Node.UCTK*sqrt(2*log(self.expansions)/c.expansions))[-1]
            if s is not None:
                if s.move is not None:
                    pass
            else:
                Params.log("uct.py", "Move is not None")
            return s
        else:
            return None

    def get_best_child_move(self):
        if len(self.children) > 0:
            s = sorted(self.children, key=lambda c:
                                      c.proba + c.val_exploit*Node.UCTK*sqrt(2*log(self.expansions)/c.expansions))[-1]

            return s.move

    def expand_node(self):
        if len(self.children) == 0:
            moves = self.get_moves_list()
            nb = self.board.get_legal_moves_play_list(moves)

            c = self.color
            if self.move is not None:
                c = -self.move[0]

            for m in nb:
                self.add_child((c, m[0], m[1]), self, self.p[self.board.board_size*m[0]+m[1]])

            self.update_proba()
            self.update_expansion(len(nb))

        else:
            self.select_child_expand().expand_node()

    def get_moves_list(self):
        if self.father is not None:
            return [self.move] + self.father.get_moves_list()
        else:
            return []

    def compute_ia_proba(self):
        moves = self.get_moves_list()
        # We multiply by -self.move[0][0] to get the "canonical board"
        c = self.color
        if self.move is not None:
            c = -self.move[0]
        self.p, self.proba = self.ia.get_proba(c*self.board.get_matrix_play_list(moves))

    def update_proba(self):
        if len(self.children) == 0:
            self.compute_ia_proba()
        else:
            for c in self.children:
                self.min_max(c.proba)

    def min_max(self, proba):
        if self.move is None:
            pass
        elif self.move[0] == self.color:
            if proba > self.proba:
                self.proba = proba
                if self.father is not None:
                    self.father.update_proba()
        else:
            if proba < self.proba:
                self.proba = proba
                if self.father is not None:
                    self.father.update_proba()

    def update_expansion(self, nb):
        self.expansions += nb
        if self.father is not None:
            self.father.update_expansion(nb)


class UCT:
    def __init__(self, ia, *args, **kwargs):
        self.ia = ia

        seconds = kwargs.get('time', 1.0)
        self.calculation_time = seconds

    def next_turn(self, board, color):
        root = Node(board, self.ia, None, None, -color, 0)
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            root.expand_node()
        return root.get_best_child_move()

