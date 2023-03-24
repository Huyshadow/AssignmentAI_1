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
WHITE = (250,250,250)
LIGHT_BLUE = (16, 109, 191)
BLACK = (80,80,80)
GRAY = (150,150,150)
RED = (150,0,0)

class AlgorithUI_Stats:
    SOLUTION={
        'BFS': 'Node explored',
        'DFS': 'Node explored',
        # Sẽ import thêm các giải thuật sau :V     
    }

    def __init__(self, background, UI_height , UI_width, level ,algorithm):
        self.background = background
        self.UI_height = UI_height
        self.UI_width = UI_width
        self.center_x = self.UI_width / 2
        self.center_y = self.UI_height / 2

        self.game = Blozorx(level)
        self.algorithm = Algorithm(algorithm)

        self.solution_cost = None
        self.path = None
        self.exe_time_s = None

        pygame.font.init()
        self.big_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30, bold=False)

        self.ESC  = False
        self.show = False

        self.running()
    
    def loading_screen(self, receiver: Connection):
        msg = 'Waiting...'
        fps_  = 20
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
                    msg = getback['msg']
            
            self.background.fill(WHITE)
            
            text = self.big_font.render(f"Level: {self.game.level_id.level:02d}", True, LIGHT_BLUE)
            text_rect = text.get_rect(center=(self.UI_width/2, 80))
            self.background.blit(text, text_rect)

            # Algorithm header
            text = self.medium_font.render(f"Algorithm: {self.algorithm.algo}", True, LIGHT_BLUE)
            text_rect = text.get_rect(center=(self.UI_width/2, 125))
            self.background.blit(text, text_rect)

            # Algorithm Calculating Status
            text = self.medium_font.render(msg, True, BLACK)
            text_rect = text.get_rect(center=(self.UI_width/2, self.UI_height/2))
            self.background.blit(text, text_rect)

            pygame.display.update()
            clock_.tick(fps_)
    #Lam tiep sau 
    def running(self):
        receiver, sender = multiprocessing.Pipe(duplex=False)
        checker = multiprocessing.Process(target=self.algorithm.running, args=(self.game,None,sender))
        checker.daemon = True
        checker.start()
        self.loading_screen(receiver)

    def show_path(self):
        return self.path
    
    def input_process(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.running()
                elif event.key == pygame.K_s and self.path is not None:
                    self.show = True
                elif event.key == pygame.K_ESCAPE:
                    self.ESC = True
    def draw(self):
        self.background.fill(WHITE)

        # header_Level
        text = self.big_font.render(f"Level: {self.game.level_id.level:02d}", True, LIGHT_BLUE)
        text_rect = text.get_rect(center=(self.UI_width/2, 80))
        self.background.blit(text, text_rect)

        #Algorithm
        text = self.medium_font.render(f"Algorithm: {self.algorithm.algo}", True, LIGHT_BLUE)
        text_rect = text.get_rect(center=(self.UI_width/2, 125))
        self.background.blit(text, text_rect)

        # Running Solution  
        if self.solution_cost is not None:
            text = self.medium_font.render(f"{self.SOLUTION[self.algorithm.algo]}: {self.solution_cost}", True, BLACK)
            text_rect = text.get_rect(center=(self.UI_width/2, 250))
            self.background.blit(text, text_rect)
        
        # Time running
        if self.exe_time_s is not None:
            text = self.medium_font.render(f"Time exec: {int(self.exe_time_s*1000)}ms", True, BLACK)
            text_rect = text.get_rect(center=(self.UI_width/2, 300))
            self.background.blit(text, text_rect)
        
        if self.path is not None:
            # Total Step
            text = self.medium_font.render(f"Total step: {len(self.path)}", 230, BLACK)
            text_rect = text.get_rect(center=(self.UI_width/2, 350))
            self.background.blit(text, text_rect)
            # Press keyword to view Solution.
            text = self.small_font.render("Press S to view solution steps.", True, GRAY)
            text_rect = text.get_rect(center=(self.UI_height/2, self.UI_width - 128))
            self.background.blit(text, text_rect)
        
        else:
            text = self.small_font.render("NO SOLUTION FOUND!", True, RED)
            text_rect = text.get_rect(center=(self.UI_width/2, 350))
            self.background.blit(text, text_rect)

    def process(self, events):
        self.input_process(events)
        self.draw()

    def should_quit(self):
        return self.ESC

    def should_show(self):
        return self.show
    
class AlgorithmUI_Show:
    def __init__(self, background, W_HEIGHT_SIZE, W_WIDTH_SIZE, level_id, solution, transition_speed_ms):
        self.game_play = UI(background, W_HEIGHT_SIZE, W_WIDTH_SIZE, level_id)
        self.background = background

        self.W_HEIGHT_SIZE = W_HEIGHT_SIZE
        self.W_WIDTH_SIZE  = W_WIDTH_SIZE
        self.CENTER_X = W_WIDTH_SIZE / 2
        self.CENTER_Y = W_HEIGHT_SIZE / 2

        self.transition_speed_ms = transition_speed_ms
        self.timer_ms = 0

        self.FONT = pygame.font.Font(None, 50)

        self.solution = solution
        self.solution_index = -1

        self.ESC = False
        self.PAUSE = False

    def next_action(self, deltatime):
        if self.PAUSE:
            return
        if self.solution_index == len(self.solution) - 1:
            return

        self.timer_ms += deltatime
        if self.timer_ms >= self.transition_speed_ms:
            self.timer_ms -= self.transition_speed_ms
            self.solution_index += 1

            coded_action = self.solution[self.solution_index]
            return GamePlay.decode_action(coded_action)


    def input_process(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESC = True
                elif event.key == pygame.K_SPACE:
                    self.PAUSE ^= True

    def draw_pause(self):
        text = self.FONT.render('PAUSE', True, WHITE)
        text_rect = text.get_rect(center=(self.W_WIDTH_SIZE/2, 35))
        self.surface.blit(text, text_rect)
            

    def process(self, events, deltatime):
        self.input_process(events)

        next_action = self.next_action(deltatime)
        if next_action is not None:
            self.game_play.action_possible(next_action)

        self.game_play.draw()
        self.game_play.process_end()

        if self.PAUSE:
            self.draw_pause()

    def should_quit(self):
        return self.ESC
    

if __name__ == '__main__':
    # with open('results/ga.txt','w') as f:
    background = pygame.display.set_mode((900,770))
    
    p1 = AlgorithUI_Stats(background, 770,900,1,'BFS')
    