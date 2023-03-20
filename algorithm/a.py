import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing.connection import Connection
from collections import deque,defaultdict

import numpy as np


from problem import Blozorx, State

def a_first_search(problem:Blozorx, state:State = None, sender: Connection = None):
    pass