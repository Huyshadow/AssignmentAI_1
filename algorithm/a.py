import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
from collections import deque,defaultdict
from math import sqrt

import numpy as num

#in This A* Search, we use h(x) is Eucledian

from Bloxoz import State, Blozorx

class Node:
    def __init__(self,path,state:State , f = 0 , g = 0, h = 0):
        self.path = path
        self.state = state
        self.f = f
        self.g = g
        self.h = h
        

def Eucledian_calculate(x0:int,y0:int, x1:int, y1:int):
    h_x = sqrt(((x0 - x1) ** 2) + ((y0 - y1) ** 2))
    return h_x

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
    
    has_visited = defaultdict(list)

    open_list = []
    closed_list = []

    def is_visited(state: State):
        nonlocal has_visited
        for board_visited in has_visited[tuple(state.cur)]:
            if num.array_equal(state.board_state,board_visited):
                return True
        return False

    def add_visited_state(state: State):
        nonlocal has_visited
        has_visited[tuple(state.cur)].append(state.board_state)

    open_list.append(Node('',state, 0 , 0 , 0))
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        for i, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = i
        
        open_list.pop(current_index)
        closed_list.append(current_node)

    