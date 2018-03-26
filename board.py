import copy
import numpy as np



class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.matrix = np.zeros((board_size, board_size), dtype=int)
        self.win = 0

    def get_clone(self):
        return copy.deepcopy(self)

    def next_legal_moves(self):
        pass

    def play_move(self, move):
        pass

    def play_list(self, move_list):
        pass

    def winner(self):
        return self.win

    def get_repr_matrix(self):
        return self.matrix

    def get_legal_moves_play_list(self, move_list):
        matrix_save = np.copy(self.matrix)

        if move_list is not None:
            for m in move_list:
                self.play_move(m)

        r = self.next_legal_moves()
        self.matrix = matrix_save
        return r

    def get_matrix_play_list(self, move_list):
        matrix_save = np.copy(self.matrix)

        if move_list is not None:
            for m in move_list:
                self.play_move(m)

        r = self.get_repr_matrix().copy()
        self.matrix = matrix_save
        return r
