import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
from math import sqrt
from collections import deque,defaultdict

import numpy as num
#in This A* Search, we use h(x) is Manhattan distance

from Bloxoz import State, Blozorx

class Node:
    def __init__(self,path:str,state:State , f = 0 , g = 0, h = 0):
        self.path = path
        self.state = state
        self.f = f
        self.g = g
        self.h = h

    def __lt__(self, other):
        return self.f < other.f
        

def heuristic(current_state, goal_state):
    return abs(current_state[0] - goal_state[0]) + abs(current_state[1] - goal_state[1])

def a_search(game:Blozorx, state:State = None, sender: Connection = None):
    ready = time.time()
    nums_of_node = 0
    def getback(nums_of_node,path=None,is_done=False):
        nonlocal sender,ready
        if sender is not None:
            return_dict = {
                'solution_cost': nums_of_node,
                'path': path,
                'time': time.time() - ready,
                'msg': f'Node has been through: {nums_of_node}',
                'is_done': is_done
            }
            try:
                sender.send(return_dict)
            except:
                pass 
        else:
            return nums_of_node,path,time.time() - ready
    
    if state is None:
        state = game.init_state

    if state.goaling():
        return getback(0, '', True)
    
    open_list = []
    closed_list = []

    has_visited = defaultdict(list)
    def is_visited(state: State):
        nonlocal has_visited
        for board_visited in has_visited[tuple(state.cur)]:
            if num.array_equal(state.board_state,board_visited):
                return True
        return False

    def add_visited_state(state: State):
        nonlocal has_visited
        has_visited[tuple(state.cur)].append(state.board_state)

    open_list.append(Node('',game.init_state))
    while len(open_list) > 0:
        current_state = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_state.f:
                current_state = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_state)
        nums_of_node += 1
        if nums_of_node % 1000 == 0:
            getback(nums_of_node)
        if current_state.state.goaling():
            return getback(nums_of_node,current_state.path,True)
        for action in game.possible_actions_nows(current_state.state):
            next_state = game.playing(current_state.state,action,inplace=False)
            if (is_visited(next_state)):
                continue
            add_visited_state(next_state)
            check_node_g = current_state.g + 1
            check_node_h = heuristic(next_state.cur,game.init_state.goal)
            check_node_f = check_node_g + check_node_h
            successor = Node(current_state.path+action[0],next_state,check_node_g,check_node_h,check_node_f)
            if successor in closed_list:
                continue
            open_list.append(successor)
    return getback(nums_of_node,None,True)
    
#Dang lo do :v Qua met moi :V 