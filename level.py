import json
import numpy as num

class Level:
    def __init__(self, level):
        self.level= level
        self.runLevel(f'./level/level_{level}.json')
    
    def runLevel(self,path_level):
        with open(path_level,'r') as file_map:
            map_blo = json.load(file_map)
        self.board = num.asarray(map_blo.get('map'), dtype=bool)
        self.size_y, self.size_x = self.board.shape
        
        self.start = map_blo.get('start')
        self.goal = map_blo.get('end')

        tmp_board = num.asarray(map_blo.get('map'), dtype=int)
        self.fragile_cells = [(r,c) for r,c in zip(*num.where(tmp_board == 2))]

        self.x_btn = map_blo.get('x_btn')
        self.o_btn = map_blo.get('o_btn')
        self.split_btn = map_blo.get('split_btn')
    
