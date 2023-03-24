import pygame
import copy
import sys, os

from algorithm import Algorithm
from Bloxoz import GamePlay,State,Blozorx
#Referrence
""" AVAILABLE_COLOR = (255, 255, 255)
BLOCK_COLOR = (255,20,60)
UNCONTROLLED_BLOCK_COLOR = (179,14,42)
GOAL_COLOR = (50,205,50)
BUTTON_COLOR = (105,105,105)
FLEXIBLE_CELL_COLOR = (150,150,150)
FRAGILE_CELL_COLOR = (242, 183, 5)
GAME_COLOR_BACKGROUND = (0,0,139) """
BUTTON_COLOR_XOSPLIT = (16,109,191)
CELL_COLOR = (255,255,255)
FLEXIBLE_FRAGILE_COLOR = (13,140,162)
GOAL_COLOR = (96,255,236)
BLOCK_COLOR = (123,123,123)
UNCONTROLBLOCK_COLOR=(123,11,11)
BACKGROUND_COLOR=(96,255,236)


class UI: #Design UI for Game
    def __init__(self, background, UI_height , UI_width, level):
        self.background = background
        self.UI_height = UI_height
        self.UI_witdh = UI_width
        self.center_x = self.UI_witdh / 2
        self.center_y = self.UI_height / 2
        self.level = level

        self.game = Blozorx(level)
        self.state = copy.deepcopy(self.game.init_state)

        #create the background
        self.rec_size = min(50, 700//max(self.game.level_id.size_x,self.game.level_id.size_y))
        self.x_start = self.center_x - self.game.level_id.size_x / 2 * self.rec_size
        self.y_start = self.center_y - self.game.level_id.size_y / 2 * self.rec_size
        self.ending_x = self.center_x + self.game.level_id.size_x / 2 * self.rec_size
        self.ending_y = self.center_y + self.game.level_id.size_y / 2 * self.rec_size
        #Some attribute to go
        pygame.font.init()
        self.FONT = pygame.font.Font(None, 50)
        self.moves = 0
        self.end = False 
        self.ESC  = False
    def action_possible(self, action):
        possible,_ = self.game.possible_move(self.state,action,True)
        if possible:
            self.moves += 1
        return possible
    
    def input_game(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if not self.end and event.key == pygame.K_UP:
                    possible,_ = self.game.possible_move(self.state,GamePlay.up,True)
                    if possible:
                        self.moves += 1
                elif not self.end and event.key == pygame.K_RIGHT:
                    possible,_ = self.game.possible_move(self.state,GamePlay.right,True)
                    if possible:
                        self.moves += 1
                elif not self.end and event.key == pygame.K_DOWN:
                    possible,_ = self.game.possible_move(self.state,GamePlay.down,True)
                    if possible:
                        self.moves += 1
                elif not self.end and event.key == pygame.K_LEFT:
                    possible,_ = self.game.possible_move(self.state,GamePlay.left,True)
                    if possible:
                        self.moves += 1
                elif event.key == pygame.K_ESCAPE:
                    self.ESC = True
    def draw_cell(self, position, size, color):
        pygame.draw.rect(
            self.background,color,
            (*position,size,size)
        )

    def XButton(self, position, size, cell_color=CELL_COLOR, btn_color=BUTTON_COLOR_XOSPLIT , line_color=BUTTON_COLOR_XOSPLIT):
        self.draw_cell(position,size,cell_color)
        cx = position[0]+size/2
        cy = position[1]+size/2
        btn_size = size*0.5*0.7
        pygame.draw.line(self.background,line_color,(cx-btn_size,cy-btn_size),(cx+btn_size,cy+btn_size),int(size*0.2))
        pygame.draw.line(self.background,line_color,(cx+btn_size,cy-btn_size),(cx-btn_size,cy+btn_size),int(size*0.2))

    def OButton(self, position, size, cell_color=CELL_COLOR, btn_color=BUTTON_COLOR_XOSPLIT):
        self.draw_cell(position,size,cell_color)
        cx = position[0]+size/2
        cy = position[1]+size/2
        pygame.draw.circle(self.background,btn_color,(cx,cy),size*0.5*0.8)   

    def SpliButton(self, position, size, cell_color=CELL_COLOR, btn_color=BUTTON_COLOR_XOSPLIT):
        self.draw_cell(position,size,cell_color)
        cx = position[0]+size/2
        cy = position[1]+size/2
        width = size*0.2
        height = size*0.7
        pygame.draw.line(self.background,btn_color,(cx-width,cy-height/2),(cx-width,cy+height/2),int(width))
        pygame.draw.line(self.background,btn_color,(cx+width,cy-height/2),(cx+width,cy+height/2),int(width))

    def Map_paint(self):
        for x in range(self.game.level_id.size_x):
            for y in range(self.game.level_id.size_y):
                
                start_x = self.x_start+1+x*self.rec_size
                start_y = self.y_start+1+y*self.rec_size

                if self.state.board_state[y,x]: # is available
                    cell_type = self.game.board[y,x]
                    
                    if cell_type == Blozorx.CELL_TYPE_MAP['normal']:
                        self.draw_cell(position=(start_x,start_y),
                            size=self.rec_size-1,color=CELL_COLOR)

                    elif cell_type == Blozorx.CELL_TYPE_MAP['x_btn']:
                        self.XButton(position=(start_x,start_y),
                            size=self.rec_size-1,cell_color=CELL_COLOR)

                    elif cell_type == Blozorx.CELL_TYPE_MAP['o_btn']:
                        self.OButton(position=(start_x,start_y),
                            size=self.rec_size-1,cell_color=CELL_COLOR)

                    elif cell_type == Blozorx.CELL_TYPE_MAP['split_btn']:
                        self.SpliButton(position=(start_x,start_y),
                            size=self.rec_size-1,cell_color=CELL_COLOR)

                    elif cell_type == Blozorx.CELL_TYPE_MAP['flexible']:
                        self.draw_cell(position=(start_x,start_y),
                            size=self.rec_size-1,color=FLEXIBLE_FRAGILE_COLOR)

                    elif cell_type == Blozorx.CELL_TYPE_MAP['fragile']:
                        self.draw_cell(position=(start_x,start_y),
                            size=self.rec_size-1,color=FLEXIBLE_FRAGILE_COLOR)


    def goal_paint(self):
        start_x = self.x_start+1+self.state.goal[1]*self.rec_size
        start_y = self.y_start+1+self.state.goal[0]*self.rec_size
        self.draw_cell(
            position=(start_x,start_y),
            size=self.rec_size-1,
            color=GOAL_COLOR)

    def block_paint(self):
        if self.state.standing():
            x = self.x_start+1+self.state.cur[1]*self.rec_size
            y = self.y_start+1+self.state.cur[0]*self.rec_size
            self.draw_cell(position=(x,y),size=self.rec_size-1,color=BLOCK_COLOR)
        else:
            x0 = self.x_start+1+self.state.cur[1]*self.rec_size
            y0 = self.y_start+1+self.state.cur[0]*self.rec_size
            x1 = self.x_start+1+self.state.cur[3]*self.rec_size
            y1 = self.y_start+1+self.state.cur[2]*self.rec_size
            self.draw_cell(position=(x0,y0),size=self.rec_size-1,color=BLOCK_COLOR)
            self.draw_cell(position=(x1,y1),size=self.rec_size-1,color=BLOCK_COLOR)
            
            if self.state.lying():
                self.draw_cell(position=(x1,y1),size=self.rec_size-1,color=BLOCK_COLOR)
                self.draw_cell(position=((x0+x1)/2,(y0+y1)/2),size=self.rec_size-1,color=BLOCK_COLOR)
            else: # splited state
                self.draw_cell(position=(x1,y1),size=self.rec_size-1,color=UNCONTROLBLOCK_COLOR)
    
    def draw(self):
        charRect = pygame.Rect((0,0),(1000, 600))
        pygame.init()
        charImage = pygame.image.load(os.path.join("design_game", "Background2.png"))
        charImage = pygame.transform.scale(charImage, charRect.size)
        charImage = charImage.convert()
        self.background.blit(charImage,charRect)
        self.Map_paint()
        self.goal_paint()
        self.block_paint()

    def process_end(self):
        if self.state.goaling():
            self.over = True
            msg = f'Win at {self.moves} moves. Press ESC to go back.'
        else:
            msg = f'Moves: {self.moves:05d}'

        text = self.FONT.render(msg, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.UI_witdh/2, self.UI_height - 35))
        self.background.blit(text, text_rect)

    def process(self, events):
        self.input_game(events)
        self.draw()
        self.process_end()

    def should_quit(self):
        return self.ESC
