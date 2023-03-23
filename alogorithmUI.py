import time
import sys
import multiprocessing
from multiprocessing.connection import Connection

import pygame
import numpy as num

from Bloxoz import GamePlay, State, Blozorx
from game import UI
from algorithm import *

#Color for design 


class AlgorithUI:
    SOLUTION={
        'BFS': 'Node explored',
        'DFS': 'Node explored',
        'A*': 'Node explored',
        'MonteCarlo': 'Node explored'
    }

    def __init__(self, background, UI_height , UI_width, level,algorithm):
        self.background = background
        self.UI_height = UI_height
        self.UI_witdh = UI_width
        self.center_x = self.UI_witdh / 2
        self.center_y = self.UI_witdh / 2

        self.game = Blozorx(level)
        self.algorithm = Algorithm(algorithm)

        self.solution_cost = None
        self.path = None
        self.exe_time_s = None

        self.big_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30, bold=False)

        self.ESC  = False
        self.show = False

        self.run_algorithm()
    
    def loading_screen(self, receiver: Connection):
        msg = 'Waiting...'
        fps_  = 10
        clock_ = pygame.time.Clock() 

        while True:
            for todo in pygame.event.get():
                if todo.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if todo.type == pygame.KEYDOWN:
                    if todo.key == pygame.K_ESCAPE:
                        self.ESC = True
                        return
            if receiver.poll():
                getback = receiver.recv()
                if getback['is_done']:
                    self.solution_cost = getback['solution_cost']
                    self.path = getback['path']
                    self.exe_time_s = getback['time']
                    return
                else:
                    msg = getbackreturn_dict['msg']

    #Lam tiep sau 