import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
import numpy as num

from Bloxoz import Blozorx, State
from algorithm.bfs import *
from algorithm.dfs import *
from algorithm.a import *
from algorithm.monte_carlo import *

class Algorithm:
    Algorithm_For_Game={
        'DFS':depth_first_search,
        'BFS':breath_first_search,
        'A':a_search,
        'MONTECARLO': monte_carlo_search
    }