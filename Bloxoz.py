from level import Level
import numpy as np
import copy

class GamePlay:
    left ="LEFT"
    right = 'RIGHT'
    up    = 'UP'
    down  = 'DOWN'
    switch = 'SWITCH'

    @staticmethod
    def opposite_action(action:str, check):
        if action == GamePlay.DOWN:
            return check == GamePlay.UP
        if action == GamePlay.UP:
            return check == GamePlay.DOWN
        if action == GamePlay.LEFT:
            return check == GamePlay.RIGHT
        if action == GamePlay.RIGHT:
            return check == GamePlay.LEFT
        if action == GamePlay.SWITCH:
            return check == GamePlay.SWITCH
        return False

    @staticmethod
    def take_action_set():
        return [GamePlay.UP,GamePlay.DOWN,GamePlay.LEFT,GamePlay.RIGHT,GamePlay.SWITCH]
    
    @staticmethod
    def decode_action(action_check):
        for action in GamePlay.take_action_set():
            if action[0] == action_check:
                return action

class State:
    def __init__(self, cur:list, goal: list, board_state: dict):
        self.cur = copy.copy(cur)
        self.goal = copy.copy(goal)
        self.board_state = copy.copy(board_state)

    def is_standing_state(self):
        return len(self.cur) == 2

    def is_plited_state(self):
        # if splited, 2-first number in self.cur is the position of the current controlled block
        return len(self.cur) == 4 \
            and Blozorx.manhattan_distance(self.cur[:2], self.cur[2:]) != 1
        
    def is_lying_state(self):
        return not self.is_standing_state() and not self.is_plited_state()

    def is_goal_state(self):
        return self.is_standing_state() \
            and self.cur == self.goal

    def is_cell_available(self,x,y):
        return (0 <= x < self.board_state.shape[0])\
            and (0 <= y < self.board_state.shape[1])\
            and self.board_state[x,y]

    def __eq__(self, other):
        return np.array_equal(self.board_state,other.board_state) \
            and self.cur == other.cur
