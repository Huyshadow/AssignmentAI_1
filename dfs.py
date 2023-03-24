import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
from collections import deque,defaultdict

import numpy as num


from Bloxoz import Blozorx, State

def depth_first_search(game:Blozorx, state:State = None, sender: Connection = None):
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
     
    que = deque()
    que.append(('',state))
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

    while len(que) > 0:
        path,cur_state = que.pop()
        if is_visited(cur_state): 
            continue
        add_visited_state(cur_state)
        nums_of_node += 1
        if nums_of_node % 1000 == 0:
            getback(nums_of_node)
        
        for action in game.possible_actions_nows(cur_state):
            next_state = game.playing(cur_state, action, inplace=False)
            if not is_visited(next_state):
                que.append((path+action[0],next_state))
            if next_state.goaling():
                return getback(nums_of_node, path+action[0], True)
            
                    

    return getback(nums_of_node,None,True)

""" if __name__ == "__main__":
    p1 = Blozorx(2)
    depth_first_search(p1,p1.init_state,None) """