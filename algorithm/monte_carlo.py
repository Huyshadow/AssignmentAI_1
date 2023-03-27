import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
from collections import deque,defaultdict

import numpy as np


from Bloxoz import Blozorx, State
from abc import ABC, abstractmethod

class MonteCarloTreeSearchNode(ABC):
    def __init__(self, state, parent=None, prev_action=None):
        """
        Parameters
        ----------
        state : GameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.parent = parent
        self.prev_action = prev_action
        self.children = []

    @property
    @abstractmethod
    def untried_actions(self):
        """
        Returns
        -------
        list of GameAction
        """
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def is_terminal_node(self):
        pass

    @abstractmethod
    def rollout(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        # choices_weights = [
        #     (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
        #     for c in self.children
        # ]
        # return self.children[np.argmax(choices_weights)]
    
        choices_weights = [
            (c.q / c.n) - c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmin(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def getHeight(self):
        if self.parent == None: return 0
        return 1 + self.parent.getHeight()


class BlozorxMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):
    def __init__(self, game: Blozorx, state: State, parent=None, prev_action=None):
        super().__init__(state, parent, prev_action)
        self.game = game
        self._number_of_visits = 0.
        # self._results = defaultdict(int)
        self._results = 0
        self._untried_actions = None
#####
    @property
    def untried_actions(self):
        if self._untried_actions is None:
            # self._untried_actions = self.state.get_legal_actions()
            self._untried_actions = self.game.possible_actions_nows(self.state)
        return self._untried_actions
#####
    @property
    def q(self):
        # wins = self._results[self.parent.state.next_to_move]
        # loses = self._results[-1 * self.parent.state.next_to_move]
        # return wins - loses
        return self._results

    @property
    def n(self):
        return self._number_of_visits
#####    
    def expand(self):
        action = self.untried_actions.pop()
        # next_state = self.state.move(action)
        next_state = self.game.playing(self.state, action, inplace=False)
        # print(next_state.cur)
        child_node = BlozorxMonteCarloTreeSearchNode(
            self.game, next_state, parent=self, prev_action=action
        )
        self.children.append(child_node)
        # print(self.)
        return child_node
#####    
    def is_terminal_node(self):
        # return self.state.is_game_over()
        return self.state.goaling()
#####
    def rollout(self):
        current_rollout_state = self.state
        step = 0
        # while not current_rollout_state.is_game_over():
        while not current_rollout_state.goaling() and step < 1000:
            # possible_moves = current_rollout_state.get_legal_actions()
            possible_moves = self.game.possible_actions_nows(current_rollout_state)
            action = self.rollout_policy(possible_moves)
            # current_rollout_state = current_rollout_state.move(action)
            current_rollout_state = self.game.playing(current_rollout_state, action, inplace=False)
            step += 1
        # return current_rollout_state.game_result
        return step
#####
    def backpropagate(self, result):
        # self._results[result] += 1.
        self._results += result
        self._number_of_visits += 1.
        if self.parent:
            self.parent.backpropagate(result + 1)
            
            
class MonteCarloTreeSearch:
    def __init__(self, node):
        """
        MonteCarloTreeSearchNode
        Parameters
        ----------
        node : MonteCarloTreeSearchNode
        """
        self.root = node
        self.num_of_node = 1
    
    def best_action(self, simulations_number=None, total_simulation_seconds=None):
        """
        Parameters
        ----------
        simulations_number : int
            number of simulations performed to get the best action
        total_simulation_seconds : float
            Amount of time the algorithm has to run. Specified in seconds
        Returns
        -------
        """

        if simulations_number is None :
            assert(total_simulation_seconds is not None)
            end_time = time.time() + total_simulation_seconds
            while True:
                v = self._tree_policy()
                reward = v.rollout()
                v.backpropagate(reward)
                if time.time() > end_time:
                    break
        else :
            for _ in range(0, simulations_number):            
                v = self._tree_policy()
                reward = v.rollout()
                v.backpropagate(reward)
        # to select best child go for exploitation only
        # return self.root.best_child(c_param=0.)
        # return self.path_to_best_child()
    
    def path_to_best_child(self):
        current_node = self.root
        
        path = "abc"
        
        while current_node.children != []:
            # print(current_node.children)
            current_node = current_node.best_child(c_param=0.)
            # print(current_node.children != [])
            # print(current_node.prev_action)
            if path == "abc":
                path = current_node.prev_action[0]
            else:
                path += current_node.prev_action[0]
            # print(path)
            
        is_done = False
        if current_node.is_terminal_node():
            is_done = True
        return self.num_of_node, path, is_done
            
    
    def _tree_policy(self):
        """
        selects node to run rollout/playout for
        Returns
        -------
        """
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                self.num_of_node += 1
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

def monte_carlo_tree_search(game:Blozorx, state:State = None, sender: Connection = None):
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
    
    root = BlozorxMonteCarloTreeSearchNode(game,state)
    mcts = MonteCarloTreeSearch(root)
    mcts.best_action(1000)
    # print(mcts.root.children)
    num_of_node, path, is_done = mcts.path_to_best_child()
    return getback(num_of_node, path, is_done)
    